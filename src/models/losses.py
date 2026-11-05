"""
SynapseLex: Smooth Lukasiewicz Fuzzy Description Logic Loss Relaxation
========================================================================
Implements the continuous Lukasiewicz t-norm loss relaxation and exact analytical
gradients as formulated in Section 4.6 of the SynapseLex paper.

Key Mathematical Formulations:
1. Lukasiewicz t-norm: T_L(x, y) = max(0, x + y - 1)
2. Residuated implication: I_L(x, y) = min(1, 1 - x + y)
3. Residual violation penalty: psi_1^L(theta) = max(0, u(Delta tau) - P(Extinguished))
4. Temperature-annealed continuous membership surrogate:
   u(Delta tau) = sigma_{tau_0}(Delta tau) = 1 / (1 + exp(-(Delta tau - 1095) / tau_0))
5. Substantial performance curing surrogate:
   sigma_{rho_0}(Perf) = 1 / (1 + exp(-(Perf - 2/3) / rho_0))
6. Analytical gradients with respect to Delta tau eliminating the "Gradient Void".

Authors: Nguyen Tien Dat (VNU-IS) & SynapseLex Research Team
Standard: NeurIPS / AAAI / Q1 AI and Law Rigor
"""

import math
from typing import Dict, Any, Optional, Tuple, Union
import torch
import torch.nn as nn
import torch.nn.functional as F

# Operational Legal Constants under Vietnamese Civil Code (BLDS 2015)
ARTICLE_429_PRESCRIPTION_DAYS = 1095.0  # 3 calendar years limitation period
ARTICLE_129_CURING_THRESHOLD = 2.0 / 3.0  # >= 2/3 contractual performance cures formal defect


