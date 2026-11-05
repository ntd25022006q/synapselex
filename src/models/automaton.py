"""
SynapseLex: 4-State Markovian Legal State-Transition Automaton
=============================================================
Formally models non-monotonic civil contract phase transitions under the
Vietnamese Civil Code 2015 (BLDS 2015).

Operational States:
- s_0: Valid (0)
- s_1: Voidable (1)
- s_2: Void_Ab_Initio (2)
- s_3: Extinguished (3)

Transition Rules:
- delta(s_0, e_defect) = s_1                        (Art. 502: Formal Defect, e.g. unnotarized land transfer)
- delta(s_1, e_cure(Perf >= 2/3)) = s_0             (Art. 129(2): Substantial Performance Curing ex lege)
- delta(s_1, e_nullity) = s_2                       (Art. 132: Judicial Declaration of Relative Nullity)
- delta(s_0, e_unlawful) = s_2                      (Art. 123: Absolute Nullity Ab Initio)
- delta(s, e_lapse(Delta tau > 1095)) = s_3, forall s (Art. 429: Procedural Prescription Extinction)

Authors: Nguyen Tien Dat (VNU-IS) & SynapseLex Research Team
Standard: NeurIPS / AAAI / Q1 AI and Law Rigor
"""

from enum import IntEnum
from typing import List, Tuple, Dict, Any, Optional
from datetime import date, datetime


class LegalState(IntEnum):
    VALID = 0
    VOIDABLE = 1
    VOID_AB_INITIO = 2
    EXTINGUISHED = 3

    @property
    def label(self) -> str:
        names = {
            LegalState.VALID: "Valid",
            LegalState.VOIDABLE: "Voidable",
            LegalState.VOID_AB_INITIO: "Void_Ab_Initio",
            LegalState.EXTINGUISHED: "Extinguished"
        }
        return names[self]


class ContractStateAutomaton:
    """
    Deterministic 4-State Legal Mutation Automaton M_S = <S, Sigma, delta, s_0>.
    Tracks non-monotonic phase transitions across procedural and physical time.
    """
    def __init__(self, initial_state: LegalState = LegalState.VALID):
        self.current_state = initial_state
        self.history: List[Tuple[str, LegalState, str]] = [("init", self.current_state, "Contract formed")]

    def reset(self, initial_state: LegalState = LegalState.VALID):
        self.current_state = initial_state
        self.history = [("init", self.current_state, "Contract formed")]

    def transition(self, event_name: str, **kwargs) -> LegalState:
        """
        Applies transition function delta(s, event).
        """
        prev = self.current_state
        explanation = ""

        # Article 429: Procedural Prescription Extinction (takes precedence over all prior states)
        if event_name == "statute_lapse" or kwargs.get("delta_tau", 0) > 1095.0:
            delta_tau = kwargs.get("delta_tau", 0)
            self.current_state = LegalState.EXTINGUISHED
            explanation = f"Article 429 BLDS 2015: procedural limitation period lapsed ({delta_tau:.1f}d > 1095d)"
            self.history.append((event_name, self.current_state, explanation))
            return self.current_state

        if self.current_state == LegalState.VALID:
            if event_name == "formal_defect":
                # Article 502 / Article 117: formal non-compliance renders contract voidable
                self.current_state = LegalState.VOIDABLE
                explanation = "Article 502: formal defect (unnotarized agreement for real property)"
            elif event_name == "unlawful_prohibition":
                # Article 123: Violation of law or social morality -> Void Ab Initio
                self.current_state = LegalState.VOID_AB_INITIO
                explanation = "Article 123: absolute nullity ab initio (prohibited object/illegal)"

        elif self.current_state == LegalState.VOIDABLE:
            if event_name == "cure_performance":
                performance_ratio = kwargs.get("performance_ratio", 0.0)
                if performance_ratio >= 2.0 / 3.0:
                    # Article 129(2): Substantial performance curing
                    self.current_state = LegalState.VALID
                    explanation = f"Article 129(2): cured ex lege by substantial performance ({performance_ratio:.1%} >= 66.7%)"
                else:
                    explanation = f"Article 129(2): curing rejected (performance {performance_ratio:.1%} < 66.7%)"
            elif event_name == "declare_nullity":
                # Article 132: Declaration of relative nullity by court
                self.current_state = LegalState.VOID_AB_INITIO
                explanation = "Article 132: court declares relative nullity"

        self.history.append((event_name, self.current_state, explanation))
        return self.current_state

    def simulate_case_lifecycle(
        self,
        has_formal_defect: bool = False,
        performance_ratio: float = 0.0,
        is_unlawful: bool = False,
        elapsed_days: float = 0.0,
        tolling_days: float = 0.0,
        has_restart_ack: bool = False,
        restart_elapsed_days: float = 0.0
    ) -> LegalState:
        """
        Simulates end-to-end legal mutation from contract formation through dispute.
        """
        self.reset(LegalState.VALID)

        # 1. Formation defects
        if is_unlawful:
            self.transition("unlawful_prohibition")
            return self.current_state
        elif has_formal_defect:
            self.transition("formal_defect")
            # Check curing under Article 129(2)
            if performance_ratio >= 2.0 / 3.0:
                self.transition("cure_performance", performance_ratio=performance_ratio)

        # 2. Jurisprudential procedural latency calculation (Article 156 tolling & Article 157 restart)
        if has_restart_ack:
            # Latency collapses to restart point
            effective_delta_tau = restart_elapsed_days - tolling_days
        else:
            effective_delta_tau = elapsed_days - tolling_days

        effective_delta_tau = max(0.0, effective_delta_tau)

        # 3. Procedural prescription audit (Article 429)
        if effective_delta_tau > 1095.0:
            self.transition("statute_lapse", delta_tau=effective_delta_tau)

        return self.current_state

    def get_trace(self) -> List[Dict[str, Any]]:
        return [
            {"step": i, "event": h[0], "state": h[1].label, "state_id": int(h[1]), "explanation": h[2]}
            for i, h in enumerate(self.history)
        ]
