"""
Git Quest - Level Generators
Generators for complex Git repository states.
"""

import subprocess
from pathlib import Path


class MergeConflictGenerator:
    """Generates merge conflict scenarios."""

    @staticmethod
    def generate_simple_conflict(repo_path: Path) -> bool:
        """
        Generate a simple merge conflict.

        Args:
            repo_path: Path to repository

        Returns:
            True if successful
        """
        try:
            # Setup git config
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Create base file
            readme = repo_path / "README.md"
            readme.write_text("# Project\n\nThis is my project.\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)

            # Create feature branch with change
            subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_path, check=True)
            readme.write_text("# Project\n\nThis is the feature version.\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Update on feature"], cwd=repo_path, check=True)

            # Go back to main and make conflicting change
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
            readme.write_text("# Project\n\nThis is the main version.\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Update on main"], cwd=repo_path, check=True)

            # Start merge (will create conflict)
            subprocess.run(["git", "merge", "feature"], cwd=repo_path)

            return True
        except subprocess.CalledProcessError:
            return True  # Merge conflict expected to "fail"
        except Exception as e:
            print(f"Error generating conflict: {e}")
            return False

    @staticmethod
    def generate_multi_file_conflict(repo_path: Path) -> bool:
        """Generate conflicts in multiple files."""
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Create base files
            (repo_path / "config.py").write_text("DEBUG = False\nPORT = 8080\n")
            (repo_path / "main.py").write_text("print('Hello')\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo_path, check=True)

            # Feature branch changes
            subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_path, check=True)
            (repo_path / "config.py").write_text("DEBUG = True\nPORT = 3000\n")
            (repo_path / "main.py").write_text("print('Feature')\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Feature changes"], cwd=repo_path, check=True)

            # Main branch changes
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
            (repo_path / "config.py").write_text("DEBUG = False\nPORT = 9000\n")
            (repo_path / "main.py").write_text("print('Main')\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Main changes"], cwd=repo_path, check=True)

            # Merge
            subprocess.run(["git", "merge", "feature"], cwd=repo_path)

            return True
        except subprocess.CalledProcessError:
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


class RebaseGenerator:
    """Generates rebase scenarios."""

    @staticmethod
    def generate_simple_rebase(repo_path: Path) -> bool:
        """Generate a simple rebase scenario."""
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Base commit
            (repo_path / "README.md").write_text("# Project\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)

            # Feature branch
            subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_path, check=True)
            (repo_path / "feature.py").write_text("def feature(): pass\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Add feature"], cwd=repo_path, check=True)

            # Main branch updates
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
            (repo_path / "update1.txt").write_text("Update 1\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Update 1"], cwd=repo_path, check=True)

            (repo_path / "update2.txt").write_text("Update 2\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Update 2"], cwd=repo_path, check=True)

            # Back to feature
            subprocess.run(["git", "checkout", "feature"], cwd=repo_path, check=True)

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def generate_rebase_conflict(repo_path: Path) -> bool:
        """Generate a rebase scenario with conflicts."""
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Base
            (repo_path / "app.py").write_text("def main():\n    print('Base')\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Base"], cwd=repo_path, check=True)

            # Feature with conflicting change
            subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_path, check=True)
            (repo_path / "app.py").write_text("def main():\n    print('Feature')\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Feature change"], cwd=repo_path, check=True)

            # Main with conflicting change
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
            (repo_path / "app.py").write_text("def main():\n    print('Main')\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Main change"], cwd=repo_path, check=True)

            # Back to feature - ready for conflicted rebase
            subprocess.run(["git", "checkout", "feature"], cwd=repo_path, check=True)

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


