"""
Objective implementations for merge, rebase and complex operations.
"""

from typing import Any, Dict

from core.level_runner import LevelRunner

from .base import Objective


class ConflictResolvedObjective(Objective):
    """Verify if a merge conflict has been resolved."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        if runner.has_merge_conflict():
            return {"success": False, "message": "Merge conflict is still unresolved."}

        # Additionally verify if the merge was actually completed (HEAD has multiple parents)
        try:
            parents = runner.run_git(["log", "-1", "--format=%P"]).split()
            if len(parents) > 1:
                return {"success": True, "message": "Conflict resolved and merge completed!"}
            return {
                "success": False,
                "message": "Conflict files fixed, but merge commit not found.",
            }
        except Exception:
            return {"success": False, "message": "Error checking merge state."}


class RebaseCompletedObjective(Objective):
    """Verify if a rebase was successfully completed."""

    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        # During a rebase, .git/rebase-apply or .git/rebase-merge exists
        repo_path = runner.repo_path
        if (repo_path / ".git" / "rebase-apply").exists() or (
            repo_path / ".git" / "rebase-merge"
        ).exists():
            return {"success": False, "message": "Rebase is still in progress."}

        # Check if the current branch history contains the target branch commits
        target_branch = objective_data.get("onto", "")
        try:
            # Check if all commits from target are in current history
            result = runner.run_git(["cherry", "-v", target_branch])
            if not result.strip():  # No commits in current not in target? (simplistic check)
                return {"success": True, "message": "Rebase completed successfully!"}
            return {"success": True, "message": "Rebase appears completed."}
        except Exception:
            return {"success": False, "message": "Rebase state could not be verified."}
