"""
Git Quest - Git Commands
Helper functions for common Git operations.
"""

import subprocess
from pathlib import Path
from typing import List, Tuple

from core.exceptions import GitCommandError
from core.logger import setup_logger

logger = setup_logger(__name__)


class GitCommands:
    """Helper class for executing Git commands."""

    def __init__(self, repo_path: Path):
        self.repo_path: Path = repo_path

    def run(self, args: List[str], check: bool = True) -> Tuple[bool, str, str]:
        """
        Run a git command.

        Args:
            args: Command arguments (without 'git')
            check: If True (default), raise exception on error

        Returns:
            Tuple of (success, stdout, stderr)

        Raises:
            GitCommandError: if check is True and command fails
        """
        cmd = ["git"] + args

        try:
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=30
            )

            success = result.returncode == 0

            if not success:
                logger.error(f"Git command failed: {' '.join(cmd)}\nStderr: {result.stderr}")
                if check:
                    raise GitCommandError(f"Git command failed: {result.stderr}")

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            logger.error(f"Git command timed out: {' '.join(cmd)}")
            if check:
                raise GitCommandError("Command timed out")
            return False, "", "Command timed out"
        except GitCommandError:
            raise
        except Exception as e:
            logger.error(f"Error executing git command: {e}")
            if check:
                raise GitCommandError(str(e))
            return False, "", str(e)

    def init(self, initial_branch: str = "main") -> Tuple[bool, str, str]:
        """Initialize a new repository."""
        return self.run(["init", f"--initial-branch={initial_branch}"])

    def clone(self, url: str, directory: str | None = None) -> Tuple[bool, str, str]:
        """Clone a repository."""
        args = ["clone", url]
        if directory:
            args.append(directory)
        return self.run(args)

    def add(self, files: List[str] | None = None, all_files: bool = False) -> Tuple[bool, str, str]:
        """Stage files."""
        args = ["add"]
        if all_files:
            args.append(".")
        elif files:
            args.extend(files)
        return self.run(args)

    def commit(self, message: str, amend: bool = False) -> Tuple[bool, str, str]:
        """Create a commit."""
        args = ["commit", "-m", message]
        if amend:
            args.append("--amend")
        return self.run(args)

    def checkout(
        self, target: str, create_branch: bool = False, orphan: bool = False
    ) -> Tuple[bool, str, str]:
        """Checkout a branch or commit."""
        args = ["checkout"]
        if orphan:
            args.append("--orphan")
        elif create_branch:
            args.append("-b")
        args.append(target)
        return self.run(args)

    def branch(
        self, name: str, delete: bool = False, force_delete: bool = False
    ) -> Tuple[bool, str, str]:
        """Create or delete a branch."""
        args = ["branch"]
        if delete:
            args.append("-d")
        elif force_delete:
            args.append("-D")
        args.append(name)
        return self.run(args)

    def merge(self, branch: str, no_ff: bool = False, abort: bool = False) -> Tuple[bool, str, str]:
        """Merge a branch."""
        args = ["merge"]
        if abort:
            args.append("--abort")
        elif no_ff:
            args.append("--no-ff")
        args.append(branch)
        return self.run(args)

    def rebase(
        self, branch: str, abort: bool = False, continue_rebase: bool = False
    ) -> Tuple[bool, str, str]:
        """Rebase current branch."""
        args = ["rebase"]
        if abort:
            args.append("--abort")
        elif continue_rebase:
            args.append("--continue")
        args.append(branch)
        return self.run(args)

    def pull(self, remote: str = "origin", branch: str | None = None) -> Tuple[bool, str, str]:
        """Pull from remote."""
        args = ["pull", remote]
        if branch:
            args.append(branch)
        return self.run(args)

    def push(
        self,
        remote: str = "origin",
        branch: str | None = None,
        force: bool = False,
        set_upstream: bool = False,
    ) -> Tuple[bool, str, str]:
        """Push to remote."""
        args = ["push"]
        if force:
            args.append("--force")
        if set_upstream:
            args.append("-u")
        args.append(remote)
        if branch:
            args.append(branch)
        return self.run(args)

    def fetch(self, remote: str = "origin", prune: bool = False) -> Tuple[bool, str, str]:
        """Fetch from remote."""
        args = ["fetch", remote]
        if prune:
            args.append("--prune")
        return self.run(args)

    def remote(
        self, name: str, url: str | None = None, remove: bool = False
    ) -> Tuple[bool, str, str]:
        """Manage remotes."""
        args = ["remote"]
        if remove:
            args.extend(["remove", name])
        elif url:
            args.extend(["add", name, url])
        else:
            args.append(name)
        return self.run(args)

    def stash(
        self,
        action: str = "push",
        message: str | None = None,
        pop: bool = False,
        apply: bool = False,
        drop: bool = False,
        list_stashes: bool = False,
    ) -> Tuple[bool, str, str]:
        """Manage stashes."""
        args = ["stash"]

        if list_stashes:
            args.append("list")
        elif pop:
            args.append("pop")
        elif apply:
            args.append("apply")
        elif drop:
            args.append("drop")
        else:
            args.append(action if action else "push")

        if message:
            args.extend(["-m", message])

        return self.run(args)

    def tag(
        self, name: str, delete: bool = False, annotated: bool = False, message: str | None = None
    ) -> Tuple[bool, str, str]:
        """Manage tags."""
        args = ["tag"]
        if delete:
            args.append("-d")
        elif annotated:
            args.append("-a")
            if message:
                args.extend(["-m", message])
        args.append(name)
        return self.run(args)

    def reset(self, target: str, mode: str = "hard") -> Tuple[bool, str, str]:
        """Reset current branch."""
        args = ["reset", f"--{mode}", target]
        return self.run(args)

    def revert(self, commit: str, no_edit: bool = False) -> Tuple[bool, str, str]:
        """Revert a commit."""
        args = ["revert", commit]
        if no_edit:
            args.append("--no-edit")
        return self.run(args)

    def cherry_pick(self, commit: str, no_edit: bool = False) -> Tuple[bool, str, str]:
        """Cherry-pick a commit."""
        args = ["cherry-pick", commit]
        if no_edit:
            args.append("--no-edit")
        return self.run(args)

    def bisect(self, action: str, commit: str | None = None) -> Tuple[bool, str, str]:
        """Bisect operations."""
        args = ["bisect", action]
        if commit:
            args.append(commit)
        return self.run(args)

    def log(self, options: List[str] | None = None) -> Tuple[bool, str, str]:
        """Show commit log."""
        args = ["log"]
        if options:
            args.extend(options)
        return self.run(args)

    def show(self, target: str) -> Tuple[bool, str, str]:
        """Show commit/branch/tag details."""
        return self.run(["show", target])

    def diff(self, target: str | None = None, cached: bool = False) -> Tuple[bool, str, str]:
        """Show changes."""
        args = ["diff"]
        if cached:
            args.append("--cached")
        if target:
            args.append(target)
        return self.run(args)

    def status(self, short: bool = True) -> Tuple[bool, str, str]:
        """Show repository status."""
        args = ["status"]
        if short:
            args.append("--porcelain")
        return self.run(args)

    def config(
        self, key: str, value: str | None = None, get: bool = False
    ) -> Tuple[bool, str, str]:
        """Configure git settings."""
        args = ["config"]
        if get:
            args.append("--get")
        args.append(key)
        if value and not get:
            args.append(value)
        return self.run(args)

    def reflog(self, count: int = 10) -> Tuple[bool, str, str]:
        """Show reflog."""
        return self.run(["reflog", f"-{count}"])

    def clean(self, force: bool = False, dry_run: bool = False) -> Tuple[bool, str, str]:
        """Clean untracked files."""
        args = ["clean"]
        if force:
            args.append("-f")
        if dry_run:
            args.append("-n")
        return self.run(args)

    def describe(self, commit: str | None = None, tags: bool = True) -> Tuple[bool, str, str]:
        """Describe a commit."""
        args = ["describe"]
        if tags:
            args.append("--tags")
        if commit:
            args.append(commit)
        return self.run(args)

    def rev_parse(self, target: str) -> Tuple[bool, str, str]:
        """Parse revision."""
        return self.run(["rev-parse", target])

    def rev_list(self, args: List[str]) -> Tuple[bool, str, str]:
        """List revisions."""
        return self.run(["rev-list"] + args)

    def merge_base(self, ref1: str, ref2: str) -> Tuple[bool, str, str]:
        """Find merge base."""
        return self.run(["merge-base", ref1, ref2])

    def ls_files(self, cached: bool = False, deleted: bool = False) -> Tuple[bool, str, str]:
        """List files in index."""
        args = ["ls-files"]
        if cached:
            args.append("--cached")
        if deleted:
            args.append("--deleted")
        return self.run(args)

    def update_ref(self, ref: str, new_value: str) -> Tuple[bool, str, str]:
        """Update a ref."""
        return self.run(["update-ref", ref, new_value])

    def gc(self, prune: str | None = None) -> Tuple[bool, str, str]:
        """Run garbage collection."""
        args = ["gc"]
        if prune:
            args.extend(["--prune", prune])
        return self.run(args)

    def fsck(self, full: bool = False) -> Tuple[bool, str, str]:
        """Verify repository integrity."""
        args = ["fsck"]
        if full:
            args.append("--full")
        return self.run(args)


def run_git_command(repo_path: Path, args: List[str]) -> Tuple[bool, str, str]:
    """
    Convenience function to run a git command.

    Args:
        repo_path: Path to repository
        args: Command arguments

    Returns:
        Tuple of (success, stdout, stderr)
    """
    git = GitCommands(repo_path)
    return git.run(args)
