"""
Unit Tests for Smooth Lukasiewicz Fuzzy Description Logic Loss Relaxation
==========================================================================
Validates:
- Mathematical properties of the Lukasiewicz t-norm T_L and residuated implication I_L
- Continuous temperature-annealed surrogates (Article 429 prescription & Article 129 curing)
- Elimination of the Gradient Void: analytical vs autograd non-vanishing gradient flow into Delta tau
- Differentiable multi-task loss computation and parameter backpropagation
"""

import math
import pytest
import torch
import torch.nn.functional as F

from synapselex.src.models.losses import (
    lukasiewicz_t_norm,
    lukasiewicz_implication,
    smooth_prescription_surrogate,
    smooth_curing_surrogate,
    compute_analytical_prescription_gradient,
    LukasiewiczLoss,
    ARTICLE_429_PRESCRIPTION_DAYS,
    ARTICLE_129_CURING_THRESHOLD,
)


class TestLukasiewiczLogicAndLoss:

    def test_lukasiewicz_t_norm_axioms(self):
        """Validates T_L(x, y) = max(0, x + y - 1) boundary and algebraic conditions."""
        # Boundaries
        x = torch.tensor([1.0, 1.0, 0.0, 0.5, 0.7])
        y = torch.tensor([1.0, 0.0, 0.0, 0.5, 0.6])
        t_norm = lukasiewicz_t_norm(x, y)
        expected = torch.tensor([1.0, 0.0, 0.0, 0.0, 0.3])
        assert torch.allclose(t_norm, expected, atol=1e-6)

        # Commutativity: T_L(a, b) == T_L(b, a)
        a = torch.tensor([0.8, 0.4, 0.9])
        b = torch.tensor([0.5, 0.7, 0.2])
        assert torch.allclose(lukasiewicz_t_norm(a, b), lukasiewicz_t_norm(b, a))

        # Associativity: T_L(T_L(a, b), c) == T_L(a, T_L(b, c))
        c = torch.tensor([0.6, 0.8, 0.5])
        left = lukasiewicz_t_norm(lukasiewicz_t_norm(a, b), c)
        right = lukasiewicz_t_norm(a, lukasiewicz_t_norm(b, c))
        assert torch.allclose(left, right, atol=1e-6)

    def test_lukasiewicz_residuated_implication(self):
        """Validates I_L(x, y) = min(1, 1 - x + y)."""
        # When antecedent <= consequent, implication is 1.0 (truth preserved)
        assert lukasiewicz_implication(torch.tensor(0.5), torch.tensor(0.8)).item() == 1.0
        assert lukasiewicz_implication(torch.tensor(0.7), torch.tensor(0.7)).item() == 1.0

        # When antecedent > consequent, implication decreases linearly
        assert pytest.approx(lukasiewicz_implication(torch.tensor(1.0), torch.tensor(0.0)).item()) == 0.0
        assert pytest.approx(lukasiewicz_implication(torch.tensor(0.9), torch.tensor(0.4)).item(), abs=1e-5) == 0.5

    def test_smooth_prescription_surrogate(self):
        """Validates temperature-annealed logistic sigmoid surrogate around 1,095 days."""
        threshold = ARTICLE_429_PRESCRIPTION_DAYS
        tau_0 = 30.0

        # At the exact statutory threshold, surrogate must equal 0.5
        t_crit = torch.tensor([threshold], dtype=torch.float32)
        assert pytest.approx(smooth_prescription_surrogate(t_crit, tau_0).item(), abs=1e-5) == 0.5

        # Monotonicity test
        times = torch.tensor([500.0, 1000.0, 1095.0, 1150.0, 2000.0])
        surrogates = smooth_prescription_surrogate(times, tau_0)
        for i in range(len(surrogates) - 1):
            assert surrogates[i] < surrogates[i + 1]

        # Sharpness as tau_0 -> 0 (converges to step indicator)
        t_before = torch.tensor([1094.0])
        t_after = torch.tensor([1096.0])
        u_sharp_before = smooth_prescription_surrogate(t_before, tau_0=0.1).item()
        u_sharp_after = smooth_prescription_surrogate(t_after, tau_0=0.1).item()
        assert u_sharp_before < 1e-4
        assert u_sharp_after > 0.9999

    def test_smooth_curing_surrogate(self):
        """Validates Article 129(2) curing surrogate around 2/3 performance."""
        thresh = ARTICLE_129_CURING_THRESHOLD
        p_crit = torch.tensor([thresh], dtype=torch.float32)
        assert pytest.approx(smooth_curing_surrogate(p_crit).item(), abs=1e-5) == 0.5

        # Lower performance (< 2/3) yields low surrogate
        assert smooth_curing_surrogate(torch.tensor([0.4])).item() < 0.05
        # Substantial performance (>= 2/3) yields high surrogate
        assert smooth_curing_surrogate(torch.tensor([0.85])).item() > 0.95

    def test_gradient_void_elimination_analytical_vs_autograd(self):
        """
        Theorem Test: Eliminating the Gradient Void.
        In discrete formulation, d(indicator)/d(Delta tau) == 0 everywhere (gradient void).
        In smooth Lukasiewicz relaxation, autograd gradient matches exact analytical formula:
        d(psi_1)/d(Delta tau) = (1 / tau_0) * sigma * (1 - sigma) * (1 - P(Extinguished))
        """
        tau_0 = 30.0
        delta_tau = torch.tensor([1120.0], dtype=torch.float64, requires_grad=True)
        prob_extinguished = 0.25  # Model is currently failing to predict extinguished state

        # Smooth loss definition: sigma(Delta tau) * (1 - P(Extinguished))
        u_tau = torch.sigmoid((delta_tau - ARTICLE_429_PRESCRIPTION_DAYS) / tau_0)
        psi_1 = u_tau * (1.0 - prob_extinguished)
        psi_1.backward()

        autograd_grad = delta_tau.grad.item()
        analytical_grad = compute_analytical_prescription_gradient(
            delta_tau=1120.0,
            prob_extinguished=prob_extinguished,
            tau_0=tau_0
        )

        assert autograd_grad > 0.0, "Gradient must be strictly positive (eliminating the Gradient Void)!"
        assert pytest.approx(autograd_grad, rel=1e-4) == analytical_grad, (
            f"Autograd gradient ({autograd_grad}) does not match analytical derivative ({analytical_grad})"
        )

    def test_lukasiewicz_loss_module_forward_and_backward(self):
        """Tests LukasiewiczLoss PyTorch module end-to-end forward pass and backprop."""
        loss_fn = LukasiewiczLoss(tau_0=30.0, lambda_onto=2.0)

        # Batch of 3 cases:
        # Case 0: Normal active contract (tau = 200d)
        # Case 1: Expired contract (tau = 1300d), model correctly predicting Extinguished
        # Case 2: Expired contract (tau = 1400d), model mistakenly predicting Valid
        verdict_logits = torch.randn(3, 4, requires_grad=True)
        state_logits = torch.randn(3, 4, requires_grad=True)
        delta_tau = torch.tensor([200.0, 1300.0, 1400.0], dtype=torch.float32, requires_grad=True)
        has_defect = torch.tensor([0.0, 1.0, 0.0])
        perf_ratio = torch.tensor([0.0, 0.75, 0.0])

        out = loss_fn(
            verdict_logits=verdict_logits,
            state_logits=state_logits,
            delta_tau=delta_tau,
            has_formal_defect=has_defect,
            performance_ratio=perf_ratio
        )

        assert "loss_onto" in out
        assert "psi_1_prescription" in out
        assert "psi_2_curing" in out
        assert "psi_3_mutual_exclusivity" in out

        total_loss = out["loss_onto"]
        assert total_loss.item() >= 0.0
        total_loss.backward()

        assert verdict_logits.grad is not None
        assert state_logits.grad is not None
        assert delta_tau.grad is not None
        assert not torch.all(delta_tau.grad == 0), "Gradients must flow into continuous procedural latency."
