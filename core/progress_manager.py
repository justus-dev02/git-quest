"""
Git Quest - Progress Manager
Handles player progress, scores and leaderboard persistence.
Separates concerns from the main GameEngine.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from core.logger import setup_logger

logger = setup_logger(__name__)


class ProgressManager:
    """Manages player progress and leaderboard data."""

    def __init__(self, data_path: Path):
        """
        Initialize the progress manager.

        Args:
            data_path: Directory to store progress files.
        """
        self.data_path = data_path
        self.progress_file = data_path / "progress.json"
        self.leaderboard_file = data_path / "leaderboard.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists."""
        self.data_path.mkdir(parents=True, exist_ok=True)

    def load_progress(self) -> Dict[str, Any]:
        """Load player progress from file with migration support."""
        if not self.progress_file.exists():
            return self._init_new_progress()

        try:
            with open(self.progress_file, "r") as f:
                from typing import cast

                data = cast(Dict[str, Any], json.load(f))

                # Check for version and migrate if needed
                if "version" not in data:
                    data = self._migrate_to_v1(data)
                    self.save_progress(data)

                return data
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load progress file: {e}")
            return self._init_new_progress()

    def _init_new_progress(self) -> Dict[str, Any]:
        """Initialize empty progress data."""
        return {
            "version": 1,
            "levels_completed": [],
            "total_score": 0,
            "levels_attempted": [],
            "hints_used": 0,
            "start_date": datetime.now().isoformat(),
        }

    def _migrate_to_v1(self, old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate legacy progress data to version 1."""
        logger.info("Migrating legacy progress to version 1.")
        new_data = self._init_new_progress()
        new_data["levels_completed"] = old_data.get("levels_completed", [])
        new_data["total_score"] = old_data.get("total_score", 0)
        return new_data

    def save_progress(self, progress: Dict[str, Any]) -> bool:
        """Save player progress to file."""
        try:
            with open(self.progress_file, "w") as f:
                json.dump(progress, f, indent=2)
            return True
        except OSError as e:
            logger.error(f"Failed to save progress: {e}")
            return False

    def load_leaderboard(self) -> List[Dict[str, Any]]:
        """Load leaderboard from file."""
        if not self.leaderboard_file.exists():
            return []

        try:
            with open(self.leaderboard_file, "r") as f:
                from typing import cast

                return cast(List[Dict[str, Any]], json.load(f))
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load leaderboard: {e}")
            return []

    def save_leaderboard(self, leaderboard: List[Dict[str, Any]]) -> bool:
        """Save leaderboard to file."""
        try:
            with open(self.leaderboard_file, "w") as f:
                json.dump(leaderboard, f, indent=2)
            return True
        except OSError as e:
            logger.error(f"Failed to save leaderboard: {e}")
            return False


False
