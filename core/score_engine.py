"""
Git Quest - Score Engine
Handles score calculation based on time, commands, and hints.
"""

from typing import Any, Dict, List, Optional

from core.config import Config
from core.logger import setup_logger

logger = setup_logger(__name__)


class ScoreEngine:
    """Engine for calculating player scores."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config if config else Config()
        # Scoring constants from config
        self.TIME_BONUS_PER_SECOND: float = self.config.TIME_BONUS_PER_SECOND
        self.TIME_PENALTY_PER_SECOND: float = self.config.TIME_PENALTY_PER_SECOND
        self.COMMAND_BONUS: int = self.config.COMMAND_BONUS
        self.HINT_PENALTY: int = self.config.HINT_PENALTY
        self.COMPLETION_BONUS: int = self.config.COMPLETION_BONUS

    def calculate_score(
        self,
        base_score: int,
        time_taken: float,
        commands_used: int,
        hints_used: int,
        par_time: Optional[float] = None,
        par_commands: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Calculate the score for a completed level.

        Args:
            base_score: Base score for the level
            time_taken: Time taken in seconds
            commands_used: Number of commands used
            hints_used: Number of hints used
            par_time: Expected par time (optional)
            par_commands: Expected par command count (optional)

        Returns:
            Dict with score breakdown
        """
        if par_time is None:
            par_time = self.config.DEFAULT_PAR_TIME
        if par_commands is None:
            par_commands = self.config.DEFAULT_PAR_COMMANDS

        # Time scoring
        time_score = 0
        if time_taken < par_time:
            time_saved = par_time - time_taken
            time_score = int(time_saved * self.TIME_BONUS_PER_SECOND)
        else:
            time_over = time_taken - par_time
            time_score = -int(time_over * self.TIME_PENALTY_PER_SECOND)

        # Command efficiency scoring
        command_score = 0
        if commands_used <= par_commands:
            command_score = (par_commands - commands_used + 1) * self.COMMAND_BONUS
        else:
            command_score = -(commands_used - par_commands) * self.COMMAND_BONUS

        # Hint penalty
        hint_penalty = hints_used * self.HINT_PENALTY

        # Calculate total
        total = base_score + time_score + command_score - hint_penalty + self.COMPLETION_BONUS
        total = max(0, total)  # Ensure non-negative

        return {
            "base": base_score,
            "time_score": time_score,
            "command_score": command_score,
            "hint_penalty": hint_penalty,
            "completion_bonus": self.COMPLETION_BONUS,
            "total": total,
            "time_taken": time_taken,
            "commands_used": commands_used,
            "hints_used": hints_used,
            "par_time": par_time,
            "par_commands": par_commands,
            "rating": self._get_rating(total, base_score),
        }

    def _get_rating(self, score: int, base_score: int) -> str:
        """Get a rating based on the score."""
        if score >= base_score * 2:
            return "S"  # Superior
        elif score >= base_score * 1.5:
            return "A"  # Excellent
        elif score >= base_score * 1.2:
            return "B"  # Good
        elif score >= base_score:
            return "C"  # Average
        elif score >= base_score * 0.7:
            return "D"  # Below Average
        else:
            return "F"  # Needs Improvement

    def calculate_level_stats(self, scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics across multiple levels.

        Args:
            scores: List of score dicts

        Returns:
            Dict with aggregated stats
        """
        if not scores:
            return {
                "total_score": 0,
                "average_score": 0,
                "best_rating": "N/A",
                "total_time": 0.0,
                "total_commands": 0,
                "total_hints": 0,
            }

        total_score = sum(s["total"] for s in scores)
        total_time = sum(s["time_taken"] for s in scores)
        total_commands = sum(s["commands_used"] for s in scores)
        total_hints = sum(s["hints_used"] for s in scores)

        ratings = [s["rating"] for s in scores]
        rating_order = ["S", "A", "B", "C", "D", "F"]
        best_rating = min(
            ratings, key=lambda r: rating_order.index(r) if r in rating_order else 999
        )

        return {
            "total_score": total_score,
            "average_score": total_score // len(scores),
            "best_rating": best_rating,
            "total_time": total_time,
            "total_commands": total_commands,
            "total_hints": total_hints,
            "levels_completed": len(scores),
        }

    def get_performance_feedback(self, score_data: Dict[str, Any]) -> str:
        """
        Get feedback based on performance.

        Args:
            score_data: Score calculation result

        Returns:
            Feedback string
        """
        rating = score_data.get("rating", "C")
        feedback = []

        if rating == "S":
            feedback.append("🏆 Outstanding! Git master level!")
        elif rating == "A":
            feedback.append("🌟 Excellent work! Almost perfect!")
        elif rating == "B":
            feedback.append("👍 Good job! Keep practicing!")
        elif rating == "C":
            feedback.append("📚 Average performance. Room for improvement!")
        elif rating == "D":
            feedback.append("⚠️ Below average. Try again for better score!")
        else:
            feedback.append("❌ Needs improvement. Review Git basics!")

        # Specific feedback
        if score_data.get("hint_penalty", 0) > 0:
            feedback.append(
                f"💡 Try using fewer hints next time (-{score_data['hint_penalty']} points)"
            )

        if score_data.get("command_score", 0) < 0:
            feedback.append("🔧 Work on using more efficient command sequences")

        if score_data.get("time_score", 0) < 0:
            feedback.append("⏱️ Try to complete levels faster")

        return "\n".join(feedback)
