"""
Objective Factory for creating specific objective strategies.
"""

from typing import Dict, Optional, Type

from .advanced_objectives import CurrentBranchObjective, DetachedHeadObjective, TagExistsObjective
from .base import Objective
from .commit_objectives import CommitCountObjective, CommitExistsObjective
from .merge_objectives import ConflictResolvedObjective, RebaseCompletedObjective
from .state_objectives import BranchExistsObjective, CleanStateObjective


class ObjectiveFactory:
    """Factory to map objective types to Strategy implementations."""

    _OBJECTIVES: Dict[str, Type[Objective]] = {
        "commit_exists": CommitExistsObjective,
        "commit_count": CommitCountObjective,
        "clean_state": CleanStateObjective,
        "branch_exists": BranchExistsObjective,
        "tag_exists": TagExistsObjective,
        "detached_head": DetachedHeadObjective,
        "current_branch": CurrentBranchObjective,
        "conflict_resolved": ConflictResolvedObjective,
        "rebase_completed": RebaseCompletedObjective,
        "merge_completed": ConflictResolvedObjective,  # Reuse for simple merge check
    }

    @classmethod
    def get_objective(cls, objective_type: str) -> Optional[Objective]:
        """
        Get an objective strategy by its type string.
        """
        objective_class = cls._OBJECTIVES.get(objective_type)
        if objective_class:
            return objective_class()
        return None

    @classmethod
    def register_objective(cls, objective_type: str, objective_class: Type[Objective]) -> None:
        """Register a new objective implementation."""
        cls._OBJECTIVES[objective_type] = objective_class