def lukasiewicz_t_norm(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Lukasiewicz continuous t-norm (fuzzy conjunction):
    T_L(x, y) = max(0, x + y - 1)
    """
    return torch.clamp(x + y - 1.0, min=0.0)


def lukasiewicz_implication(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Lukasiewicz residuated implication operator:
    I_L(x, y) = min(1, 1 - x + y)
    """
    return torch.clamp(1.0 - x + y, max=1.0)


def smooth_prescription_surrogate(
    delta_tau: torch.Tensor,
    tau_0: float = 30.0,
    threshold: float = ARTICLE_429_PRESCRIPTION_DAYS
) -> torch.Tensor:
    """
    Continuous temperature-annealed Fermi-Dirac / logistic sigmoid surrogate:
    sigma_{tau_0}(Delta tau) = 1 / (1 + exp(-(Delta tau - threshold) / tau_0))
    
    Eliminates the step-function gradient void.
    """
    return torch.sigmoid((delta_tau - threshold) / tau_0)


def smooth_curing_surrogate(
    performance_ratio: torch.Tensor,
    rho_0: float = 0.05,
    threshold: float = ARTICLE_129_CURING_THRESHOLD
) -> torch.Tensor:
    """
    Continuous surrogate for Article 129(2) substantial performance curing:
    sigma_{rho_0}(Perf) = 1 / (1 + exp(-(Perf - 2/3) / rho_0))
    """
    return torch.sigmoid((performance_ratio - threshold) / rho_0)


def compute_analytical_prescription_gradient(
    delta_tau: float,
    prob_extinguished: float,
    tau_0: float = 30.0,
    threshold: float = ARTICLE_429_PRESCRIPTION_DAYS
) -> float:
    """
    Exact analytical gradient d(psi_1^smooth) / d(Delta tau) as derived in Eq. (401):
    (1 / tau_0) * sigma(Delta tau) * (1 - sigma(Delta tau)) * (1 - P(Extinguished))
    
    Strictly positive and non-vanishing for finite Delta tau when P(Extinguished) < 1.
    """
    sigma = 1.0 / (1.0 + math.exp(-(delta_tau - threshold) / tau_0))
    d_sigma = (1.0 / tau_0) * sigma * (1.0 - sigma)
    return d_sigma * (1.0 - prob_extinguished)


class LukasiewiczLoss(nn.Module):
    """
    Continuous Lukasiewicz Fuzzy Description Logic Loss Regularizer.
    
    Computes three smooth axiomatic penalty terms:
    - psi_1^smooth: Article 429 prescription bar enforcement (penalty if not extinguished when Delta tau > 1095)
    - psi_2^smooth: Article 129(2) curing defect enforcement (penalty if void ab initio despite Perf >= 2/3)
    - psi_3^smooth: Article 328 mutual exclusivity (penalty for simultaneous forfeiture & double refund)
    """
    def __init__(
        self,
        tau_0: float = 30.0,
        rho_0: float = 0.05,
        lambda_onto: float = 1.5,
        prescription_threshold: float = ARTICLE_429_PRESCRIPTION_DAYS,
        curing_threshold: float = ARTICLE_129_CURING_THRESHOLD
    ):
        super().__init__()
        self.tau_0 = tau_0
        self.rho_0 = rho_0
        self.lambda_onto = lambda_onto
        self.prescription_threshold = prescription_threshold
        self.curing_threshold = curing_threshold

    def forward(
        self,
        verdict_logits: torch.Tensor,
        state_logits: torch.Tensor,
        delta_tau: torch.Tensor,
        has_formal_defect: Optional[torch.Tensor] = None,
        performance_ratio: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        verdict_logits: [batch_size, 4] (0: Forfeiture, 1: DoubleRefund, 2: DismissStatuteLapsed, 3: DeclareVoid)
        state_logits:   [batch_size, 4] (0: Valid, 1: Voidable, 2: Void_Ab_Initio, 3: Extinguished)
        delta_tau:      [batch_size] or [batch_size, 1] continuous procedural latency in days
        has_formal_defect: optional binary tensor [batch_size]
        performance_ratio: optional float tensor [batch_size] in [0, 1]
        """
        if delta_tau.dim() > 1:
            delta_tau = delta_tau.squeeze(-1)
            
        batch_size = verdict_logits.size(0)
        device = verdict_logits.device
        
        probs_v = F.softmax(verdict_logits, dim=-1)
        probs_s = F.softmax(state_logits, dim=-1)
        
        # 1. Smooth Prescription Surrogate u(Delta tau) = sigma_{tau_0}(Delta tau)
        u_tau = smooth_prescription_surrogate(delta_tau, self.tau_0, self.prescription_threshold)
        p_extinguished = probs_s[:, 3]
        
        # psi_1: Article 429 residual violation penalty under Lukasiewicz implication:
        # psi_1 = 1 - I_L(u(tau), P(Extinguished)) = max(0, u(tau) - P(Extinguished))
        # Smooth formulation: sigma_{tau_0}(Delta tau) * (1 - P(Extinguished))
        psi_1 = u_tau * (1.0 - p_extinguished)
        
        # In addition, penalize non-dismissal if statute lapsed
        p_dismiss = probs_v[:, 2]
        psi_1_verdict = u_tau * (1.0 - p_dismiss)
        psi_1_total = 0.5 * (psi_1 + psi_1_verdict)
        
        # 2. Article 129(2) Curing Penalty psi_2
        if has_formal_defect is not None and performance_ratio is not None:
            if has_formal_defect.dim() > 1:
                has_formal_defect = has_formal_defect.squeeze(-1)
            if performance_ratio.dim() > 1:
                performance_ratio = performance_ratio.squeeze(-1)
            u_perf = smooth_curing_surrogate(performance_ratio, self.rho_0, self.curing_threshold)
            p_void_ab_initio = probs_s[:, 2]
            # If defect is cured (u_perf high), contract MUST NOT be Void_Ab_Initio
            psi_2 = has_formal_defect.float() * u_perf * p_void_ab_initio
        else:
            psi_2 = torch.zeros(batch_size, device=device)
            
        # 3. Article 328 Mutual Exclusivity Penalty psi_3
        # Cannot decree both Forfeiture (index 0) and Double Refund (index 1)
        p_forfeit = probs_v[:, 0]
        p_double = probs_v[:, 1]
        psi_3 = 2.0 * (p_forfeit * p_double)
        
        # Aggregate penalties
        l_psi1 = torch.mean(psi_1_total)
        l_psi2 = torch.mean(psi_2)
        l_psi3 = torch.mean(psi_3)
        l_onto = l_psi1 + l_psi2 + l_psi3
        total_regularized_loss = self.lambda_onto * l_onto
        
        return {
            "loss_onto": total_regularized_loss,
            "psi_1_prescription": l_psi1,
            "psi_2_curing": l_psi2,
            "psi_3_mutual_exclusivity": l_psi3,
            "u_tau": u_tau
        }
