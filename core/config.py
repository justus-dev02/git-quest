from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Game configuration and constants."""

    # Paths
    HOME_DIR: Path = Path.home() / ".git-quest"
    WORKSPACE_DIR: Path = HOME_DIR / "workspace"
    DATA_DIR: Path = HOME_DIR / "data"
    LEVELS_DIR: Path = Path(__file__).parent.parent / "level_definitions"

    PROGRESS_FILE_NAME: str = "progress.json"
    LEADERBOARD_FILE_NAME: str = "leaderboard.json"

    @property
    def progress_file(self) -> Path:
        return self.DATA_DIR / self.PROGRESS_FILE_NAME

    @property
    def leaderboard_file(self) -> Path:
        return self.DATA_DIR / self.LEADERBOARD_FILE_NAME

    # Scoring Constants
    TIME_BONUS_PER_SECOND: float = 0.5
    TIME_PENALTY_PER_SECOND: float = 0.2
    COMMAND_BONUS: int = 10
    HINT_PENALTY: int = 50
    COMPLETION_BONUS: int = 200
    DEFAULT_BASE_SCORE: int = 1000

    # Level Defaults
    DEFAULT_PAR_TIME: float = 120.0
    DEFAULT_PAR_COMMANDS: int = 5

    # Git Defaults
    DEFAULT_PLAYER_EMAIL: str = "player@game.local"
    DEFAULT_PLAYER_NAME: str = "Player"

    @classmethod
    def from_args(cls, workspace: str | None = None, data_dir: str | None = None) -> "Config":
        """Create a config instance from command line arguments."""
        config = cls()
        if workspace:
            config.WORKSPACE_DIR = Path(workspace)
        if data_dir:
            config.DATA_DIR = Path(data_dir)
        return config
