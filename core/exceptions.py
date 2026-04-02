class GitQuestError(Exception):
    """Base class for all Git Quest exceptions."""



class RepoNotFoundError(GitQuestError):
    """Raised when a repository is not found."""



class ObjectiveNotMetError(GitQuestError):
    """Raised when a level objective is not completed."""



class GitCommandError(GitQuestError):
    """Raised when a Git command fails."""

    def __init__(
        self,
        message: str,
        stdout: str | None = None,
        stderr: str | None = None,
        command: str | None = None,
    ) -> None:
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr
        self.command = command


class ConfigurationError(GitQuestError):
    """Raised when there is a configuration issue."""

