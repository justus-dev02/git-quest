"""
Git Quest - Level Loader
Loads and manages level definitions from external JSON files.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.logger import setup_logger

logger = setup_logger(__name__)


class LevelLoader:
    """Loads level definitions from JSON files."""

    def __init__(self, levels_dir: Path) -> None:
        """
        Initialize the level loader.

        Args:
            levels_dir: Root directory for levels.
        """
        self.levels_dir = levels_dir / "levels"
        self.levels: Dict[int, Dict[str, Any]] = {}
        self._load_all_levels()

    def _load_all_levels(self) -> None:
        """Load all level definitions from the levels directory."""
        if not self.levels_dir.exists():
            logger.error(f"Levels directory not found: {self.levels_dir}")
            return

        for json_file in sorted(self.levels_dir.glob("level*.json")):
            try:
                with open(json_file, "r") as f:
                    level_data = json.load(f)
                    level_id = level_data.get("id", 0)
                    if level_id > 0:
                        self.levels[level_id] = level_data
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}", exc_info=True)

        if not self.levels:
            logger.warning("No levels loaded from the levels directory.")
        else:
            logger.info(f"Successfully loaded {len(self.levels)} levels.")

    def get_level(self, level_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific level definition.

        Args:
            level_id: The ID of the level to retrieve.

        Returns:
            The level data dictionary or None if not found.
        """
        return self.levels.get(level_id)

    def get_all_levels(self) -> List[Dict[str, Any]]:
        """
        Get all available level definitions sorted by ID.

        Returns:
            A list of level data dictionaries.
        """
        return [self.levels[level_id] for level_id in sorted(self.levels.keys())]

    def get_level_count(self) -> int:
        """
        Get the total number of available levels.

        Returns:
            The number of levels.
        """
        return len(self.levels)

    def get_next_level(self, completed_ids: List[int]) -> Optional[Dict[str, Any]]:
        """
        Find the next uncompleted level.

        Args:
            completed_ids: List of IDs of already completed levels.

        Returns:
            The next level data or None if all levels are completed.
        """
        for level_id in sorted(self.levels.keys()):
            if level_id not in completed_ids:
                return self.levels[level_id]
        return None
