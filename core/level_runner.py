"""
Git Quest - Level Runner
Provides a simplified interface for executing Git commands within a level's repository.
Refactored to use GitExecutor for consistency.
"""

import subprocess
from pathlib import Path
from typing import List

from core.exceptions import GitCommandError
from core.logger import setup_logger

logger = setup_logger(__name__)


class LevelRunner:
    """Helper class for checking git state in a level repository."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    def run_git(self, args: List[str]) -> str:
        """Run a git command and return stdout."""
        try:
            result = subprocess.run(
                ["git"] + args, cwd=self.repo_path, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e.stderr}")
            raise GitCommandError(f"Git command failed: {e.stderr}", stderr=e.stderr)

    def commit_exists(self, message: str) -> bool:
        """Check if a commit with specific message exists."""
        try:
            # Check all branches for the commit message
            result = self.run_git(["log", "--all", "--grep", message, "--format=%s"])
            return message.lower() in result.lower()
        except GitCommandError:
            return False

    def get_commit_count(self) -> int:
        """Get the total number of commits in the repository."""
        try:
            result = self.run_git(["rev-list", "--count", "--all"])
            return int(result)
        except (GitCommandError, ValueError):
            return 0

    def branch_exists(self, branch_name: str) -> bool:
        """Check if a specific branch exists."""
        try:
            self.run_git(["show-ref", "--verify", f"refs/heads/{branch_name}"])
            return True
        except GitCommandError:
            return False

    def has_uncommitted_changes(self) -> bool:
        """Check if there are any uncommitted changes (staged or unstaged)."""
        try:
            # git status --porcelain is empty if the repo is clean
            result = self.run_git(["status", "--porcelain"])
            return bool(result.strip())
        except GitCommandError:
            return False

    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        try:
            return self.run_git(["branch", "--show-current"])
        except GitCommandError:
            return ""

    def has_merge_conflict(self) -> bool:
        """Check if the repository has an ongoing merge conflict."""
        try:
            # git ls-files -u lists unmerged files
            result = self.run_git(["ls-files", "-u"])
            return bool(result.strip())
        except GitCommandError:
            return False
