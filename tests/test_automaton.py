"""
Unit Tests for 4-State Markovian Legal State-Transition Automaton
================================================================
Validates:
- 4 legal operational states: Valid, Voidable, Void_Ab_Initio, Extinguished
- Article 502 formal defect transition (Valid -> Voidable)
- Article 129(2) BLDS 2015 substantial performance curing ex lege (Voidable -> Valid when Perf >= 2/3)
- Non-curing when performance < 2/3 (remains Voidable)
- Article 429 BLDS 2015 procedural prescription extinction (Any state -> Extinguished when Delta tau > 1,095)
- Article 156 force majeure tolling and Article 157 acknowledgment restart interactions
- End-to-end non-monotonic dispute lifecycle simulation
"""

import pytest

from synapselex.src.models.automaton import (
    ContractStateAutomaton,
    LegalState,
)


class TestLegalAutomaton:

    def test_initial_state(self):
        """A newly initialized contract begins in the Valid state (s_0)."""
        automaton = ContractStateAutomaton()
        assert automaton.current_state == LegalState.VALID
        assert automaton.current_state.label == "Valid"
        assert int(automaton.current_state) == 0

    def test_formal_defect_transition(self):
        """Article 502: Lack of mandatory notarization mutates state Valid -> Voidable (s_1)."""
        automaton = ContractStateAutomaton()
        new_state = automaton.transition("formal_defect")
        assert new_state == LegalState.VOIDABLE
        assert automaton.current_state == LegalState.VOIDABLE

    def test_substantial_performance_curing_article_129_clause_2(self):
        """
        Article 129(2) BLDS 2015:
        When a voidable contract with formal defect achieves judicial acceptance of
        at least 2/3 (>= 66.7%) of obligations, it is cured ex lege to Valid (s_0).
        """
        automaton = ContractStateAutomaton()
        automaton.transition("formal_defect")
        assert automaton.current_state == LegalState.VOIDABLE

        # Test successful curing: Perf = 75% >= 66.7%
        cured_state = automaton.transition("cure_performance", performance_ratio=0.75)
        assert cured_state == LegalState.VALID
        assert automaton.current_state == LegalState.VALID

    def test_performance_under_threshold_fails_curing(self):
        """
        When performance is strictly less than 2/3 (< 66.7%), the formal defect is
        NOT cured and the contract remains Voidable (s_1).
        """
        automaton = ContractStateAutomaton()
        automaton.transition("formal_defect")
        assert automaton.current_state == LegalState.VOIDABLE

        # Test rejected curing: Perf = 50% < 66.7%
        state = automaton.transition("cure_performance", performance_ratio=0.50)
        assert state == LegalState.VOIDABLE
        assert automaton.current_state == LegalState.VOIDABLE

        # Edge test: Perf = 66.0% < 66.6667%
        state = automaton.transition("cure_performance", performance_ratio=0.66)
        assert state == LegalState.VOIDABLE

        # Exactly 2/3 (66.6667%) cures
        state = automaton.transition("cure_performance", performance_ratio=2.0 / 3.0)
        assert state == LegalState.VALID

    def test_procedural_prescription_extinction_article_429(self):
        """
        Article 429 BLDS 2015:
        When procedural latency Delta tau > 1,095 days without tolling or restart,
        the cause of action is extinguished ex lege, mutating state to Extinguished (s_3).
        """
        # Case A: From Valid state
        aut_valid = ContractStateAutomaton()
        res_valid = aut_valid.transition("statute_lapse", delta_tau=1200.0)
        assert res_valid == LegalState.EXTINGUISHED

        # Case B: From Voidable state
        aut_voidable = ContractStateAutomaton()
        aut_voidable.transition("formal_defect")
        res_voidable = aut_voidable.transition("statute_lapse", delta_tau=1100.0)
        assert res_voidable == LegalState.EXTINGUISHED

        # Case C: From Void_Ab_Initio state
        aut_void = ContractStateAutomaton()
        aut_void.transition("unlawful_prohibition")
        res_void = aut_void.transition("statute_lapse", delta_tau=1500.0)
        assert res_void == LegalState.EXTINGUISHED

    def test_dual_clock_tolling_preserves_validity(self):
        """
        Article 156: Force majeure tolling freezes procedural time.
        Physical elapsed days = 1,200 (> 1,095), but administrative freeze = 180 days.
        Procedural latency = 1,200 - 180 = 1,020 days (<= 1,095), preserving claim validity!
        """
        automaton = ContractStateAutomaton()
        final_state = automaton.simulate_case_lifecycle(
            has_formal_defect=False,
            elapsed_days=1200.0,
            tolling_days=180.0,  # e.g., COVID-19 administrative freeze
            has_restart_ack=False
        )
        assert final_state == LegalState.VALID
        assert final_state != LegalState.EXTINGUISHED

    def test_dual_clock_restart_preserves_validity(self):
        """
        Article 157: Indebtedness acknowledgment collapses procedural clock to zero.
        Physical days = 1,500, but acknowledgment occurred 300 days prior to filing.
        Procedural latency = 300 days (<= 1,095), preserving claim validity!
        """
        automaton = ContractStateAutomaton()
        final_state = automaton.simulate_case_lifecycle(
            has_formal_defect=False,
            elapsed_days=1500.0,
            has_restart_ack=True,
            restart_elapsed_days=300.0
        )
        assert final_state == LegalState.VALID
        assert final_state != LegalState.EXTINGUISHED

    def test_full_non_monotonic_lifecycle(self):
        """
        Simulates the canonical non-monotonic civil lifecycle:
        1. Formation (Valid s_0)
        2. Unnotarized defect (Voidable s_1)
        3. 80% Payment Curing under Art. 129(2) (recovers to Valid s_0)
        4. Statutory lapse after 1,250 days without suit (Extinguished s_3)
        """
        automaton = ContractStateAutomaton()
        final_state = automaton.simulate_case_lifecycle(
            has_formal_defect=True,
            performance_ratio=0.80,  # Cures defect
            elapsed_days=1250.0      # Lapses statute
        )
        assert final_state == LegalState.EXTINGUISHED
        
        trace = automaton.get_trace()
        states_visited = [t["state"] for t in trace]
        assert states_visited == ["Valid", "Voidable", "Valid", "Extinguished"]
