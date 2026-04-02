"""
Objective implementation: Check if a specific commit exists.
"""

from typing import Any, Dict

from core.level_runner import LevelRunner

from .base import Objective


class CommitExistsObjective(Objective):
    """Checks if a commit with a specific message exists."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        message = objective_data.get("message", "")
        if runner.commit_exists(message):
            return {"success": True, "message": f"Commit with '{message}' found!"}
        return {"success": False, "message": f"Commit with '{message}' not found"}


class CommitCountObjective(Objective):
    """Checks if the repository has a minimum number of commits."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        expected_count = objective_data.get("count", 0)
        actual_count = runner.get_commit_count()
        if actual_count >= expected_count:
            return {"success": True, "message": f"Found {actual_count} commits!"}
        return {
            "success": False,
            "message": f"Expected {expected_count} commits, found {actual_count}",
        }
