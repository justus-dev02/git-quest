"""
Git Quest - Git Graph Generator
Generates ASCII visualizations of Git repository history.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from core.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class Commit:
    """Represents a commit in the graph."""

    hash: str
    short_hash: str
    message: str
    author: str
    date: str
    parents: List[str]
    branches: List[str]
    tags: List[str]
    graph_line: str


class GitGraphGenerator:
    """Generates ASCII visualizations of Git history."""

    def __init__(self, repo_path: Path):
        self.repo_path: Path = repo_path

    def generate_simple_graph(self, max_commits: int = 50) -> str:
        """
        Generate a simple ASCII commit graph.

        Args:
            max_commits: Maximum number of commits to show

        Returns:
            ASCII graph string
        """
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", "--all", f"-{max_commits}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error generating simple graph: {e}")
            return f"Error generating graph: {e}"

    def generate_decorated_graph(self, max_commits: int = 50) -> str:
        """
        Generate a graph with branch and tag decorations.

        Args:
            max_commits: Maximum number of commits to show

        Returns:
            Decorated ASCII graph string
        """
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", "--all", "--decorate", f"-{max_commits}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error generating decorated graph: {e}")
            return f"Error generating graph: {e}"

    def generate_branch_specific_graph(self, branch: str, max_commits: int = 50) -> str:
        """
        Generate a graph for a specific branch.

        Args:
            branch: Branch name
            max_commits: Maximum number of commits to show

        Returns:
            ASCII graph string
        """
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", branch, f"-{max_commits}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error generating branch specific graph: {e}")
            return f"Error generating graph: {e}"

    def generate_detailed_graph(self, max_commits: int = 20) -> str:
        """
        Generate a detailed graph with commit messages and metadata.

        Args:
            max_commits: Maximum number of commits to show

        Returns:
            Detailed ASCII graph string
        """
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--format=%h %s (%an, %ar)", "--all", f"-{max_commits}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Error generating detailed graph: {e}")
            return f"Error generating graph: {e}"

    def parse_commits(self, max_commits: int = 100) -> List[Commit]:
        """
        Parse commits into structured format.

        Args:
            max_commits: Maximum number of commits to parse

        Returns:
            List of Commit objects
        """
        commits = []

        try:
            # Get commit data with custom format
            result = subprocess.run(
                ["git", "log", "--all", "--format=%H|%h|%s|%an|%ai|%P", f"-{max_commits}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                parts = line.split("|")
                if len(parts) >= 6:
                    commit = Commit(
                        hash=parts[0],
                        short_hash=parts[1],
                        message=parts[2],
                        author=parts[3],
                        date=parts[4],
                        parents=parts[5].split() if parts[5] else [],
                        branches=[],
                        tags=[],
                        graph_line="",
                    )
                    commits.append(commit)

            # Get branch information
            subprocess.run(
                ["git", "branch", "-a", "--contains", "--format=%(refname:short)"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            # Get tag information
            subprocess.run(
                ["git", "tag", "--list", "--contains"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            # Associate branches and tags with commits
            # (simplified - full implementation would map each commit)

        except Exception as e:
            logger.error(f"Error parsing commits: {e}")

        return commits

    def generate_custom_graph(self, commits: List[Commit]) -> str:
        """
        Generate a custom ASCII graph from parsed commits.

        Args:
            commits: List of Commit objects

        Returns:
            Custom ASCII graph string
        """
        if not commits:
            return "No commits to display"

        lines = []
        lines.append("╔════════════════════════════════════════════════════════╗")
        lines.append("║                    COMMIT HISTORY                      ║")
        lines.append("╠════════════════════════════════════════════════════════╣")

        for i, commit in enumerate(commits[:20]):  # Limit display
            # Build branch/tag decorations
            decorations = []
            if commit.branches:
                decorations.extend(commit.branches)
            if commit.tags:
                decorations.extend([f"tag: {t}" for t in commit.tags])

            decor_str = ""
            if decorations:
                decor_str = f" [{', '.join(decorations)}]"

            # Build graph line
            prefix = "● " if i == 0 else "○ "
            if len(commit.parents) > 1:
                prefix = "●─┬ "  # Merge commit
            elif i < len(commits) - 1 and len(commits[i + 1].parents) > 1:
                prefix = "○─┘ "  # Before merge

            line = f"{prefix}{commit.short_hash} {commit.message}{decor_str}"
            lines.append(f"║ {line[:58]:<58} ║")

        lines.append("╚════════════════════════════════════════════════════════╝")

        return "\n".join(lines)

    def generate_tree_view(self) -> str:
        """
        Generate a tree-like view of branches.

        Returns:
            Tree view string
        """
        lines = []
        lines.append("Branch Structure:")
        lines.append("─" * 40)

        try:
            # Get all branches
            result = subprocess.run(
                ["git", "branch", "-vv", "--all"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue

                is_current = line.startswith("*")
                clean_line = line.lstrip("* ").strip()

                if is_current:
                    lines.append(f"├─► {clean_line}")
                else:
                    lines.append(f"├── {clean_line}")

        except Exception as e:
            logger.error(f"Error generating tree view: {e}")
            lines.append(f"Error: {e}")

        return "\n".join(lines)

    def _get_current_branch(self) -> str:
        """Get current branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Error getting current branch: {e}")
            return ""

    def generate_comparison_graph(self, branch1: str, branch2: str) -> str:
        """
        Generate a graph comparing two branches.

        Args:
            branch1: First branch name
            branch2: Second branch name

        Returns:
            Comparison graph string
        """
        lines = []
        lines.append(f"Comparing: {branch1} vs {branch2}")
        lines.append("=" * 50)

        try:
            # Get commits only in branch1
            result1 = subprocess.run(
                ["git", "log", "--oneline", f"{branch2}..{branch1}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            # Get commits only in branch2
            result2 = subprocess.run(
                ["git", "log", "--oneline", f"{branch1}..{branch2}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            # Get common ancestor
            result3 = subprocess.run(
                ["git", "merge-base", branch1, branch2],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            lines.append(f"\n{branch1} only:")
            for commit in result1.stdout.strip().split("\n"):
                if commit:
                    lines.append(f"  + {commit}")

            lines.append(f"\n{branch2} only:")
            for commit in result2.stdout.strip().split("\n"):
                if commit:
                    lines.append(f"  - {commit}")

            lines.append(f"\nCommon ancestor: {result3.stdout.strip()[:8]}")

        except Exception as e:
            logger.error(f"Error generating comparison graph: {e}")
            lines.append(f"Error: {e}")

        return "\n".join(lines)

    def generate_timeline(self, max_commits: int = 30) -> str:
        """
        Generate a timeline view of commits.

        Args:
            max_commits: Maximum number of commits to show

        Returns:
            Timeline string
        """
        lines = []
        lines.append("Commit Timeline:")
        lines.append("─" * 60)

        try:
            result = subprocess.run(
                ["git", "log", "--all", "--format=%ar │ %h │ %s", f"-{max_commits}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.strip().split("\n"):
                if line:
                    lines.append(f"  {line}")

        except Exception as e:
            logger.error(f"Error generating timeline: {e}")
            lines.append(f"Error: {e}")

        return "\n".join(lines)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get repository statistics.

        Returns:
            Dict with statistics
        """
        stats: Dict[str, Any] = {
            "total_commits": 0,
            "total_branches": 0,
            "total_tags": 0,
            "contributors": 0,
            "first_commit": None,
            "last_commit": None,
        }

        try:
            # Total commits
            result = subprocess.run(
                ["git", "rev-list", "--count", "--all"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            stats["total_commits"] = int(result.stdout.strip())

            # Total branches
            result = subprocess.run(
                ["git", "branch", "--list"], cwd=self.repo_path, capture_output=True, text=True
            )
            stats["total_branches"] = len(
                [line for line in result.stdout.split("\n") if line.strip()]
            )

            # Total tags
            result = subprocess.run(
                ["git", "tag", "--list"], cwd=self.repo_path, capture_output=True, text=True
            )
            stats["total_tags"] = len([line for line in result.stdout.split("\n") if line.strip()])

            # Contributors
            result = subprocess.run(
                ["git", "shortlog", "-sn", "--all"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            stats["contributors"] = len(
                [line for line in result.stdout.split("\n") if line.strip()]
            )

            # First and last commit dates
            result = subprocess.run(
                ["git", "log", "--all", "--format=%ai", "--reverse"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            dates = [d for d in result.stdout.split("\n") if d.strip()]
            if dates:
                stats["first_commit"] = dates[0]
                stats["last_commit"] = dates[-1]

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")

        return stats


def generate_graph(repo_path: Path, style: str = "simple") -> str:
    """
    Convenience function to generate a graph.

    Args:
        repo_path: Path to repository
        style: Graph style ('simple', 'decorated', 'detailed', 'timeline')

    Returns:
        ASCII graph string
    """
    generator = GitGraphGenerator(repo_path)

    if style == "simple":
        return generator.generate_simple_graph()
    elif style == "decorated":
        return generator.generate_decorated_graph()
    elif style == "detailed":
        return generator.generate_detailed_graph()
    elif style == "timeline":
        return generator.generate_timeline()
    else:
        return generator.generate_simple_graph()
