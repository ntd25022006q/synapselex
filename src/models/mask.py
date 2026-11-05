"""
SynapseLex: Amortized Structural Compilation Mask (M_defeasible)
================================================================
Implements the Description Logic TBox compiled algebraic projection mask
M_defeasible and state-conditional log-projection operator from Theorem 2
and Theorem 3 of the SynapseLex paper.

Guarantees:
1. 100% Deductive Soundness: Zero substantive remedy logits when state is Extinguished or Void.
2. O(1) Inference Amortization: Eliminates 2-NExpTime hypertableau reasoning at runtime.

Remedies / Adjudication Classes:
- 0: ACCEPT_DEPOSIT_FORFEITURE     (Substantive remedy)
- 1: ACCEPT_DOUBLE_DEPOSIT_REFUND  (Substantive remedy)
- 2: DISMISS_STATUTE_LAPSED        (Procedural remedy)
- 3: DECLARE_CONTRACT_VOID         (Nullity remedy)

Legal Contract States:
- 0: Valid
- 1: Voidable
- 2: Void_Ab_Initio
- 3: Extinguished

Authors: Nguyen Tien Dat (VNU-IS) & SynapseLex Research Team
Standard: NeurIPS / AAAI / Q1 AI and Law Rigor
"""

from typing import Union, Tuple, Optional
import torch
import torch.nn.functional as F

# Precompiled Exact Algebraic Projection Mask (Theorem 2, Eq. 528)
# Rows: States [Valid(0), Voidable(1), Void_Ab_Initio(2), Extinguished(3)]
# Cols: Verdicts [Forfeit(0), DoubleRefund(1), Dismiss(2), Void(3)]
M_DEFEASIBLE = torch.tensor([
    [1.0, 1.0, 0.0, 0.0],  # Valid: substantive remedies allowed; dismissal/void prohibited
    [1.0, 1.0, 0.0, 1.0],  # Voidable: substantive remedies or judicial void declaration allowed
    [0.0, 0.0, 0.0, 1.0],  # Void_Ab_Initio: ONLY contract void declaration permitted
    [0.0, 0.0, 1.0, 0.0],  # Extinguished: ONLY procedural dismissal permitted (substantive blocked)
], dtype=torch.float32)

NEG_INF = -1e9  # Numerically stable surrogate for -infinity in log-projection


def get_defeasible_projection_vector(
    state: Union[int, torch.Tensor],
    device: Optional[torch.device] = None,
    dtype: torch.dtype = torch.float32
) -> torch.Tensor:
    """
    Computes m_proj(s) = log(M_defeasible[s, :])
    Forbidden classes receive NEG_INF (-1e9).
    """
    mask_matrix = M_DEFEASIBLE.to(device=device, dtype=dtype)
    
    if isinstance(state, int):
        row = mask_matrix[state]
        m_proj = torch.where(row > 0.5, torch.zeros_like(row), torch.full_like(row, NEG_INF))
        return m_proj
        
    elif isinstance(state, torch.Tensor):
        if state.dim() == 0:
            state = state.unsqueeze(0)
        state_idx = state.long().view(-1)
        rows = mask_matrix[state_idx]  # [batch_size, 4]
        m_proj = torch.where(rows > 0.5, torch.zeros_like(rows), torch.full_like(rows, NEG_INF))
        return m_proj
    else:
        raise TypeError(f"Unsupported state type: {type(state)}")


def apply_amortized_mask(
    verdict_logits: torch.Tensor,
    contract_state: Union[int, torch.Tensor]
) -> torch.Tensor:
    """
    Applies the amortized TBox projection mask:
    z_tilde = z_verdict + m_proj(s)
    
    Guarantees:
    - If state == Extinguished (3):
      z_tilde[..., 0] = -inf, z_tilde[..., 1] = -inf, P(substantive) == 0.0
    - If state == Void_Ab_Initio (2):
      z_tilde[..., 0] = -inf, z_tilde[..., 1] = -inf, z_tilde[..., 2] = -inf
    """
    device = verdict_logits.device
    dtype = verdict_logits.dtype
    m_proj = get_defeasible_projection_vector(contract_state, device=device, dtype=dtype)
    
    if verdict_logits.dim() == 1 and m_proj.dim() == 2:
        m_proj = m_proj.squeeze(0)
        
    return verdict_logits + m_proj


def compute_defeasible_remedy_probabilities(
    verdict_logits: torch.Tensor,
    contract_state: Union[int, torch.Tensor]
) -> torch.Tensor:
    """
    Computes softmax probabilities after applying the amortized defeasible projection mask:
    P_theta(y | s) = Softmax(z_verdict + log M_defeasible[s, :])
    """
    masked_logits = apply_amortized_mask(verdict_logits, contract_state)
    return F.softmax(masked_logits, dim=-1)
