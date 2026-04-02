"""
Base class for mission objectives.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from core.level_runner import LevelRunner


class Objective(ABC):
    """Abstract base class for mission objectives."""

    @abstractmethod
    def verify(self, runner: LevelRunner, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify if the objective is met.

        Args:
            runner: The LevelRunner instance for executing git commands.
            objective_data: The configuration data for this objective.

        Returns:
            Dict with success (bool) and message (str).
        """
