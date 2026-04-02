"""
Git Quest - Utility Modules
Filesystem and timer utilities.
"""

import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from core.logger import setup_logger

logger = setup_logger(__name__)


class FileSystemUtils:
    """Filesystem utility functions."""

    @staticmethod
    def ensure_directory(path: Path) -> bool:
        """
        Ensure a directory exists.

        Args:
            path: Directory path

        Returns:
            True if directory exists or was created
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            return False

    @staticmethod
    def clear_directory(path: Path, exclude: list[str] | None = None) -> bool:
        """
        Clear all contents of a directory.

        Args:
            path: Directory to clear
            exclude: List of filenames to exclude from deletion

        Returns:
            True if successful
        """
        if not path.exists():
            return True

        exclude_list = exclude or []

        try:
            for item in path.iterdir():
                if item.name not in exclude_list:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            return True
        except Exception as e:
            logger.error(f"Error clearing directory {path}: {e}")
            return False

    @staticmethod
    def copy_directory(src: Path, dst: Path) -> bool:
        """
        Copy a directory recursively.

        Args:
            src: Source directory
            dst: Destination directory

        Returns:
            True if successful
        """
        try:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            return True
        except Exception as e:
            print(f"Error copying directory: {e}")
            return False

    @staticmethod
    def get_directory_size(path: Path) -> int:
        """
        Get total size of a directory.

        Args:
            path: Directory path

        Returns:
            Size in bytes
        """
        total = 0
        if not path.exists():
            return 0

        try:
            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
        except Exception:
            pass

        return total

    @staticmethod
    def count_files(path: Path, pattern: str = "*") -> int:
        """
        Count files matching a pattern.

        Args:
            path: Directory to search
            pattern: Glob pattern

        Returns:
            Number of matching files
        """
        if not path.exists():
            return 0

        return len(list(path.glob(pattern)))

    @staticmethod
    def is_git_repo(path: Path) -> bool:
        """
        Check if a path is a Git repository.

        Args:
            path: Path to check

        Returns:
            True if Git repository
        """
        return (path / ".git").exists()

    @staticmethod
    def get_file_extension(path: Path) -> str:
        """
        Get file extension.

        Args:
            path: File path

        Returns:
            Extension (e.g., '.txt')
        """
        return path.suffix.lower()

    @staticmethod
    def create_temp_directory(prefix: str = "gitquest_") -> Optional[Path]:
        """
        Create a temporary directory.

        Args:
            prefix: Directory name prefix

        Returns:
            Path to temp directory or None
        """
        import tempfile

        try:
            temp_dir = tempfile.mkdtemp(prefix=prefix)
            return Path(temp_dir)
        except Exception as e:
            print(f"Error creating temp directory: {e}")
            return None

    @staticmethod
    def cleanup_temp_directory(path: Path) -> bool:
        """
        Clean up a temporary directory.

        Args:
            path: Directory to clean up

        Returns:
            True if successful
        """
        try:
            if path.exists() and "gitquest" in str(path):
                shutil.rmtree(path)
                return True
            return False
        except Exception as e:
            print(f"Error cleaning up temp directory: {e}")
            return False

    @staticmethod
    def write_file(path: Path, content: str) -> bool:
        """
        Write content to a file.

        Args:
            path: File path
            content: Content to write

        Returns:
            True if successful
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return True
        except Exception as e:
            print(f"Error writing file {path}: {e}")
            return False

    @staticmethod
    def read_file(path: Path) -> Optional[str]:
        """
        Read content from a file.

        Args:
            path: File path

        Returns:
            File content or None
        """
        try:
            if path.exists():
                return path.read_text()
            return None
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return None

    @staticmethod
    def file_exists(path: Path) -> bool:
        """Check if a file exists."""
        return path.exists() and path.is_file()

    @staticmethod
    def directory_exists(path: Path) -> bool:
        """Check if a directory exists."""
        return path.exists() and path.is_dir()


