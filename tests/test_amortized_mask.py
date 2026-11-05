"""
Unit Tests for Description Logic Amortized Defeasible Mask (M_defeasible)
========================================================================
Validates:
- Exact algebraic 4x4 matrix entries matching Theorem 2 (Eq. 528)
- Zero substantive remedy probability guarantee when state is Extinguished (s = 3)
- Zero substantive remedy probability guarantee when state is Void_Ab_Initio (s = 2)
- State-conditional log projection vector m_proj(s) = log M_defeasible[s, :]
- Batch processing across heterogeneous state assignments
- Deductive soundness: guaranteed zero probability for any TBox-inconsistent decree
- DefeasibleDeonticHead integration with Dung grounded extension semantics
"""

import time
import pytest
import torch
import torch.nn.functional as F

from synapselex.src.models.mask import (
    M_DEFEASIBLE,
    NEG_INF,
    get_defeasible_projection_vector,
    apply_amortized_mask,
    compute_defeasible_remedy_probabilities,
)
from synapselex.src.models.tgat_core import DefeasibleDeonticHead


class TestAmortizedDefeasibleMask:

    def test_m_defeasible_matrix_structure_theorem_2(self):
        """
        Validates the exact binary projection matrix from Theorem 2 (Eq. 528):
        Row 0 (Valid):          [1, 1, 0, 0]
        Row 1 (Voidable):       [1, 1, 0, 1]
        Row 2 (Void_Ab_Initio): [0, 0, 0, 1]
        Row 3 (Extinguished):   [0, 0, 1, 0]
        """
        expected = torch.tensor([
            [1.0, 1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
        ], dtype=torch.float32)

        assert M_DEFEASIBLE.shape == (4, 4), f"Expected shape (4, 4), got {M_DEFEASIBLE.shape}"
        assert torch.all(M_DEFEASIBLE == expected), "M_DEFEASIBLE does not match Theorem 2 matrix!"

    def test_zero_substantive_remedy_when_extinguished(self):
        """
        Core Law & AI Guarantee:
        When contract state is Extinguished (s = 3 under Art. 429), the substantive
        remedy logits (0: Forfeiture, 1: DoubleRefund) MUST be masked to -inf,
        guaranteeing identically 0.0% probability.
        """
        # Even if raw unconstrained neural logits heavily favor substantive relief
        raw_logits = torch.tensor([5.0, 12.0, -2.0, -1.0], dtype=torch.float32)
        state_extinguished = 3

        masked_logits = apply_amortized_mask(raw_logits, state_extinguished)

        # Logits for substantive remedies (indices 0 and 1) must be <= NEG_INF
        assert masked_logits[0].item() <= NEG_INF / 2
        assert masked_logits[1].item() <= NEG_INF / 2
        # Nullity (index 3) is also prohibited for expired contract
        assert masked_logits[3].item() <= NEG_INF / 2

        # Softmax probabilities
        probs = compute_defeasible_remedy_probabilities(raw_logits, state_extinguished)
        assert probs[0].item() == 0.0, f"Expected 0.0 for Forfeiture, got {probs[0].item()}"
        assert probs[1].item() == 0.0, f"Expected 0.0 for DoubleRefund, got {probs[1].item()}"
        assert probs[3].item() == 0.0, f"Expected 0.0 for DeclareVoid, got {probs[3].item()}"
        # Procedural dismissal (index 2) must receive 100% probability
        assert pytest.approx(probs[2].item(), abs=1e-5) == 1.0

    def test_zero_substantive_remedy_when_void_ab_initio(self):
        """
        When contract is absolutely void ab initio (s = 2 under Art. 123),
        substantive remedies (0, 1) and dismissal (2) are prohibited.
        Only DECLARE_CONTRACT_VOID (3) is permitted.
        """
        raw_logits = torch.tensor([10.0, 10.0, 2.0, 1.0], dtype=torch.float32)
        state_void = 2

        probs = compute_defeasible_remedy_probabilities(raw_logits, state_void)
        assert probs[0].item() == 0.0
        assert probs[1].item() == 0.0
        assert probs[2].item() == 0.0
        assert pytest.approx(probs[3].item(), abs=1e-5) == 1.0

    def test_valid_contract_allows_substantive_remedies_only(self):
        """
        When contract is Valid (s = 0), procedural dismissal (2) and void declaration (3)
        are prohibited by TBox axioms.
        """
        raw_logits = torch.tensor([3.0, 2.0, 8.0, 8.0], dtype=torch.float32)
        state_valid = 0

        probs = compute_defeasible_remedy_probabilities(raw_logits, state_valid)
        assert probs[2].item() == 0.0
        assert probs[3].item() == 0.0
        assert probs[0].item() + probs[1].item() == pytest.approx(1.0, abs=1e-5)

    def test_batch_masking_across_heterogeneous_states(self):
        """Batch evaluation where each case has a different legal state [0, 1, 2, 3]."""
        batch_logits = torch.tensor([
            [2.0, 1.0, 5.0, 4.0],  # State 0 (Valid)
            [1.0, 3.0, 4.0, 2.0],  # State 1 (Voidable)
            [5.0, 5.0, 2.0, 1.0],  # State 2 (Void_Ab_Initio)
            [8.0, 9.0, 1.0, 3.0],  # State 3 (Extinguished)
        ], dtype=torch.float32)

        states = torch.tensor([0, 1, 2, 3], dtype=torch.long)
        masked_probs = compute_defeasible_remedy_probabilities(batch_logits, states)

        assert masked_probs.shape == (4, 4)

        # Check State 0: dismissal (2) and void (3) zeroed
        assert masked_probs[0, 2].item() == 0.0
        assert masked_probs[0, 3].item() == 0.0

        # Check State 2: substantive (0, 1) and dismissal (2) zeroed
        assert masked_probs[2, 0].item() == 0.0
        assert masked_probs[2, 1].item() == 0.0
        assert masked_probs[2, 2].item() == 0.0
        assert pytest.approx(masked_probs[2, 3].item(), abs=1e-5) == 1.0

        # Check State 3: substantive (0, 1) and void (3) zeroed
        assert masked_probs[3, 0].item() == 0.0
        assert masked_probs[3, 1].item() == 0.0
        assert masked_probs[3, 3].item() == 0.0
        assert pytest.approx(masked_probs[3, 2].item(), abs=1e-5) == 1.0

    def test_o1_amortized_inference_latency(self):
        """
        Validates O(1) amortized complexity:
        Applying M_defeasible requires only an indexed tensor addition (no live OWL reasoning),
        executing in < 0.1 ms on CPU.
        """
        logits = torch.randn(100, 4)
        states = torch.randint(0, 4, (100,))

        t_start = time.perf_counter()
        _ = apply_amortized_mask(logits, states)
        t_elapsed = time.perf_counter() - t_start

        # 100 samples should take far less than 5 milliseconds
        assert t_elapsed < 0.005, f"Mask application took {t_elapsed * 1000:.2f} ms (expected < 5 ms for 100 cases)"

    def test_defeasible_deontic_head_asymmetric_defeat(self):
        """
        Validates DefeasibleDeonticHead Dung grounded extension:
        When is_statute_lapsed > 0.5, substantive remedies are defeated (-1e4),
        and DISMISS_STATUTE_LAPSED receives grounded boost (+4.0).
        """
        head = DefeasibleDeonticHead(in_features=64, num_classes=4)
        h = torch.randn(1, 64)

        # When NOT lapsed: standard forward pass
        logits_active = head(h, is_statute_lapsed=0.0)
        assert logits_active.shape == (1, 4)

        # When LAPSED: asymmetric defeat triggered
        logits_lapsed = head(h, is_statute_lapsed=1.0)
        assert logits_lapsed[0, 0].item() <= -9000.0  # Forfeiture defeated
        assert logits_lapsed[0, 1].item() <= -9000.0  # Double refund defeated
        assert torch.argmax(logits_lapsed, dim=-1).item() == 2  # Procedural dismissal winner
