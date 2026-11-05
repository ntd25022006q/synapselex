"""
SynapseLex Neural and Neuro-Symbolic Model Modules
==================================================
Includes:
- HarmonicTimeEmbedding: Bochner continuous Fourier time encoding
- DualClockHarmonicEmbedding: Coupled physical & procedural dual-clock time
- DefeasibleDeonticHead: Dung grounded extension argumentation head
- LegalMarkovGating: Contract state gating
- SynapseLexTGAT: Full Axiom-TGAT framework
- OCTSTGModel: Baseline OC-TSTG model
- LukasiewiczLoss: Smooth fuzzy logic axiomatic loss relaxation
- ContractStateAutomaton, LegalState: 4-state Markovian legal mutation automaton
- M_DEFEASIBLE, apply_amortized_mask: Amortized TBox projection mask
"""

from synapselex.src.models.tgat_core import (
    HarmonicTimeEmbedding,
    DualClockHarmonicEmbedding,
    DefeasibleDeonticHead,
    LegalMarkovGating,
    TemporalGraphAttentionLayer,
    NormativeHierarchyArbiter,
    SynapseLexTGAT,
    HarmonicFourierEncoder,
    AxiomTGAT,
    NUM_NODE_TYPES,
    NUM_REL_TYPES,
    NUM_LEGAL_STATES,
    NUM_VERDICT_CLASSES,
)
from synapselex.src.models.oc_tstg import (
    Time2Vec,
    DualSpaceContinualEmbedding,
    OCTSTGModel,
    VERDICT_MAP,
)
from synapselex.src.models.losses import (
    LukasiewiczLoss,
    lukasiewicz_t_norm,
    lukasiewicz_implication,
    smooth_prescription_surrogate,
    smooth_curing_surrogate,
    compute_analytical_prescription_gradient,
    ARTICLE_429_PRESCRIPTION_DAYS,
    ARTICLE_129_CURING_THRESHOLD,
)
from synapselex.src.models.automaton import (
    ContractStateAutomaton,
    LegalState,
)
from synapselex.src.models.mask import (
    M_DEFEASIBLE,
    NEG_INF,
    get_defeasible_projection_vector,
    apply_amortized_mask,
    compute_defeasible_remedy_probabilities,
)

__all__ = [
    "HarmonicTimeEmbedding",
    "DualClockHarmonicEmbedding",
    "DefeasibleDeonticHead",
    "LegalMarkovGating",
    "TemporalGraphAttentionLayer",
    "NormativeHierarchyArbiter",
    "SynapseLexTGAT",
    "HarmonicFourierEncoder",
    "AxiomTGAT",
    "Time2Vec",
    "DualSpaceContinualEmbedding",
    "OCTSTGModel",
    "VERDICT_MAP",
    "LukasiewiczLoss",
    "lukasiewicz_t_norm",
    "lukasiewicz_implication",
    "smooth_prescription_surrogate",
    "smooth_curing_surrogate",
    "compute_analytical_prescription_gradient",
    "ARTICLE_429_PRESCRIPTION_DAYS",
    "ARTICLE_129_CURING_THRESHOLD",
    "ContractStateAutomaton",
    "LegalState",
    "M_DEFEASIBLE",
    "NEG_INF",
    "get_defeasible_projection_vector",
    "apply_amortized_mask",
    "compute_defeasible_remedy_probabilities",
]
