import unittest
from pathlib import Path

from core.config import Config


class TestConfig(unittest.TestCase):
    def test_default_paths(self) -> None:
        config = Config()
        self.assertEqual(config.HOME_DIR, Path.home() / ".git-quest")
        self.assertEqual(config.WORKSPACE_DIR, config.HOME_DIR / "workspace")
        self.assertEqual(config.DATA_DIR, config.HOME_DIR / "data")

    def test_from_args(self) -> None:
        custom_workspace = "/tmp/workspace"
        custom_data = "/tmp/data"
        config = Config.from_args(workspace=custom_workspace, data_dir=custom_data)
        self.assertEqual(config.WORKSPACE_DIR, Path(custom_workspace))
        self.assertEqual(config.DATA_DIR, Path(custom_data))

    def test_file_properties(self) -> None:
        config = Config()
        self.assertEqual(config.progress_file, config.DATA_DIR / "progress.json")
        self.assertEqual(config.leaderboard_file, config.DATA_DIR / "leaderboard.json")


if __name__ == "__main__":
    unittest.main()
