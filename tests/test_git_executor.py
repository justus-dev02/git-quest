import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.exceptions import GitCommandError
from git_engine.git_executor import GitExecutor


@patch("subprocess.run")
def test_check_git_version_success(mock_run: MagicMock) -> None:
    # Setup mock to return a valid result
    mock_result = MagicMock()
    mock_result.stdout = "git version 2.39.3"
    mock_run.return_value = mock_result

    # If this raises an exception, the test will fail
    executor = GitExecutor()
    mock_run.assert_called_once_with(["git", "--version"], capture_output=True, text=True, check=True)


@patch("subprocess.run")
def test_check_git_version_failure(mock_run: MagicMock) -> None:
    # Setup mock to raise CalledProcessError
    mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "--version"])

    with pytest.raises(GitCommandError) as exc_info:
        GitExecutor()

    assert "Git environment check failed" in str(exc_info.value)


@patch("subprocess.run")
def test_git_executor_run_success(mock_run: MagicMock, tmp_path: Path) -> None:
    # First call is for __init__ check_git_version
    mock_version_result = MagicMock(stdout="git version 2.0.0")
    
    # Second call is for run()
    mock_run_result = MagicMock()
    mock_run_result.returncode = 0
    mock_run_result.stdout = "On branch main"
    mock_run_result.stderr = ""
    
    mock_run.side_effect = [mock_version_result, mock_run_result]

    executor = GitExecutor()
    result = executor.run(["status"], cwd=tmp_path)

    assert result.returncode == 0
    assert result.stdout == "On branch main"
    
    # Assert subprocess.run was called correctly for the command
    mock_run.assert_called_with(
        ["git", "status"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False
    )


@patch("subprocess.run")
def test_git_executor_run_failure(mock_run: MagicMock, tmp_path: Path) -> None:
    # Setup mock for __init__
    mock_version_result = MagicMock(stdout="git version 2.0.0")
    
    # Setup mock for run() failure
    mock_run_result = MagicMock()
    mock_run_result.returncode = 128
    mock_run_result.stdout = ""
    mock_run_result.stderr = "fatal: not a git repository"
    
    mock_run.side_effect = [mock_version_result, mock_run_result]

    executor = GitExecutor()
    
    with pytest.raises(GitCommandError) as exc_info:
        executor.run(["status"], cwd=tmp_path)

    assert "Git command failed with exit code 128" in str(exc_info.value)
    assert exc_info.value.stderr == "fatal: not a git repository"


@patch("subprocess.run")
def test_git_executor_run_unexpected_exception(mock_run: MagicMock, tmp_path: Path) -> None:
    mock_version_result = MagicMock(stdout="git version 2.0.0")
    mock_run.side_effect = [mock_version_result, ValueError("Unexpected system error")]

    executor = GitExecutor()
    
    with pytest.raises(GitCommandError) as exc_info:
        executor.run(["status"], cwd=tmp_path)

    assert "Unexpected error" in str(exc_info.value)