class Timer:
    """Timer utility for tracking elapsed time."""

    def __init__(self) -> None:
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._total_paused_time: float = 0.0
        self._is_paused: bool = False

    def start(self) -> None:
        """Start the timer."""
        self._start_time = time.time()
        self._pause_time = None
        self._total_paused_time = 0.0
        self._is_paused = False

    def stop(self) -> float:
        """
        Stop the timer.

        Returns:
            Elapsed time in seconds
        """
        if self._start_time is None:
            return 0.0

        elapsed = time.time() - self._start_time - self._total_paused_time
        self._start_time = None
        self._pause_time = None
        self._total_paused_time = 0.0
        self._is_paused = False

        return elapsed

    def pause(self) -> None:
        """Pause the timer."""
        if self._start_time is not None and not self._is_paused:
            self._pause_time = time.time()
            self._is_paused = True

    def resume(self) -> None:
        """Resume the timer."""
        if self._pause_time is not None and self._is_paused:
            paused_duration = time.time() - self._pause_time
            self._total_paused_time += paused_duration
            self._pause_time = None
            self._is_paused = False

    def elapsed(self) -> float:
        """
        Get elapsed time.

        Returns:
            Elapsed time in seconds
        """
        if self._start_time is None:
            return 0.0

        if self._is_paused and self._pause_time is not None:
            return self._pause_time - self._start_time - self._total_paused_time

        return time.time() - self._start_time - self._total_paused_time

    def elapsed_formatted(self) -> str:
        """
        Get formatted elapsed time.

        Returns:
            Formatted time string (e.g., "2m 30s")
        """
        elapsed = self.elapsed()
        return Timer.format_time(elapsed)

    @staticmethod
    def format_time(seconds: float) -> str:
        """
        Format seconds into human-readable string.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted string
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours}h {minutes}m {secs}s"

    @staticmethod
    def format_time_detailed(seconds: float) -> str:
        """
        Format seconds with milliseconds.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted string with milliseconds
        """
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        ms = int((seconds * 1000) % 1000)
        return f"{mins:02d}:{secs:02d}.{ms:03d}"


class Stopwatch:
    """Simple stopwatch for timing operations."""

    def __init__(self) -> None:
        self._start: Optional[float] = None
        self._end: Optional[float] = None

    def __enter__(self) -> "Stopwatch":
        self._start = time.time()
        return self

    def __exit__(self, *args: Any) -> None:
        self._end = time.time()

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self._start is None:
            return 0.0
        end = self._end if self._end else time.time()
        return end - self._start


class ProgressTracker:
    """Tracks progress through levels."""

    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self.progress_file = data_path / "progress.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists."""
        self.data_path.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """Load progress from file."""
        import json

        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r") as f:
                    from typing import cast
                return cast(Dict[str, Any], json.load(f))
            except Exception as e:
                print(f"Error loading progress: {e}")

        default_progress: Dict[str, Any] = {
            "levels_completed": [],
            "levels_attempted": [],
            "total_score": 0,
            "hints_used": 0,
            "start_date": datetime.now().isoformat(),
        }
        return default_progress

    def save(self, progress: Dict[str, Any]) -> bool:
        """Save progress to file."""
        import json

        try:
            with open(self.progress_file, "w") as f:
                json.dump(progress, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False

    def mark_complete(self, level_id: int, score: int) -> Dict[str, Any]:
        """
        Mark a level as complete.

        Args:
            level_id: Level ID
            score: Score achieved

        Returns:
            Updated progress
        """
        progress = self.load()

        if level_id not in progress["levels_completed"]:
            progress["levels_completed"].append(level_id)

        if level_id not in progress["levels_attempted"]:
            progress["levels_attempted"].append(level_id)

        progress["total_score"] += score

        return progress

    def get_completion_percentage(self, total_levels: int = 50) -> float:
        """Get completion percentage."""
        progress = self.load()
        completed = len(progress.get("levels_completed", []))
        return (completed / total_levels) * 100


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes = int(size_bytes / 1024.0)
    return f"{size_bytes:.1f} PB"
