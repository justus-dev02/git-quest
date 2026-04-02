"""
Git Quest - Game Engine
Orchestrates level lifecycle and repository state.
Updated to include LevelSetupService and player command execution.
"""

import shlex
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.config import Config
from core.level_setup_service import LevelSetupService
from core.logger import setup_logger
from core.mission_engine import MissionEngine
from core.progress_manager import ProgressManager
from core.score_engine import ScoreEngine
from git_engine.repo_analyzer import RepoAnalyzer
from git_engine.repo_manager import RepoManager
from level_definitions.level_loader import LevelLoader

logger = setup_logger(__name__)


class GameEngine:
    """Core game engine coordinating all level and repository services."""

    def __init__(
        self,
        config: Config,
        level_loader: LevelLoader,
        repo_manager: RepoManager,
        repo_analyzer: RepoAnalyzer,
        mission_engine: MissionEngine,
        score_engine: ScoreEngine,
        progress_manager: ProgressManager,
        setup_service: LevelSetupService,
    ):
        self.config = config
        self.level_loader = level_loader
        self.repo_manager = repo_manager
        self.repo_analyzer = repo_analyzer
        self.mission_engine = mission_engine
        self.score_engine = score_engine
        self.progress_manager = progress_manager
        self.setup_service = setup_service

        self.current_level_id: Optional[int] = None
        self.current_level: Optional[Dict[str, Any]] = None
        self.level_start_time: Optional[datetime] = None
        self.level_commands: List[str] = []
        self.level_hints_used: int = 0
        self.is_level_completed: bool = False

    def load_level(self, level_id: int) -> bool:
        """Prepare a specific level's environment."""
        level_data = self.level_loader.get_level(level_id)
        if not level_data:
            return False

        self.current_level_id = level_id
        self.current_level = level_data
        self.level_start_time = datetime.now()
        self.level_commands = []
        self.level_hints_used = 0
        self.is_level_completed = False

        level_path = self.config.WORKSPACE_DIR / f"level{level_id:02d}"

        # 1. Clean and init repo
        if not self.repo_manager.init_repo(level_path):
            return False

        # 2. Setup initial state via service
        if not self.setup_service.setup_level(level_path, level_data):
            return False

        # 3. Create initial snapshot (only if not empty to avoid git bundle error)
        try:
            self.repo_manager.create_snapshot(level_path, f"level{level_id:02d}_start")
        except Exception:
            logger.warning(
                f"Could not create initial snapshot for level {level_id} (possibly empty repo)."
            )

        return True

    def run_player_command(self, command_str: str) -> str:
        """Execute a git command from the player and record it."""
        if not self.current_level_id:
            return "No level active."

        level_path = self.config.WORKSPACE_DIR / f"level{self.current_level_id:02d}"

        # Split command correctly using shlex
        try:
            args = shlex.split(command_str)
        except ValueError as e:
            return f"Error parsing command: {e}"

        if args and args[0].lower() == "git":
            args = args[1:]

        try:
            self.record_command(command_str)
            result = self.repo_manager.git_executor.run(args, cwd=level_path)
            return result.stdout if result.stdout else "Success."
        except Exception as e:
            return str(e)

    def check_objective(self) -> Dict[str, Any]:
        """Check if mission objectives are met."""
        if not self.current_level_id or not self.current_level:
            return {"success": False, "message": "No level loaded."}

        level_path = self.config.WORKSPACE_DIR / f"level{self.current_level_id:02d}"
        result = self.mission_engine.check_mission(level_path, self.current_level)

        if result["success"]:
            self.is_level_completed = True

        return result

    def record_command(self, command: str) -> None:
        """Log a command executed by the player."""
        self.level_commands.append(command)

    def use_hint(self) -> str:
        """Get the next hint for the current level."""
        self.level_hints_used += 1
        hints = self.current_level.get("hints", []) if self.current_level else []
        if self.level_hints_used <= len(hints):
            return str(hints[self.level_hints_used - 1])
        return "No more hints available!"

    def complete_level(self) -> Dict[str, Any]:
        """Finalize level and persist progress."""
        if not self.is_level_completed or not self.current_level_id or not self.current_level:
            return {"error": "Level objectives not met."}

        end_time = datetime.now()
        time_taken = (
            (end_time - self.level_start_time).total_seconds() if self.level_start_time else 0.0
        )

        score_result = self.score_engine.calculate_score(
            self.current_level.get("base_score", 1000),
            time_taken,
            len(self.level_commands),
            self.level_hints_used,
            self.current_level.get("par_time", 300),
            self.current_level.get("par_commands", 10),
        )

        progress = self.progress_manager.load_progress()
        if self.current_level_id not in progress["levels_completed"]:
            progress["levels_completed"].append(self.current_level_id)
            progress["total_score"] += score_result["total"]
            self.progress_manager.save_progress(progress)

        self.repo_manager.cleanup_snapshots()
        return {
            "level_id": self.current_level_id,
            "level_name": self.current_level["name"],
            "score": score_result,
            "commands_used": len(self.level_commands),
            "hints_used": self.level_hints_used,
        }

    def quit(self) -> None:
        """Cleanup and shutdown."""
        self.repo_manager.cleanup_snapshots()
        logger.info("Game engine shut down.")
