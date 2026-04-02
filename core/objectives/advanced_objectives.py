"""
Advanced mission objective implementations.
"""

from typing import Any, Dict

from core.level_runner import LevelRunner

from .base import Objective


class TagExistsObjective(Objective):
    """Verify if a specific git tag exists."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        tag = objective_data.get("tag", "")
        try:
            runner.run_git(["show-ref", "--tags", tag])
            return {"success": True, "message": f"Tag '{tag}' found!"}
        except Exception:
            return {"success": False, "message": f"Tag '{tag}' not found."}


class DetachedHeadObjective(Objective):
    """Verify if the repository is in a detached HEAD state."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            branch = runner.run_git(["branch", "--show-current"])
            if not branch:
                return {"success": True, "message": "HEAD is successfully detached!"}
            return {"success": False, "message": f"HEAD is still on branch '{branch}'."}
        except Exception:
            return {"success": False, "message": "Could not determine HEAD state."}


class CurrentBranchObjective(Objective):
    """Verify if the current branch matches the target."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        expected = objective_data.get("branch", "")
        actual = runner.get_current_branch()
        if actual == expected:
            return {"success": True, "message": f"Currently on branch '{expected}'."}
        return {"success": False, "message": f"Currently on '{actual}', expected '{expected}'."}
