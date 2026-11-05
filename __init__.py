"""
SynapseLex: An Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication
=============================================================================================================

Authors: Nguyen Tien Dat (ntd25022006q@gmail.com)
Affiliation: International School, Vietnam National University, Hanoi (VNU-IS), Hanoi, Vietnam
License: MIT
"""

import sys
from pathlib import Path

__version__ = "0.1.0"
__author__ = "Nguyen Tien Dat"
__email__ = "ntd25022006q@gmail.com"
__affiliation__ = "International School, Vietnam National University, Hanoi (VNU-IS), Hanoi, Vietnam"
__description__ = "SynapseLex: An Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication"

# Ensure base paths are in sys.path
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

# Import core models and components
from synapselex.src import models
from synapselex.src import data
from synapselex.src import extraction

from synapselex.src.models import (
    HarmonicTimeEmbedding,
    DualClockHarmonicEmbedding,
    DefeasibleDeonticHead,
    LegalMarkovGating,
    SynapseLexTGAT,
    AxiomTGAT,
    HarmonicFourierEncoder,
    OCTSTGModel,
    LukasiewiczLoss,
    ContractStateAutomaton,
    LegalState,
    M_DEFEASIBLE,
    apply_amortized_mask,
    compute_defeasible_remedy_probabilities,
    lukasiewicz_t_norm,
    lukasiewicz_implication,
    smooth_prescription_surrogate,
    smooth_curing_surrogate,
    compute_analytical_prescription_gradient,
)

from synapselex.src.data import LegalGraphBuilder
from synapselex.src.extraction import ChronoChunker, HLEExtractor, SelfVerifier

# Register module aliases in sys.modules for clean imports
sys.modules["synapselex.models"] = models
sys.modules["synapselex.models.tgat_core"] = sys.modules.get("synapselex.src.models.tgat_core", models.tgat_core)
sys.modules["synapselex.models.losses"] = sys.modules.get("synapselex.src.models.losses", models.losses)
sys.modules["synapselex.models.automaton"] = sys.modules.get("synapselex.src.models.automaton", models.automaton)
sys.modules["synapselex.models.mask"] = sys.modules.get("synapselex.src.models.mask", models.mask)
sys.modules["synapselex.data"] = data
sys.modules["synapselex.data.graph_builder"] = sys.modules.get("synapselex.src.data.graph_builder", data.graph_builder)
sys.modules["synapselex.extraction"] = extraction

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__affiliation__",
    "__description__",
    "HarmonicTimeEmbedding",
    "DualClockHarmonicEmbedding",
    "DefeasibleDeonticHead",
    "LegalMarkovGating",
    "SynapseLexTGAT",
    "AxiomTGAT",
    "HarmonicFourierEncoder",
    "OCTSTGModel",
    "LukasiewiczLoss",
    "ContractStateAutomaton",
    "LegalState",
    "M_DEFEASIBLE",
    "apply_amortized_mask",
    "compute_defeasible_remedy_probabilities",
    "lukasiewicz_t_norm",
    "lukasiewicz_implication",
    "smooth_prescription_surrogate",
    "smooth_curing_surrogate",
    "compute_analytical_prescription_gradient",
    "LegalGraphBuilder",
    "ChronoChunker",
    "HLEExtractor",
    "SelfVerifier",
    "models",
    "data",
    "extraction",
]
