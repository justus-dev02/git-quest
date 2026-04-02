"""
Objective implementation: Repository state checks.
"""

from typing import Any, Dict

from core.level_runner import LevelRunner

from .base import Objective


class CleanStateObjective(Objective):
    """Checks if the repository state is clean (no uncommitted changes)."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        if not runner.has_uncommitted_changes():
            return {"success": True, "message": "The repository is in a clean state!"}
        return {"success": False, "message": "There are still uncommitted changes."}


class BranchExistsObjective(Objective):
    """Checks if a specific branch exists."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        branch_name = objective_data.get("branch", "")
        if runner.branch_exists(branch_name):
            return {"success": True, "message": f"Branch '{branch_name}' found!"}
        return {"success": False, "message": f"Branch '{branch_name}' not found."}
