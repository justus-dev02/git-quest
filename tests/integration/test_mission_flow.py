"""
Integration tests for Git Quest mission flow.
Uses real git repositories and filesystem operations.
"""

import shutil
import unittest
from pathlib import Path

from core.config import Config
from core.game_engine import GameEngine
from core.level_setup_service import LevelSetupService
from core.mission_engine import MissionEngine
from core.progress_manager import ProgressManager
from core.score_engine import ScoreEngine
from git_engine.git_executor import GitExecutor
from git_engine.repo_analyzer import RepoAnalyzer
from git_engine.repo_manager import RepoManager
from level_definitions.level_loader import LevelLoader


class TestMissionFlow(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = Path("./test_env").absolute()
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

        self.workspace = self.test_dir / "workspace"
        self.data_dir = self.test_dir / "data"

        self.config = Config.from_args(workspace=str(self.workspace), data_dir=str(self.data_dir))

        self.git_executor = GitExecutor()
        self.repo_manager = RepoManager(self.config.WORKSPACE_DIR, self.git_executor)
        self.repo_analyzer = RepoAnalyzer()
        self.level_loader = LevelLoader(Path(__file__).parent.parent.parent / "level_definitions")
        self.score_engine = ScoreEngine(self.config)
        self.mission_engine = MissionEngine(self.repo_analyzer)
        self.progress_manager = ProgressManager(self.config.DATA_DIR)
        self.setup_service = LevelSetupService(self.git_executor)

        self.game_engine = GameEngine(
            config=self.config,
            level_loader=self.level_loader,
            repo_manager=self.repo_manager,
            repo_analyzer=self.repo_analyzer,
            mission_engine=self.mission_engine,
            score_engine=self.score_engine,
            progress_manager=self.progress_manager,
            setup_service=self.setup_service,
        )

    def tearDown(self) -> None:
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_level_01_completion_flow(self) -> None:
        """Test the full flow of completing the first level."""
        # 1. Load Level 1
        success = self.game_engine.load_level(1)
        self.assertTrue(success)

        # 2. Check initial objective (should fail)
        status = self.game_engine.check_objective()
        self.assertFalse(status["success"])

        # 3. Perform the required git actions
        # Level 1 usually requires an initial commit
        self.game_engine.run_player_command("git add README.md")
        self.game_engine.run_player_command("git commit -m 'initial commit'")

        # 4. Check objective again (should succeed)
        status = self.game_engine.check_objective()
        self.assertTrue(status["success"], f"Objective failed: {status.get('message')}")

        # 5. Complete level
        completion = self.game_engine.complete_level()
        self.assertEqual(completion["level_id"], 1)
        self.assertIn("score", completion)

        # 6. Verify progress saved
        progress = self.progress_manager.load_progress()
        self.assertIn(1, progress["levels_completed"])

    def test_level_snapshot_restoration(self) -> None:
        """Test that snapshots are created and can be restored (indirectly via cleanup)."""
        self.game_engine.load_level(1)
        level_path = self.workspace / "level01"
        self.assertTrue((self.workspace / ".snapshots" / "level01_start.bundle").exists())

        # Corrupt the repo
        shutil.rmtree(level_path / ".git")

        # Restore via reload
        self.game_engine.load_level(1)
        self.assertTrue((level_path / ".git").exists())


if __name__ == "__main__":
    unittest.main()