class DetachedHeadGenerator:
    """Generates detached HEAD scenarios."""

    @staticmethod
    def generate_detached_head(repo_path: Path) -> bool:
        """Generate a detached HEAD state."""
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Create several commits
            for i in range(3):
                (repo_path / f"file{i}.txt").write_text(f"Content {i}\n")
                subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
                subprocess.run(["git", "commit", "-m", f"Commit {i}"], cwd=repo_path, check=True)

            # Get first commit hash
            result = subprocess.run(
                ["git", "rev-list", "--max-parents=0", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            first_commit = result.stdout.strip()

            # Detach HEAD
            subprocess.run(["git", "checkout", first_commit], cwd=repo_path, check=True)

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def generate_lost_commit_scenario(repo_path: Path) -> bool:
        """Generate a scenario with lost commits recoverable via reflog."""
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Create commits
            (repo_path / "important.txt").write_text("Important data\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Important work"], cwd=repo_path, check=True)

            # Create more work
            (repo_path / "more.txt").write_text("More data\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "More work"], cwd=repo_path, check=True)

            # Hard reset to lose commits
            result = subprocess.run(
                ["git", "rev-list", "--max-parents=0", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            first_commit = result.stdout.strip()
            subprocess.run(["git", "reset", "--hard", first_commit], cwd=repo_path, check=True)

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


class StashGenerator:
    """Generates stash scenarios."""

    @staticmethod
    def generate_stash_scenario(repo_path: Path) -> bool:
        """Generate a scenario requiring stashing."""
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Base commit
            (repo_path / "config.txt").write_text("setting=value\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo_path, check=True)

            # Make uncommitted changes
            (repo_path / "config.txt").write_text("setting=newvalue\n")
            (repo_path / "wip.txt").write_text("Work in progress\n")

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


class ComplexScenarioGenerator:
    """Generates complex multi-faceted scenarios."""

    @staticmethod
    def generate_escape_room(repo_path: Path) -> bool:
        """
        Generate an escape room scenario with multiple issues.
        """
        try:
            subprocess.run(["git", "config", "user.email", "game@local"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Game"], cwd=repo_path, check=True)

            # Create complex history
            (repo_path / "README.md").write_text("# Project\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo_path, check=True)

            # Create feature branch
            subprocess.run(["git", "checkout", "-b", "feature-1"], cwd=repo_path, check=True)
            (repo_path / "f1.txt").write_text("Feature 1\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Feature 1"], cwd=repo_path, check=True)

            # Create another branch from main
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
            subprocess.run(["git", "checkout", "-b", "feature-2"], cwd=repo_path, check=True)
            (repo_path / "f2.txt").write_text("Feature 2\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Feature 2"], cwd=repo_path, check=True)

            # Go back to main and update
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
            (repo_path / "main_update.txt").write_text("Main update\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Main update"], cwd=repo_path, check=True)

            # Create a stash
            (repo_path / "wip.txt").write_text("WIP\n")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "stash", "push", "-m", "WIP"], cwd=repo_path, check=True)

            # Create a tag
            subprocess.run(["git", "tag", "v1.0"], cwd=repo_path, check=True)

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


def generate_level_scenario(repo_path: Path, scenario_type: str) -> bool:
    """
    Generate a specific scenario type.

    Args:
        repo_path: Path to repository
        scenario_type: Type of scenario to generate

    Returns:
        True if successful
    """
    generators = {
        "merge_conflict": MergeConflictGenerator.generate_simple_conflict,
        "multi_file_conflict": MergeConflictGenerator.generate_multi_file_conflict,
        "simple_rebase": RebaseGenerator.generate_simple_rebase,
        "rebase_conflict": RebaseGenerator.generate_rebase_conflict,
        "detached_head": DetachedHeadGenerator.generate_detached_head,
        "lost_commit": DetachedHeadGenerator.generate_lost_commit_scenario,
        "stash": StashGenerator.generate_stash_scenario,
        "escape_room": ComplexScenarioGenerator.generate_escape_room,
    }

    generator = generators.get(scenario_type)
    if generator:
        return generator(repo_path)
    else:
        print(f"Unknown scenario type: {scenario_type}")
        return False
