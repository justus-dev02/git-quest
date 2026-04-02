"""
Git Quest - Mission Engine
Refactored to use the Strategy Pattern for mission objectives.
"""

from pathlib import Path
from typing import Any, Dict

from core.level_runner import LevelRunner
from core.logger import setup_logger

from .objectives.factory import ObjectiveFactory

logger = setup_logger(__name__)


class MissionEngine:
    """Engine for checking mission objectives using Objective Strategy classes."""

    def __init__(self, repo_analyzer: Any):
        """
        Initialize the Mission Engine.

        Args:
            repo_analyzer: The repository analyzer instance.
        """
        self.repo_analyzer: Any = repo_analyzer

    def check_mission(self, repo_path: Path, level_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if mission objectives are met using the appropriate Objective strategy.

        Args:
            repo_path: Path to the repository.
            level_data: Level configuration.

        Returns:
            Dict with success status and message.
        """
        runner = LevelRunner(repo_path)
        objective_config = level_data.get("objective", {})

        if not objective_config:
            return {"success": False, "message": "No objectives defined for this level."}

        objective_type = objective_config.get("type", "")

        # Get the objective strategy from the factory
        strategy = ObjectiveFactory.get_objective(objective_type)

        if strategy:
            return strategy.verify(runner, objective_config)
        else:
            logger.error(f"Unsupported objective type: {objective_type}")
            return {
                "success": False,
                "message": f"Verification for objective type '{objective_type}' is not yet implemented.",
            }
