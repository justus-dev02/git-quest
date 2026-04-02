"""
Git Quest - Level Setup Service
Handles creating the initial repository state for a level.
"""

from pathlib import Path
from typing import Any, Dict

from core.logger import setup_logger
from git_engine.git_executor import GitExecutor

logger = setup_logger(__name__)


class LevelSetupService:
    """Service for preparing the repository state for a level."""

    def __init__(self, git_executor: GitExecutor):
        self.git_executor = git_executor

    def setup_level(self, repo_path: Path, level_data: Dict[str, Any]) -> bool:
        """
        Setup the repository based on level data.

        Args:
            repo_path: Path to the level repository.
            level_data: The level configuration JSON.

        Returns:
            True if setup was successful.
        """
        try:
            # Always ensure at least one commit so git bundle works
            if not self._has_commits(repo_path):
                readme = repo_path / "README.md"
                if not readme.exists():
                    readme.write_text("# Git Quest\n")
                self.git_executor.run(["add", "README.md"], cwd=repo_path)
                self.git_executor.run(["commit", "-m", "initial setup"], cwd=repo_path)

            # 1. Setup initial files (untracked)
            files = level_data.get("files", {})
            for name, content in files.items():
                file_path = repo_path / name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content)
                logger.debug(f"Created initial file: {name}")

            # 2. Setup initial commits
            initial_commits = level_data.get("initial_commits", [])
            for commit in initial_commits:
                self._apply_commit(repo_path, commit)

            # 3. Setup initial branches
            branches = level_data.get("initial_branches", [])
            for branch in branches:
                self.git_executor.run(["branch", branch], cwd=repo_path)
                logger.debug(f"Created initial branch: {branch}")

            # 4. Handle remote setup if defined
            remote = level_data.get("initial_remote")
            if remote:
                self.git_executor.run(["remote", "add", "origin", remote], cwd=repo_path)

            return True
        except Exception as e:
            logger.error(f"Failed to setup level state: {e}", exc_info=True)
            return False

    def _has_commits(self, repo_path: Path) -> bool:
        """Check if the repository has any commits."""
        try:
            self.git_executor.run(["rev-parse", "HEAD"], cwd=repo_path)
            return True
        except Exception:
            return False

    def _apply_commit(self, repo_path: Path, commit_data: Dict[str, Any]) -> None:
        """Helper to create a specific commit in the repository."""
        files = commit_data.get("files", {})
        for name, content in files.items():
            file_path = repo_path / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            self.git_executor.run(["add", name], cwd=repo_path)

        message = commit_data.get("message", "initial setup")
        self.git_executor.run(["commit", "-m", message], cwd=repo_path)
        logger.debug(f"Created setup commit: {message}")
