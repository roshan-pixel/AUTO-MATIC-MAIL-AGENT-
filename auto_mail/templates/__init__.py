"""Templates for legal notices, consumer grievances, and developer claims."""

from .legal_grievance import generate_dual_jurisdiction_grievance
from .student_pack_claim import generate_student_pack_claim

__all__ = [
    "generate_dual_jurisdiction_grievance",
    "generate_student_pack_claim",
]
