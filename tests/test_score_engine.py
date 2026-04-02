import unittest

from core.config import Config
from core.score_engine import ScoreEngine


class TestScoreEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()
        self.score_engine = ScoreEngine(self.config)

    def test_calculate_score_perfect(self) -> None:
        base_score = 1000
        time_taken = 60.0
        commands_used = 2
        hints_used = 0
        par_time = 120.0
        par_commands = 5

        result = self.score_engine.calculate_score(
            base_score, time_taken, commands_used, hints_used, par_time, par_commands
        )

        # time_score = (120 - 60) * 0.5 = 30
        # command_score = (5 - 2 + 1) * 10 = 40
        # hint_penalty = 0
        # total = 1000 + 30 + 40 - 0 + 200 = 1270
        self.assertEqual(result["total"], 1270)
        self.assertEqual(result["rating"], "B")  # 1270 >= 1000 * 1.2

    def test_calculate_score_with_penalties(self) -> None:
        base_score = 1000
        time_taken = 180.0
        commands_used = 10
        hints_used = 2
        par_time = 120.0
        par_commands = 5

        result = self.score_engine.calculate_score(
            base_score, time_taken, commands_used, hints_used, par_time, par_commands
        )

        # time_score = -(180 - 120) * 0.2 = -12
        # command_score = -(10 - 5) * 10 = -50
        # hint_penalty = 2 * 50 = 100
        # total = 1000 - 12 - 50 - 100 + 200 = 1038
        self.assertEqual(result["total"], 1038)
        self.assertEqual(result["rating"], "C")  # 1038 >= 1000

    def test_calculate_stats(self) -> None:
        scores = [
            {"total": 1000, "time_taken": 60, "commands_used": 5, "hints_used": 0, "rating": "C"},
            {"total": 1500, "time_taken": 30, "commands_used": 2, "hints_used": 0, "rating": "A"},
        ]
        stats = self.score_engine.calculate_level_stats(scores)
        self.assertEqual(stats["total_score"], 2500)
        self.assertEqual(stats["average_score"], 1250)
        self.assertEqual(stats["best_rating"], "A")
        self.assertEqual(stats["levels_completed"], 2)


if __name__ == "__main__":
    unittest.main()
