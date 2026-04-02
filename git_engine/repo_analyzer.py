"""
Git Quest - Repository Analyzer
Analyzes Git repository state and structure.
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from core.logger import setup_logger

logger = setup_logger(__name__)


class RepoAnalyzer:
    """Analyzes Git repository state."""

    def __init__(self) -> None:
        pass

    def analyze_repo(self, repo_path: Path) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a repository.

        Args:
            repo_path: Path to the repository

        Returns:
            Dict with repository analysis
        """
        if not repo_path.exists():
            return {"error": "Repository path does not exist"}

        git_dir = repo_path / ".git"
        if not git_dir.exists():
            return {"error": "Not a Git repository"}

        return {
            "is_valid": True,
            "current_branch": self.get_current_branch(repo_path),
            "is_detached": self.is_head_detached(repo_path),
            "branches": self.get_all_branches(repo_path),
            "tags": self.get_all_tags(repo_path),
            "commit_count": self.get_commit_count(repo_path),
            "has_uncommitted_changes": self.has_uncommitted_changes(repo_path),
            "has_merge_conflict": self.has_merge_conflict(repo_path),
            "remotes": self.get_remotes(repo_path),
            "recent_commits": self.get_recent_commits(repo_path),
            "stash_count": self.get_stash_count(repo_path),
        }

    def get_current_branch(self, repo_path: Path) -> Optional[str]:
        """Get the current branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True
            )
            if result.returncode == 0:
                branch = result.stdout.strip()
                return branch if branch else None
            return None
        except Exception as e:
            logger.error(f"Error getting current branch: {e}", exc_info=True)
            return None

    def is_head_detached(self, repo_path: Path) -> bool:
        """Check if HEAD is detached."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip() == "HEAD"
        except Exception as e:
            logger.error(f"Error checking if HEAD is detached: {e}", exc_info=True)
            return False

    def get_all_branches(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Get all branches with details."""
        branches = []

        try:
            # Get all branches with their upstream and last commit
            result = subprocess.run(
                ["git", "branch", "-vv", "--all"], cwd=repo_path, capture_output=True, text=True
            )

            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                is_current = line.startswith("*")
                line = line.lstrip("* ").strip()
                parts = line.split()

                if len(parts) >= 1:
                    branch_info = {
                        "name": parts[0],
                        "is_current": is_current,
                        "is_remote": "/" in parts[0],
                    }

                    # Try to get commit hash
                    if len(parts) >= 2 and len(parts[1]) >= 7:
                        branch_info["commit"] = parts[1]

                    branches.append(branch_info)

        except Exception as e:
            logger.error(f"Error getting all branches: {e}", exc_info=True)

        return branches

    def get_all_tags(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Get all tags with details."""
        tags = []

        try:
            result = subprocess.run(
                ["git", "tag", "-l", "--format=%(refname:short) %(objectname:short)"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                parts = line.split()
                tag_info = {
                    "name": parts[0] if parts else "",
                }

                if len(parts) >= 2:
                    tag_info["commit"] = parts[1]

                tags.append(tag_info)

        except Exception as e:
            logger.error(f"Error getting all tags: {e}", exc_info=True)

        return tags

    def get_commit_count(self, repo_path: Path) -> int:
        """Get total number of commits on current branch."""
        try:
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
            return 0
        except Exception as e:
            logger.error(f"Error getting commit count: {e}", exc_info=True)
            return 0

    def has_uncommitted_changes(self, repo_path: Path) -> bool:
        """Check if there are uncommitted changes."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"], cwd=repo_path, capture_output=True, text=True
            )
            return bool(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error checking for uncommitted changes: {e}", exc_info=True)
            return False

    def has_merge_conflict(self, repo_path: Path) -> bool:
        """Check if there's an ongoing merge conflict."""
        try:
            # Check for MERGE_HEAD
            merge_head = repo_path / ".git" / "MERGE_HEAD"
            if merge_head.exists():
                return True

            # Check for unmerged files
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=U"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            return bool(result.stdout.strip())

        except Exception as e:
            logger.error(f"Error checking for merge conflict: {e}", exc_info=True)
            return False

    def get_remotes(self, repo_path: Path) -> List[Dict[str, str]]:
        """Get configured remotes."""
        remotes = []

        try:
            result = subprocess.run(
                ["git", "remote", "-v"], cwd=repo_path, capture_output=True, text=True
            )

            seen: Set[str] = set()
            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    if name not in seen:
                        seen.add(name)
                        remotes.append(
                            {
                                "name": name,
                                "url": parts[1],
                            }
                        )

        except Exception as e:
            logger.error(f"Error getting remotes: {e}", exc_info=True)

        return remotes

    def get_recent_commits(self, repo_path: Path, count: int = 10) -> List[Dict[str, str]]:
        """Get recent commits."""
        commits = []

        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--format=%H|%h|%s|%an|%ae|%ai", "--all"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                parts = line.split("|")
                if len(parts) >= 6:
                    commits.append(
                        {
                            "hash": parts[0],
                            "short_hash": parts[1],
                            "message": parts[2],
                            "author": parts[3],
                            "email": parts[4],
                            "date": parts[5],
                        }
                    )

        except Exception as e:
            logger.error(f"Error getting recent commits: {e}", exc_info=True)

        return commits

    def get_stash_count(self, repo_path: Path) -> int:
        """Get number of stashes."""
        try:
            result = subprocess.run(
                ["git", "stash", "list"], cwd=repo_path, capture_output=True, text=True
            )
            return len([l for l in result.stdout.split("\n") if l.strip()])
        except Exception as e:
            logger.error(f"Error getting stash count: {e}", exc_info=True)
            return 0

    def get_commit_graph(self, repo_path: Path) -> str:
        """Get ASCII commit graph."""
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", "--all"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error getting commit graph: {e}", exc_info=True)
            return f"Error: {e}"

    def get_branch_graph(self, repo_path: Path) -> str:
        """Get detailed branch visualization."""
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", "--all", "--decorate"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error getting branch graph: {e}", exc_info=True)
            return f"Error: {e}"

    def get_file_status(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Get status of all files."""
        files = []

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain", "-z"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            entries = result.stdout.split("\x00")
            for entry in entries:
                if not entry.strip():
                    continue

                status = entry[:2]
                filename = entry[3:]

                files.append(
                    {
                        "filename": filename,
                        "status": status,
                        "staged": status[0] != " ",
                        "unstaged": status[1] != " ",
                    }
                )

        except Exception as e:
            logger.error(f"Error getting file status: {e}", exc_info=True)

        return files

    def get_conflicting_files(self, repo_path: Path) -> List[str]:
        """Get list of files with conflicts."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=U"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return [f.strip() for f in result.stdout.split("\n") if f.strip()]
        except Exception as e:
            logger.error(f"Error getting conflicting files: {e}", exc_info=True)
            return []

    def get_head_commit(self, repo_path: Path) -> Optional[Dict[str, str]]:
        """Get HEAD commit information."""
        try:
            result = subprocess.run(
                ["git", "show", "-1", "--format=%H|%h|%s|%an|%ai"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                parts = result.stdout.strip().split("|")
                if len(parts) >= 5:
                    return {
                        "hash": parts[0],
                        "short_hash": parts[1],
                        "message": parts[2],
                        "author": parts[3],
                        "date": parts[4],
                    }
            return None
        except Exception as e:
            logger.error(f"Error getting HEAD commit: {e}", exc_info=True)
            return None

    def get_branches_merged(self, repo_path: Path, branch: str | None = None) -> List[str]:
        """Get list of branches merged into specified branch."""
        try:
            cmd = ["git", "branch", "--merged"]
            if branch:
                cmd.append(branch)

            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)

            branches = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    branches.append(line.strip().lstrip("* ").strip())

            return branches
        except Exception as e:
            logger.error(f"Error getting merged branches: {e}", exc_info=True)
            return []

    def get_branches_not_merged(self, repo_path: Path, branch: str | None = None) -> List[str]:
        """Get list of branches not merged into specified branch."""
        try:
            cmd = ["git", "branch", "--no-merged"]
            if branch:
                cmd.append(branch)

            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)

            branches = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    branches.append(line.strip().lstrip("* ").strip())

            return branches
        except Exception as e:
            logger.error(f"Error getting not merged branches: {e}", exc_info=True)
            return []

    def get_reflog(self, repo_path: Path, count: int = 20) -> List[Dict[str, str]]:
        """Get reflog entries."""
        entries = []

        try:
            result = subprocess.run(
                ["git", "reflog", f"-{count}", "--format=%H|%gs|%gd|%an|%ai"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                parts = line.split("|")
                if len(parts) >= 5:
                    entries.append(
                        {
                            "hash": parts[0],
                            "action": parts[1],
                            "reflog_index": parts[2],
                            "author": parts[3],
                            "date": parts[4],
                        }
                    )

        except Exception as e:
            logger.error(f"Error getting reflog: {e}", exc_info=True)

        return entries
