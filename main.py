"""
Git Quest - Main Entry Point
Uses Dependency Injection to wire up the system.
"""

import argparse
import sys
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
from ui.cli_app import CLIApp
from utils.filesystem import FileSystemUtils


def main() -> None:
    """Wire up dependencies and start the application."""
    parser = argparse.ArgumentParser(description="🎮 Git Quest - Final Senior Edition")
    parser.add_argument("--workspace", type=str, help="Custom workspace directory")
    parser.add_argument("--data-dir", type=str, help="Custom data directory")
    args = parser.parse_args()

    # 1. Initialize Infrastructure & Config
    config = Config.from_args(workspace=args.workspace, data_dir=args.data_dir)
    FileSystemUtils.ensure_directory(config.WORKSPACE_DIR)
    FileSystemUtils.ensure_directory(config.DATA_DIR)

    # 2. Wire up Git Engine
    git_executor = GitExecutor()
    repo_manager = RepoManager(config.WORKSPACE_DIR, git_executor)
    repo_analyzer = RepoAnalyzer()

    # 3. Wire up Core Services
    level_loader = LevelLoader(Path(__file__).parent / "level_definitions")
    score_engine = ScoreEngine(config)
    mission_engine = MissionEngine(repo_analyzer)
    progress_manager = ProgressManager(config.DATA_DIR)
    setup_service = LevelSetupService(git_executor)

    # 4. Initialize Game Engine via Dependency Injection
    game_engine = GameEngine(
        config=config,
        level_loader=level_loader,
        repo_manager=repo_manager,
        repo_analyzer=repo_analyzer,
        mission_engine=mission_engine,
        score_engine=score_engine,
        progress_manager=progress_manager,
        setup_service=setup_service,
    )

    # 5. Start CLI Application
    app = CLIApp(config=config, game_engine=game_engine)

    try:
        app.start()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing Git Quest!")
        game_engine.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
