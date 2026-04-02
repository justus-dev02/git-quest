"""
Git Quest - Hint System
Provides contextual hints for levels.
"""

from typing import Any, Dict, List, Optional


class HintSystem:
    """Manages hints for levels."""

    def __init__(self) -> None:
        # Additional contextual hints by objective type
        self.contextual_hints = {
            "commit_exists": [
                "Make sure you have files to commit",
                "Use 'git status' to see what needs to be staged",
                "Don't forget the -m flag for the commit message",
            ],
            "branch_exists": [
                "Use 'git branch' to list existing branches",
                "Branch names are case-sensitive",
                "Make sure you're creating the exact branch name required",
            ],
            "current_branch": [
                "The current branch is marked with * in 'git branch' output",
                "Use 'git checkout <branch>' to switch",
                "Or use 'git switch <branch>' in newer Git versions",
            ],
            "merge_completed": [
                "Make sure you're on the target branch before merging",
                "Use 'git merge <branch-name>'",
                "Check 'git branch --merged' to see merged branches",
            ],
            "conflict_resolved": [
                "Look for conflict markers: <<<<<<<, =======, >>>>>>>",
                "Edit the file to keep the desired changes",
                "After fixing, use 'git add' then 'git commit'",
            ],
            "rebase_completed": [
                "Use 'git rebase <base-branch>'",
                "If there are conflicts, resolve and use 'git rebase --continue'",
                "Use 'git rebase --abort' to cancel",
            ],
            "stash_exists": [
                "Make uncommitted changes first",
                "Use 'git stash' or 'git stash push -m \"message\"'",
                "Check with 'git stash list'",
            ],
            "tag_exists": [
                "Use 'git tag <name>' for a lightweight tag",
                "Or 'git tag -a <name> -m \"message\"' for annotated",
                "List tags with 'git tag'",
            ],
            "reset_completed": [
                "Use 'git reset --soft' to keep changes staged",
                "Use 'git reset --mixed' (default) to unstage",
                "Use 'git reset --hard' to discard all changes",
            ],
            "detached_head": [
                "Checkout a specific commit hash to detach HEAD",
                "Or checkout a tag to view that version",
                "Create a branch to save any work in this state",
            ],
            "head_attached": [
                "Checkout a branch to attach HEAD",
                "Use 'git checkout <branch-name>'",
                "Avoid making commits in detached HEAD state",
            ],
            "clean_state": [
                "Commit or stash any uncommitted changes",
                "Use 'git status' to see what's pending",
                "Clean untracked files with 'git clean -fd'",
            ],
            "reflog_recovery": [
                "Use 'git reflog' to see all HEAD movements",
                "Find the commit hash you want to recover",
                "Use 'git reset --hard <commit>' or 'git checkout -b <branch> <commit>'",
            ],
            "bisect_completed": [
                "Start with 'git bisect start'",
                "Mark current as bad: 'git bisect bad'",
                "Mark a known good commit: 'git bisect good <commit>'",
                "Test each step and mark good/bad",
                "End with 'git bisect reset'",
            ],
            "cherry_pick_completed": [
                "Find the commit hash you want",
                "Use 'git cherry-pick <commit-hash>'",
                "Resolve conflicts if any occur",
            ],
            "orphan_branch": [
                "Use 'git checkout --orphan <branch-name>'",
                "Remove tracked files with 'git rm -rf .'",
                "Add new files and commit",
            ],
            "squash_commits": [
                "Use 'git rebase -i HEAD~N' where N is number of commits",
                "Change 'pick' to 'squash' or 's' for commits to combine",
                "Write a combined commit message",
            ],
            "amend_commit": [
                "Stage any additional files you want to add",
                "Use 'git commit --amend'",
                "Edit the message if needed",
            ],
            "revert_commit": [
                "Find the commit hash with 'git log'",
                "Use 'git revert <commit-hash>'",
                "This creates a new commit that undoes the changes",
            ],
            "remote_exists": [
                "Use 'git remote add <name> <url>'",
                "Common remote name is 'origin'",
                "Verify with 'git remote -v'",
            ],
            "commit_count": [
                "Check current count with 'git rev-list --count HEAD'",
                "Create more commits if needed",
                "Or squash commits to reduce count",
            ],
        }

    def get_hint(self, level_data: Dict[str, Any], hint_index: int) -> str:
        """
        Get a hint for a level.

        Args:
            level_data: Level configuration
            hint_index: Which hint to get (0-based)

        Returns:
            Hint string
        """
        level_hints = level_data.get("hints", [])

        if hint_index < len(level_hints):
            return str(level_hints[hint_index])

        # Fall back to contextual hints
        objective_type = level_data.get("objective", {}).get("type", "")
        contextual = self.contextual_hints.get(objective_type, [])

        if contextual:
            # Return contextual hint based on how many hints already used
            extra_index = hint_index - len(level_hints)
            if extra_index < len(contextual):
                return f"💡 Extra hint: {contextual[extra_index]}"

        return "💡 Check the objective requirements and try different Git commands."

    def get_all_hints(self, level_data: Dict[str, Any]) -> List[str]:
        """
        Get all hints for a level.

        Args:
            level_data: Level configuration

        Returns:
            List of all hints
        """
        hints = list(level_data.get("hints", []))

        objective_type = level_data.get("objective", {}).get("type", "")
        contextual = self.contextual_hints.get(objective_type, [])
        hints.extend([f"Extra: {h}" for h in contextual])

        return [str(h) for h in hints]

    def get_hint_for_command(self, command: str) -> Optional[str]:
        """
        Get a hint related to a specific command.

        Args:
            command: Git command

        Returns:
            Hint string or None
        """
        command_hints = {
            "merge": "Make sure you're on the correct branch before merging",
            "rebase": "Rebase replays commits on top of another base",
            "cherry-pick": "Cherry-pick applies a specific commit to current branch",
            "reset": "Reset moves the current branch pointer. Use with caution!",
            "revert": "Revert creates a new commit that undoes changes",
            "stash": "Stash temporarily saves uncommitted changes",
            "bisect": "Bisect helps find the commit that introduced a bug",
            "reflog": "Reflog shows all movements of HEAD, even lost commits",
            "checkout": "Checkout can switch branches or detach HEAD",
            "switch": "Switch is a newer command specifically for branches",
            "restore": "Restore can undo changes in working directory or staging",
            "branch": "Branch without arguments lists all branches",
            "tag": "Tags mark specific points in history as important",
            "fetch": "Fetch downloads objects from remote without merging",
            "pull": "Pull is fetch + merge in one command",
            "push": "Push uploads your commits to a remote repository",
        }

        # Extract command from full command string
        parts = command.strip().split()
        if len(parts) >= 2 and parts[0] == "git":
            cmd = parts[1]
            return command_hints.get(cmd)

        return None

    def get_progressive_hint(
        self, level_data: Dict[str, Any], attempts: int, time_elapsed: float
    ) -> str:
        """
        Get a hint that gets more specific based on attempts/time.

        Args:
            level_data: Level configuration
            attempts: Number of failed attempts
            time_elapsed: Time spent on level in seconds

        Returns:
            Progressive hint
        """
        hints = level_data.get("hints", [])

        if not hints:
            return "Keep trying different Git commands!"

        # More attempts = more specific hint
        if attempts < 3:
            return str(hints[0]) if hints else "Try the basics first"
        elif attempts < 6:
            return str(hints[1]) if len(hints) > 1 else str(hints[0])
        else:
            # Very specific hint
            return str(hints[-1]) if hints else "Check git status for clues"

    def get_objective_explanation(self, objective_type: str) -> str:
        """
        Get an explanation of what an objective type means.

        Args:
            objective_type: Type of objective

        Returns:
            Explanation string
        """
        explanations = {
            "commit_exists": "A commit with the specified message must exist in the history",
            "branch_exists": "A branch with the specified name must exist",
            "current_branch": "You must be on the specified branch",
            "merge_completed": "The specified branch must be merged into current branch",
            "conflict_resolved": "All merge conflicts must be resolved",
            "rebase_completed": "Rebase operation must be completed successfully",
            "stash_exists": "At least one stash must exist",
            "tag_exists": "A tag with the specified name must exist",
            "reset_completed": "Reset operation must be completed",
            "detached_head": "HEAD must be in detached state",
            "head_attached": "HEAD must be attached to a branch",
            "clean_state": "Working directory must have no uncommitted changes",
            "reflog_recovery": "A lost commit must be recovered",
            "bisect_completed": "Bisect operation must find the bad commit",
            "cherry_pick_completed": "Cherry-pick operation must complete",
            "orphan_branch": "An orphan branch with no shared history must exist",
            "squash_commits": "Multiple commits must be combined into fewer",
            "amend_commit": "The last commit must be amended",
            "revert_commit": "A commit must be reverted",
            "commit_count": "The repository must have a specific number of commits",
            "remote_exists": "A remote with the specified name must be configured",
        }

        return explanations.get(
            objective_type, "Complete the Git operation described in the objective"
        )

    def get_common_mistakes(self, objective_type: str) -> List[str]:
        """
        Get common mistakes for an objective type.

        Args:
            objective_type: Type of objective

        Returns:
            List of common mistakes
        """
        mistakes = {
            "commit_exists": [
                "Forgetting to stage files before committing",
                "Using wrong commit message format",
                "Not configuring git user name/email",
            ],
            "branch_exists": [
                "Typo in branch name",
                "Creating branch but on wrong commit",
                "Not verifying branch was created",
            ],
            "merge_completed": [
                "Trying to merge from wrong branch",
                "Not resolving conflicts properly",
                "Aborting merge before completion",
            ],
            "conflict_resolved": [
                "Leaving conflict markers in files",
                "Not staging resolved files",
                "Forgetting to commit after resolving",
            ],
            "rebase_completed": [
                "Not being on the correct branch",
                "Aborting rebase at first conflict",
                "Not using --continue after resolving",
            ],
            "detached_head": [
                "Making commits without creating a branch",
                "Losing work by switching away",
                "Not understanding what detached HEAD means",
            ],
            "reflog_recovery": [
                "Not using reflog to find lost commits",
                "Using wrong commit hash",
                "Not verifying recovery was successful",
            ],
        }

        return mistakes.get(objective_type, ["Review the objective carefully"])


def format_hint(hint: str, include_icon: bool = True) -> str:
    """
    Format a hint for display.

    Args:
        hint: Hint string
        include_icon: Whether to include lightbulb icon

    Returns:
        Formatted hint
    """
    icon = "💡 " if include_icon else ""

    # Check if hint already has formatting
    if hint.startswith("💡") or hint.startswith("Extra:"):
        return hint

    return f"{icon}{hint}"
