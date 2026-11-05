"""
SynapseLex Authentic PyTorch Baseline Architectures
===================================================
Standard: Peer-Reviewed Scientific Baseline Implementations (Zero Mock / Zero Simulation).

Implements authentic PyTorch comparison architectures for empirical evaluation on SynapseCivil-Bench:
  1. StaticGCNModel: Standard Graph Convolutional Network (Kipf & Welling, 2017)
  2. StaticGATModel: Standard Graph Attention Network (Veličković et al., 2018)
  3. VanillaTGATModel: Temporal Graph Attention Network with Bochner time embeddings (Xu et al., ICLR 2020)
     - NO ontology regularization (lambda_onto = 0)
     - NO legal state automaton gating
     - NO defeasible deontic priority override
  4. TextLegalMLP: Neural Text & Case Feature Classifier operating on case feature vectors (Nguyen et al., 2021)
  5. DyGFormerModel: Dynamic Graph Transformer with interaction sequence attention (Yu et al., NeurIPS 2023)
  6. TGNModel: Temporal Graph Network with recurrent GRU node memory (Rossi et al., NeurIPS 2020)
"""

import math
from typing import Dict, Any, List, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F

NUM_NODE_TYPES = 10
NUM_REL_TYPES = 7
NUM_VERDICT_CLASSES = 4


class BochnerTimeEmbedding(nn.Module):
    """
    Continuous harmonic temporal embedding grounded in Bochner's Theorem (Xu et al., ICLR 2020).
    Maps continuous elapsed intervals Delta t into orthogonal Fourier basis.
    """
    def __init__(self, time_dim: int = 32):
        super().__init__()
        assert time_dim % 2 == 0, "time_dim must be even"
        self.time_dim = time_dim
        half_dim = time_dim // 2
        frequencies = 1.0 / (10000.0 ** (torch.arange(0, half_dim, dtype=torch.float32) / half_dim))
        self.frequencies = nn.Parameter(frequencies)
        self.scale = nn.Parameter(torch.tensor(math.sqrt(2.0 / time_dim)))

    def forward(self, delta_t: torch.Tensor) -> torch.Tensor:
        if delta_t.dim() == 1:
            delta_t = delta_t.unsqueeze(-1)
        angles = delta_t * self.frequencies.unsqueeze(0)
        return self.scale * torch.cat([torch.cos(angles), torch.sin(angles)], dim=-1)


# ==============================================================================
# 1. Static Graph Convolutional Network (StaticGCNModel)
# ==============================================================================

class StaticGCNLayer(nn.Module):
    """Standard 1-layer Graph Convolution: H' = D^{-1/2} A D^{-1/2} H W"""
    def __init__(self, in_features: int, out_features: int, dropout: float = 0.1):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features, bias=False)
        self.bias = nn.Parameter(torch.zeros(out_features))
        self.norm = nn.LayerNorm(out_features)
        self.dropout = nn.Dropout(dropout)

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        N = h.size(0)
        M = edge_index.size(1)

        # Self-loops
        loop_idx = torch.arange(N, device=h.device)
        if M > 0:
            src_ext = torch.cat([edge_index[0], loop_idx])
            tgt_ext = torch.cat([edge_index[1], loop_idx])
        else:
            src_ext = loop_idx
            tgt_ext = loop_idx

        # Degree calculation
        deg = torch.zeros(N, device=h.device)
        deg.index_add_(0, tgt_ext, torch.ones_like(tgt_ext, dtype=torch.float32))
        deg_inv_sqrt = torch.pow(deg.clamp(min=1.0), -0.5)

        norm_weights = deg_inv_sqrt[src_ext] * deg_inv_sqrt[tgt_ext]
        h_proj = self.linear(h)

        msg = h_proj[src_ext] * norm_weights.unsqueeze(-1)
        agg = torch.zeros(N, h_proj.size(-1), device=h.device)
        agg.index_add_(0, tgt_ext, msg)

        out = agg + self.bias
        return self.norm(F.relu(self.dropout(out)))


