"""
Git Quest - ASCII Graph Display
Generates ASCII visualizations of Git history.
"""

import subprocess
from pathlib import Path


class ASCIIGraphDisplay:
    """Generates ASCII art visualizations of Git repositories."""

    # Box drawing characters
    BOX = {
        "tl": "╔",
        "tr": "╗",
        "bl": "╚",
        "br": "╝",
        "h": "═",
        "v": "║",
        "tl_inner": "╠",
        "tr_inner": "╣",
        "bl_inner": "╚",
        "br_inner": "╝",
        "cross": "╬",
        "right_t": "╠",
        "left_t": "╣",
        "top_t": "╦",
        "bottom_t": "╩",
        "single_h": "─",
        "single_v": "│",
    }

    def generate_graph(self, repo_path: Path, style: str = "simple") -> str:
        """
        Generate an ASCII graph of the repository.

        Args:
            repo_path: Path to the repository
            style: Graph style ('simple', 'detailed', 'compact')

        Returns:
            ASCII graph string
        """
        if style == "simple":
            return self._generate_simple_graph(repo_path)
        elif style == "detailed":
            return self._generate_detailed_graph(repo_path)
        elif style == "compact":
            return self._generate_compact_graph(repo_path)
        else:
            return self._generate_simple_graph(repo_path)

    def _generate_simple_graph(self, repo_path: Path) -> str:
        """Generate a simple commit graph."""
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", "--all", "-30"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            return f"Error: {e}"

    def _generate_detailed_graph(self, repo_path: Path) -> str:
        """Generate a detailed graph with decorations."""
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--oneline", "--all", "--decorate", "-20"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            return f"Error: {e}"

    def _generate_compact_graph(self, repo_path: Path) -> str:
        """Generate a compact graph view."""
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--format=%h %s", "--all", "-15"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except Exception as e:
            return f"Error: {e}"

    def generate_branch_tree(self, repo_path: Path) -> str:
        """
        Generate a branch tree visualization.

        Args:
            repo_path: Path to the repository

        Returns:
            Branch tree string
        """
        lines = []
        lines.append(self._box_top("BRANCH STRUCTURE"))

        try:
            result = subprocess.run(
                ["git", "branch", "-vv", "--all"], cwd=repo_path, capture_output=True, text=True
            )

            branches = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    is_current = line.startswith("*")
                    clean = line.lstrip("* ").strip()
                    branches.append((is_current, clean))

            for i, (is_current, branch) in enumerate(branches):
                if is_current:
                    prefix = "├─► "
                else:
                    prefix = "├── "

                lines.append(f"│ {prefix}{branch}")

            if not branches:
                lines.append("│   No branches found")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(len(branches) if branches else 1))
        return "\n".join(lines)

    def generate_commit_timeline(self, repo_path: Path, max_commits: int = 20) -> str:
        """
        Generate a timeline view of commits.

        Args:
            repo_path: Path to the repository
            max_commits: Maximum commits to show

        Returns:
            Timeline string
        """
        lines = []
        lines.append(self._box_top("COMMIT TIMELINE"))

        try:
            result = subprocess.run(
                ["git", "log", "--all", "--format=%ar │ %h │ %s", f"-{max_commits}"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            for line in result.stdout.split("\n"):
                if line.strip():
                    lines.append(f"│   {line}")

            if not result.stdout.strip():
                lines.append("│   No commits found")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(max_commits))
        return "\n".join(lines)

    def generate_file_status(self, repo_path: Path) -> str:
        """
        Generate a file status display.

        Args:
            repo_path: Path to the repository

        Returns:
            File status string
        """
        lines = []
        lines.append(self._box_top("FILE STATUS"))

        try:
            result = subprocess.run(
                ["git", "status", "--short"], cwd=repo_path, capture_output=True, text=True
            )

            status_icons = {
                "M": "✏️",  # Modified
                "A": "➕",  # Added
                "D": "❌",  # Deleted
                "R": "🔄",  # Renamed
                "C": "📋",  # Copied
                "U": "⚠️",  # Updated but unmerged
                "?": "❓",  # Untracked
            }

            for line in result.stdout.split("\n"):
                if line.strip():
                    status = line[:2]
                    filename = line[3:]

                    icon = "  "
                    for char in status:
                        if char in status_icons:
                            icon = status_icons[char]
                            break

                    lines.append(f"│   [{status}] {icon} {filename}")

            if not result.stdout.strip():
                lines.append("│   ✓ Working directory clean")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(10))
        return "\n".join(lines)

    def generate_repo_summary(self, repo_path: Path) -> str:
        """
        Generate a repository summary display.

        Args:
            repo_path: Path to the repository

        Returns:
            Summary string
        """
        lines = []
        lines.append(self._box_top("REPOSITORY SUMMARY"))

        try:
            # Current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True
            )
            current_branch = result.stdout.strip() or "DETACHED HEAD"
            lines.append(f"│   📍 Branch: {current_branch}")

            # Commit count
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            commit_count = result.stdout.strip()
            lines.append(f"│   📊 Commits: {commit_count}")

            # Branch count
            result = subprocess.run(
                ["git", "branch", "--list"], cwd=repo_path, capture_output=True, text=True
            )
            branch_count = len([line for line in result.stdout.split("\n") if line.strip()])
            lines.append(f"│   🌿 Branches: {branch_count}")

            # Tag count
            result = subprocess.run(
                ["git", "tag", "--list"], cwd=repo_path, capture_output=True, text=True
            )
            tag_count = len([line for line in result.stdout.split("\n") if line.strip()])
            lines.append(f"│   🏷️  Tags: {tag_count}")

            # Stash count
            result = subprocess.run(
                ["git", "stash", "list"], cwd=repo_path, capture_output=True, text=True
            )
            stash_count = len([line for line in result.stdout.split("\n") if line.strip()])
            lines.append(f"│   📦 Stashes: {stash_count}")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(10))
        return "\n".join(lines)

    def generate_merge_conflict_display(self, repo_path: Path) -> str:
        """
        Generate a merge conflict status display.

        Args:
            repo_path: Path to the repository

        Returns:
            Conflict status string
        """
        lines = []
        lines.append(self._box_top("MERGE CONFLICT STATUS"))

        try:
            # Check for conflicts
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=U"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            conflicts = [f for f in result.stdout.split("\n") if f.strip()]

            if conflicts:
                lines.append("│   ⚠️  Conflicted files:")
                for f in conflicts:
                    lines.append(f"│       - {f}")
                lines.append("│")
                lines.append("│   💡 Resolve by:")
                lines.append("│       1. Edit files to fix conflicts")
                lines.append("│       2. git add <file>")
                lines.append("│       3. git commit")
            else:
                # Check if merge is in progress
                merge_head = repo_path / ".git" / "MERGE_HEAD"
                if merge_head.exists():
                    lines.append("│   🔄 Merge in progress (no conflicts)")
                    lines.append("│   Run 'git commit' to complete")
                else:
                    lines.append("│   ✓ No merge conflicts")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(10))
        return "\n".join(lines)

    def _box_top(self, title: str) -> str:
        """Generate top box border."""
        width = max(len(title) + 4, 50)
        return "┌" + "─" * width + "┐\n" f"│ {title:^{width}} │\n" "├" + "─" * width + "┤"

    def _box_bottom(self, height: int) -> str:
        """Generate bottom box border."""
        width = 50
        return "└" + "─" * width + "┘"

    def generate_comparison_view(self, repo_path: Path, ref1: str, ref2: str) -> str:
        """
        Generate a comparison between two refs.

        Args:
            repo_path: Path to the repository
            ref1: First ref (branch, tag, commit)
            ref2: Second ref

        Returns:
            Comparison string
        """
        lines = []
        lines.append(self._box_top(f"COMPARISON: {ref1} vs {ref2}"))

        try:
            # Commits in ref1 but not ref2
            result1 = subprocess.run(
                ["git", "log", "--oneline", f"{ref2}..{ref1}"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            only_in_1 = [c for c in result1.stdout.split("\n") if c.strip()]

            # Commits in ref2 but not ref1
            result2 = subprocess.run(
                ["git", "log", "--oneline", f"{ref1}..{ref2}"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            only_in_2 = [c for c in result2.stdout.split("\n") if c.strip()]

            lines.append("│")
            lines.append(f"│  Only in {ref1} ({len(only_in_1)} commits):")
            for commit in only_in_1[:10]:
                lines.append(f"│    + {commit}")
            if len(only_in_1) > 10:
                lines.append(f"│    ... and {len(only_in_1) - 10} more")

            lines.append("│")
            lines.append(f"│  Only in {ref2} ({len(only_in_2)} commits):")
            for commit in only_in_2[:10]:
                lines.append(f"│    - {commit}")
            if len(only_in_2) > 10:
                lines.append(f"│    ... and {len(only_in_2) - 10} more")

            # Common ancestor
            result3 = subprocess.run(
                ["git", "merge-base", ref1, ref2], cwd=repo_path, capture_output=True, text=True
            )
            if result3.returncode == 0:
                ancestor = result3.stdout.strip()[:8]
                lines.append("│")
                lines.append(f"│  Common ancestor: {ancestor}")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(15))
        return "\n".join(lines)

    def generate_stash_list(self, repo_path: Path) -> str:
        """
        Generate a stash list display.

        Args:
            repo_path: Path to the repository

        Returns:
            Stash list string
        """
        lines = []
        lines.append(self._box_top("STASHES"))

        try:
            result = subprocess.run(
                ["git", "stash", "list"], cwd=repo_path, capture_output=True, text=True
            )

            stashes = [s for s in result.stdout.split("\n") if s.strip()]

            if stashes:
                for stash in stashes:
                    lines.append(f"│   📦 {stash}")
            else:
                lines.append("│   No stashes")

        except Exception as e:
            lines.append(f"│ Error: {e}")

        lines.append(self._box_bottom(10))
        return "\n".join(lines)


def format_graph_output(graph: str, title: str | None = None) -> str:
    """
    Format a graph for display.

    Args:
        graph: Graph string
        title: Optional title

    Returns:
        Formatted string
    """
    if not graph:
        return "No data to display"

    if title:
        width = max(len(line) for line in graph.split("\n"))
        border = "═" * width

        return (
            f"\n╔{border}╗\n"
            f"║ {title:^{width-2}} ║\n"
            f"╠{border}╣\n"
            + "\n".join(f"║ {line:<{width-2}} ║" for line in graph.split("\n"))
            + f"\n╚{border}╝\n"
        )

    return graph
