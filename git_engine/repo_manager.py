"""
Git Quest - Repository Manager
Refactored to use GitExecutor and git bundle for robust snapshots.
"""

import shutil
from pathlib import Path

from core.exceptions import GitCommandError, RepoNotFoundError
from core.logger import setup_logger

from .git_executor import GitExecutor

logger = setup_logger(__name__)


class RepoManager:
    """Manages Git repository lifecycles and robust snapshots."""

    def __init__(self, workspace_path: Path, git_executor: GitExecutor):
        """
        Initialize the repository manager.

        Args:
            workspace_path: Root directory for repositories.
            git_executor: The GitExecutor instance for running git commands.
        """
        self.workspace_path = workspace_path
        self.git_executor = git_executor
        self.snapshots_path = workspace_path / ".snapshots"
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Ensure necessary directories exist."""
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self.snapshots_path.mkdir(parents=True, exist_ok=True)

    def init_repo(self, repo_path: Path) -> bool:
        """
        Initialize a new git repository using GitExecutor.
        """
        try:
            repo_path.mkdir(parents=True, exist_ok=True)
            self.git_executor.run(["init", "--initial-branch=main"], cwd=repo_path)
            return True
        except GitCommandError as e:
            logger.error(f"Failed to initialize repository: {e}")
            return False

    def create_snapshot(self, repo_path: Path, snapshot_name: str) -> bool:
        """
        Create a robust snapshot using 'git bundle'.

        This is more efficient and reliable than raw file copies,
        especially for repositories with many files or locks.
        """
        if not repo_path.exists():
            raise RepoNotFoundError(f"Repository not found at {repo_path}")

        bundle_file = self.snapshots_path / f"{snapshot_name}.bundle"

        try:
            # Create a bundle of all refs
            self.git_executor.run(["bundle", "create", str(bundle_file), "--all"], cwd=repo_path)
            logger.info(f"Created bundle snapshot: {bundle_file}")
            return True
        except GitCommandError as e:
            logger.error(f"Failed to create bundle snapshot: {e}")
            return False

    def restore_snapshot(self, repo_path: Path, snapshot_name: str) -> bool:
        """
        Restore a repository from a bundle snapshot.
        """
        bundle_file = self.snapshots_path / f"{snapshot_name}.bundle"
        if not bundle_file.exists():
            logger.error(f"Snapshot bundle not found: {bundle_file}")
            return False

        try:
            # Clean up current repository directory
            if repo_path.exists():
                shutil.rmtree(repo_path)
            repo_path.mkdir(parents=True)

            # Clone from bundle
            self.git_executor.run(["clone", str(bundle_file), "."], cwd=repo_path)
            # Fix remote origin (it points to the bundle by default)
            self.git_executor.run(["remote", "remove", "origin"], cwd=repo_path)
            logger.info(f"Restored from bundle snapshot: {bundle_file}")
            return True
        except (GitCommandError, OSError) as e:
            logger.error(f"Failed to restore from snapshot: {e}")
            return False

    def cleanup_snapshots(self) -> None:
        """Delete all snapshots."""
        if self.snapshots_path.exists():
            shutil.rmtree(self.snapshots_path)
            self.snapshots_path.mkdir()
            logger.info("All snapshots cleaned up.")