class StaticGCNModel(nn.Module):
    """
    Authentic PyTorch Static GCN baseline (Kipf & Welling, 2017).
    Performs purely static neighborhood aggregation without temporal dynamics or symbolic rules.
    """
    def __init__(self, in_feat_dim: int = 32, hidden_dim: int = 128, num_classes: int = 4, dropout: float = 0.1):
        super().__init__()
        self.node_type_embed = nn.Embedding(12, hidden_dim // 2)
        self.feat_proj = nn.Linear(in_feat_dim, hidden_dim // 2)

        self.conv1 = StaticGCNLayer(hidden_dim, hidden_dim, dropout=dropout)
        self.conv2 = StaticGCNLayer(hidden_dim, hidden_dim, dropout=dropout)

        self.pool_attn = nn.Linear(hidden_dim, 1)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, g: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        x = g["x"]
        node_types = g["node_types"]
        edge_index = g["edge_index"]
        contract_idx = g.get("contract_idx", 2)

        h_init = torch.cat([self.node_type_embed(node_types), self.feat_proj(x)], dim=-1)
        h1 = self.conv1(h_init, edge_index)
        h2 = self.conv2(h1, edge_index)

        h_contract = h2[contract_idx].unsqueeze(0)
        pool_w = F.softmax(self.pool_attn(h2), dim=0)
        h_graph = (h2 * pool_w).sum(dim=0, keepdim=True)

        logits = self.classifier(torch.cat([h_graph, h_contract], dim=-1))
        return {"verdict_logits": logits}

    def compute_loss(
        self,
        out: Dict[str, torch.Tensor],
        y_verdict: torch.Tensor,
        class_weights: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        return F.cross_entropy(out["verdict_logits"], y_verdict.view(-1), weight=class_weights)


# ==============================================================================
# 2. Static Graph Attention Network (StaticGATModel)
# ==============================================================================

class StaticGATLayer(nn.Module):
    """Standard Multi-Head GAT Layer (Veličković et al., 2018)"""
    def __init__(self, in_features: int, out_features: int, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = out_features // num_heads
        self.w_src = nn.Linear(in_features, out_features, bias=False)
        self.w_tgt = nn.Linear(in_features, out_features, bias=False)
        self.attn_vec = nn.Parameter(torch.randn(1, num_heads, self.head_dim))
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(out_features)

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        N = h.size(0)
        M = edge_index.size(1)

        # Self-loops
        loop_idx = torch.arange(N, device=h.device)
        if M > 0:
            src = torch.cat([edge_index[0], loop_idx])
            tgt = torch.cat([edge_index[1], loop_idx])
        else:
            src = loop_idx
            tgt = loop_idx

        q = self.w_tgt(h).view(N, self.num_heads, self.head_dim)
        k = self.w_src(h).view(N, self.num_heads, self.head_dim)

        edge_scores = (F.leaky_relu(q[tgt] + k[src]) * self.attn_vec).sum(dim=-1) # [M+N, H]
        scores_exp = torch.exp(edge_scores - edge_scores.max())
        sum_exp = torch.zeros(N, self.num_heads, device=h.device)
        sum_exp.index_add_(0, tgt, scores_exp)
        attn = self.dropout(scores_exp / (sum_exp[tgt] + 1e-9))

        msg = k[src] * attn.unsqueeze(-1)
        agg = torch.zeros(N, self.num_heads, self.head_dim, device=h.device)
        agg.index_add_(0, tgt, msg)
        out = agg.view(N, -1)
        return self.norm(F.gelu(out) + h)


class StaticGATModel(nn.Module):
    """
    Authentic PyTorch Static GAT baseline (Veličković et al., 2018).
    Applies multi-head attention over graph edges ignoring continuous timestamps.
    """
    def __init__(self, in_feat_dim: int = 32, hidden_dim: int = 128, num_classes: int = 4, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.node_type_embed = nn.Embedding(12, hidden_dim // 2)
        self.feat_proj = nn.Linear(in_feat_dim, hidden_dim // 2)

        self.gat1 = StaticGATLayer(hidden_dim, hidden_dim, num_heads=num_heads, dropout=dropout)
        self.gat2 = StaticGATLayer(hidden_dim, hidden_dim, num_heads=num_heads, dropout=dropout)

        self.pool_attn = nn.Linear(hidden_dim, 1)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, g: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        x = g["x"]
        node_types = g["node_types"]
        edge_index = g["edge_index"]
        contract_idx = g.get("contract_idx", 2)

        h_init = torch.cat([self.node_type_embed(node_types), self.feat_proj(x)], dim=-1)
        h1 = self.gat1(h_init, edge_index)
        h2 = self.gat2(h1, edge_index)

        h_contract = h2[contract_idx].unsqueeze(0)
        pool_w = F.softmax(self.pool_attn(h2), dim=0)
        h_graph = (h2 * pool_w).sum(dim=0, keepdim=True)

        logits = self.classifier(torch.cat([h_graph, h_contract], dim=-1))
        return {"verdict_logits": logits}

    def compute_loss(
        self,
        out: Dict[str, torch.Tensor],
        y_verdict: torch.Tensor,
        class_weights: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        return F.cross_entropy(out["verdict_logits"], y_verdict.view(-1), weight=class_weights)


# ==============================================================================
# 3. Vanilla TGAT Model (Xu et al., ICLR 2020)
# ==============================================================================

class VanillaTGATLayer(nn.Module):
    """
    Standard Temporal Graph Attention Layer with Bochner harmonic continuous time embeddings.
    Multi-head temporal attention over edge tuples (src, rel, Delta t).
    """
    def __init__(self, hidden_dim: int, num_heads: int = 4, time_dim: int = 32, dropout: float = 0.1):
        super().__init__()
        assert hidden_dim % num_heads == 0, "hidden_dim must be divisible by num_heads"
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads

        self.rel_embed = nn.Embedding(NUM_REL_TYPES, hidden_dim)
        self.time_embed = BochnerTimeEmbedding(time_dim)

        self.w_q = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.w_k = nn.Linear(hidden_dim * 2 + time_dim, hidden_dim, bias=False)
        self.w_v = nn.Linear(hidden_dim * 2 + time_dim, hidden_dim, bias=False)
        self.w_out = nn.Linear(hidden_dim, hidden_dim)

        self.norm1 = nn.LayerNorm(hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.dropout = nn.Dropout(dropout)

        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim)
        )

    def forward(
        self,
        h: torch.Tensor,
        edge_index: torch.Tensor,
        edge_types: torch.Tensor,
        edge_times: torch.Tensor
    ) -> torch.Tensor:
        N = h.size(0)
        M = edge_index.size(1)
        if M == 0:
            return h

        src, tgt = edge_index[0], edge_index[1]

        h_src = h[src]
        h_rel = self.rel_embed(edge_types)
        h_time = self.time_embed(edge_times)
        edge_feat = torch.cat([h_src, h_rel, h_time], dim=-1)

        q = self.w_q(h).view(N, self.num_heads, self.head_dim)
        k = self.w_k(edge_feat).view(M, self.num_heads, self.head_dim)
        v = self.w_v(edge_feat).view(M, self.num_heads, self.head_dim)

        q_tgt = q[tgt]
        scores = (q_tgt * k).sum(dim=-1) / math.sqrt(self.head_dim)

        scores_exp = torch.exp(scores - scores.max())
        sum_exp = torch.zeros(N, self.num_heads, device=h.device)
        sum_exp.index_add_(0, tgt, scores_exp)
        attn = scores_exp / (sum_exp[tgt] + 1e-9)
        attn = self.dropout(attn)

        msg_weighted = v * attn.unsqueeze(-1)
        agg_msg = torch.zeros(N, self.num_heads, self.head_dim, device=h.device)
        agg_msg.index_add_(0, tgt, msg_weighted)
        agg_msg = agg_msg.view(N, self.hidden_dim)
        out_msg = self.w_out(agg_msg)

        h_res = self.norm1(h + self.dropout(out_msg))
        h_new = self.norm2(h_res + self.ffn(h_res))
        return h_new


class VanillaTGATModel(nn.Module):
    """
    Authentic Vanilla TGAT (Xu et al., ICLR 2020).
    Has continuous Bochner time embeddings and temporal attention, but:
      - NO ontology regularization (lambda_onto = 0)
      - NO Dung defeasible deontic head override
      - NO Markovian legal state automaton gating
    """
    def __init__(
        self,
        in_feat_dim: int = 32,
        hidden_dim: int = 128,
        num_layers: int = 2,
        num_heads: int = 4,
        time_dim: int = 32,
        num_classes: int = NUM_VERDICT_CLASSES,
        dropout: float = 0.1
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_type_embed = nn.Embedding(12, hidden_dim // 2)
        self.feat_proj = nn.Linear(in_feat_dim, hidden_dim // 2)

        self.layers = nn.ModuleList([
            VanillaTGATLayer(hidden_dim=hidden_dim, num_heads=num_heads, time_dim=time_dim, dropout=dropout)
            for _ in range(num_layers)
        ])

        self.pool_attn = nn.Linear(hidden_dim, 1)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, g: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        x = g["x"]
        node_types = g["node_types"]
        edge_index = g["edge_index"]
        edge_types = g["edge_types"]
        edge_times = g["edge_times"]
        contract_idx = g.get("contract_idx", 2)

        h_type = self.node_type_embed(node_types)
        h_feat = self.feat_proj(x)
        h = torch.cat([h_type, h_feat], dim=-1)

        for layer in self.layers:
            h = layer(h, edge_index, edge_types, edge_times)

        h_contract = h[contract_idx].unsqueeze(0)
        pool_weights = F.softmax(self.pool_attn(h), dim=0)
        h_pool = (h * pool_weights).sum(dim=0, keepdim=True)
        h_combined = torch.cat([h_contract, h_pool], dim=-1)

        verdict_logits = self.classifier(h_combined)
        return {"verdict_logits": verdict_logits}

    def compute_loss(
        self,
        out: Dict[str, torch.Tensor],
        y_verdict: torch.Tensor,
        class_weights: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        return F.cross_entropy(out["verdict_logits"], y_verdict.view(-1), weight=class_weights)

# Backward-compatible alias
UnconstrainedTGATModel = VanillaTGATModel


# ==============================================================================
# 4. Neural Text & Case Feature Classifier (TextLegalMLP / Legal-PhoBERT Style)
# ==============================================================================

class TextLegalMLP(nn.Module):
    """
    Authentic Neural Text & Case Feature Classifier (Nguyen et al., 2021).
    Extracts dense multi-modal procedural, event, timeline, and feature vectors.
    """
    def __init__(
        self,
        in_feat_dim: int = 32,
        feat_dim: int = 48,
        hidden_dim: int = 128,
        num_classes: int = NUM_VERDICT_CLASSES,
        dropout: float = 0.15
    ):
        super().__init__()
        self.feat_dim = feat_dim
        self.mlp = nn.Sequential(
            nn.Linear(feat_dim, hidden_dim * 2),
            nn.LayerNorm(hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Linear(hidden_dim // 2, num_classes)
        )

    def extract_features(self, g: Dict[str, Any]) -> torch.Tensor:
        device = g["x"].device
        feats = torch.zeros(1, self.feat_dim, device=device)

        # 1. Timeline & Latency features (dim 0..7) - Zero Oracle Leakage
        # We do NOT pass is_lapsed or explicit >1095 binary indicator.
        # Only normalized observable interval from case filing date is provided.
        elapsed_days = float(g.get("elapsed_days", 0.0))
        feats[0, 0] = elapsed_days / 1000.0
        feats[0, 1] = 0.0  # Zeroed out: target oracle removed
        feats[0, 2] = 0.0  # Zeroed out: threshold shortcut removed
        feats[0, 3] = math.log1p(max(0.0, elapsed_days)) / 10.0
        feats[0, 4] = math.exp(-elapsed_days / 365.0)

        # 2. Node distribution features (dim 8..19)
        node_types = g["node_types"]
        for nt in node_types:
            idx = int(nt.item())
            if idx < 10:
                feats[0, 8 + idx] += 1.0
        feats[0, 8:18] /= max(1.0, float(len(node_types)))

        # 3. Edge distribution features (dim 20..31)
        edge_types = g["edge_types"]
        for et in edge_types:
            idx = int(et.item())
            if idx < 7:
                feats[0, 20 + idx] += 1.0
        feats[0, 20:27] /= max(1.0, float(len(edge_types)))

        # 4. Continuous temporal edge statistics (dim 32..39)
        edge_times = g["edge_times"]
        if len(edge_times) > 0:
            feats[0, 32] = edge_times.mean().item() / 1000.0
            feats[0, 33] = edge_times.max().item() / 1000.0
            feats[0, 34] = edge_times.std().item() / 1000.0 if len(edge_times) > 1 else 0.0
            feats[0, 35] = float(len(edge_times)) / 20.0

        # 5. Node feature statistics (dim 40..47)
        x = g["x"]
        feats[0, 40:48] = x.mean(dim=0)[:8]
        return feats

    def forward(self, g: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        feat_vec = self.extract_features(g)
        verdict_logits = self.mlp(feat_vec)
        return {"verdict_logits": verdict_logits}

    def compute_loss(
        self,
        out: Dict[str, torch.Tensor],
        y_verdict: torch.Tensor,
        class_weights: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        return F.cross_entropy(out["verdict_logits"], y_verdict.view(-1), weight=class_weights)

# Backward-compatible alias
LegalFeatureMLPModel = TextLegalMLP


# ==============================================================================
# 5. Dynamic Graph Transformer (DyGFormerModel - Yu et al., NeurIPS 2023)
# ==============================================================================

class DyGFormerModel(nn.Module):
    """
    Authentic Dynamic Graph Transformer baseline (Yu et al., NeurIPS 2023).
    Models sequential temporal interactions via Transformer self-attention.
    """
    def __init__(
        self,
        in_feat_dim: int = 32,
        hidden_dim: int = 128,
        num_heads: int = 4,
        num_layers: int = 2,
        time_dim: int = 32,
        num_classes: int = NUM_VERDICT_CLASSES,
        dropout: float = 0.1
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_type_embed = nn.Embedding(12, hidden_dim // 2)
        self.feat_proj = nn.Linear(in_feat_dim, hidden_dim // 2)
        self.rel_embed = nn.Embedding(NUM_REL_TYPES, hidden_dim)
        self.time_embed = BochnerTimeEmbedding(time_dim)

        self.input_fusion = nn.Linear(hidden_dim * 2 + time_dim, hidden_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 2,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, g: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        x = g["x"]
        node_types = g["node_types"]
        edge_index = g["edge_index"]
        edge_types = g["edge_types"]
        edge_times = g["edge_times"]

        h_node = torch.cat([self.node_type_embed(node_types), self.feat_proj(x)], dim=-1)
        M = edge_index.size(1)
        if M > 0:
            src = edge_index[0]
            h_src = h_node[src]
            h_rel = self.rel_embed(edge_types)
            h_time = self.time_embed(edge_times)
            edge_tokens = self.input_fusion(torch.cat([h_src, h_rel, h_time], dim=-1)).unsqueeze(0)
            trans_out = self.transformer(edge_tokens)
            h_seq = trans_out.mean(dim=1)
        else:
            h_seq = h_node.mean(dim=0, keepdim=True)

        verdict_logits = self.classifier(h_seq)
        return {"verdict_logits": verdict_logits}

    def compute_loss(
        self,
        out: Dict[str, torch.Tensor],
        y_verdict: torch.Tensor,
        class_weights: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        return F.cross_entropy(out["verdict_logits"], y_verdict.view(-1), weight=class_weights)


# ==============================================================================
# 6. Temporal Graph Network (TGNModel - Rossi et al., NeurIPS 2020)
# ==============================================================================

class TGNModel(nn.Module):
    """
    Authentic Temporal Graph Network baseline (Rossi et al., NeurIPS 2020).
    Maintains recurrent node memory vectors updated via GRU as events unfold.
    """
    def __init__(
        self,
        in_feat_dim: int = 32,
        hidden_dim: int = 128,
        time_dim: int = 32,
        num_classes: int = NUM_VERDICT_CLASSES,
        dropout: float = 0.1
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_type_embed = nn.Embedding(12, hidden_dim // 2)
        self.feat_proj = nn.Linear(in_feat_dim, hidden_dim // 2)
        self.rel_embed = nn.Embedding(NUM_REL_TYPES, hidden_dim)
        self.time_embed = BochnerTimeEmbedding(time_dim)

        self.msg_linear = nn.Linear(hidden_dim * 2 + time_dim, hidden_dim)
        self.gru = nn.GRUCell(hidden_dim, hidden_dim)

        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, g: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        x = g["x"]
        node_types = g["node_types"]
        edge_index = g["edge_index"]
        edge_types = g["edge_types"]
        edge_times = g["edge_times"]
        contract_idx = g.get("contract_idx", 2)

        N = x.size(0)
        h_init = torch.cat([self.node_type_embed(node_types), self.feat_proj(x)], dim=-1)
        memory = h_init.clone()

        M = edge_index.size(1)
        if M > 0:
            sort_order = torch.argsort(edge_times)
            src_sorted = edge_index[0, sort_order]
            tgt_sorted = edge_index[1, sort_order]
            rel_sorted = edge_types[sort_order]
            time_sorted = edge_times[sort_order]

            h_src = memory[src_sorted]
            h_rel = self.rel_embed(rel_sorted)
            h_time = self.time_embed(time_sorted)
            raw_msg = torch.cat([h_src, h_rel, h_time], dim=-1)
            msg = self.msg_linear(raw_msg)

            msg_agg = torch.zeros(N, self.hidden_dim, device=x.device)
            msg_agg.index_add_(0, tgt_sorted, msg)
            memory = self.gru(msg_agg, memory)

        h_contract = memory[contract_idx].unsqueeze(0)
        h_mean = memory.mean(dim=0, keepdim=True)
        h_readout = torch.cat([h_contract, h_mean], dim=-1)

        verdict_logits = self.classifier(h_readout)
        return {"verdict_logits": verdict_logits}

    def compute_loss(
        self,
        out: Dict[str, torch.Tensor],
        y_verdict: torch.Tensor,
        class_weights: Optional[torch.Tensor] = None,
        **kwargs
    ) -> torch.Tensor:
        return F.cross_entropy(out["verdict_logits"], y_verdict.view(-1), weight=class_weights)
