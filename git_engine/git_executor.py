"""
Centralized Git Command Execution.
Ensures consistent logging, error handling and environment validation.
"""

import shlex
import subprocess
from pathlib import Path
from typing import List

from core.exceptions import GitCommandError
from core.logger import setup_logger

logger = setup_logger(__name__)


class GitExecutor:
    """Handles execution of git commands with robust error reporting."""

    def __init__(self) -> None:
        """Initialize and check git environment."""
        self._check_git_version()

    def _check_git_version(self) -> None:
        """Verify git is installed and log the version."""
        try:
            result = subprocess.run(
                ["git", "--version"], capture_output=True, text=True, check=True
            )
            logger.info(f"Git environment confirmed: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.critical("Git is not installed or not in the system path!")
            raise GitCommandError("Git environment check failed.", stderr=str(e))

    def run(
        self, args: List[str], cwd: Path | str, capture: bool = True
    ) -> subprocess.CompletedProcess[str]:
        """
        Run a git command.

        Args:
            args: The git command arguments (excluding 'git' prefix).
            cwd: Working directory to run the command in.
            capture: Whether to capture stdout and stderr.

        Returns:
            The CompletedProcess result.

        Raises:
            GitCommandError: If the command returns a non-zero exit code.
        """
        full_command = ["git"] + args
        # Use shlex.join for safer logging of the command
        cmd_str = " ".join(shlex.quote(arg) for arg in full_command)
        logger.debug(f"Executing: {cmd_str} in {cwd}")

        try:
            result = subprocess.run(
                full_command,
                cwd=cwd,
                capture_output=capture,
                text=True,
                check=False,  # We handle return codes manually for better context
            )

            if result.returncode != 0:
                logger.error(f"Git command failed: {cmd_str}")
                logger.error(f"Stderr: {result.stderr}")
                raise GitCommandError(
                    f"Git command failed with exit code {result.returncode}",
                    stdout=result.stdout,
                    stderr=result.stderr,
                )

            return result
        except GitCommandError:
            raise
        except Exception as e:
            logger.exception(f"Unexpected error executing git command: {e}")
            raise GitCommandError(f"Unexpected error: {str(e)}")
