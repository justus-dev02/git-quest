"""
Git Quest - CLI Application
Main command-line interface modernized with 'rich' library.
"""

import sys
from typing import Any, Dict

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from core.config import Config
from core.game_engine import GameEngine
from core.logger import setup_logger

logger = setup_logger(__name__)
console = Console()


class LevelManager:
    """Handles the modernized flow of a single level."""

    def __init__(self, app: "CLIApp"):
        self.app = app
        self.game_engine = app.game_engine
        self.level_loader = self.game_engine.level_loader
        self.workspace_path = self.game_engine.config.WORKSPACE_DIR

    def load_level(self, level_id: int) -> bool:
        """Load and start a level with visual feedback."""
        with console.status(f"[bold green]Loading Level {level_id}...", spinner="dots"):
            if not self.game_engine.load_level(level_id):
                console.print(f"[bold red]❌ Failed to load level {level_id}!")
                return False

        level_data = self.level_loader.get_level(level_id)
        if not level_data:
            return False

        self._show_level_intro(level_data)
        self._run_level(level_data)
        return True

    def _show_level_intro(self, level_data: Dict[str, Any]) -> None:
        """Display styled level introduction."""
        console.print(
            Panel.fit(
                f"[bold cyan]{level_data['name'].upper()}[/bold cyan]\n\n"
                f"[italic]{level_data['description']}[/italic]\n\n"
                f"[bold white]Story:[/bold white] {level_data.get('story', '')}",
                title=f"Level {level_data['id']}",
                border_style="blue",
            )
        )

        stats_table = Table(show_header=False, box=None)
        stats_table.add_row(
            "[yellow]Difficulty:[/yellow]", level_data.get("difficulty", "beginner").upper()
        )
        stats_table.add_row("[yellow]Base Score:[/yellow]", str(level_data.get("base_score", 1000)))
        stats_table.add_row("[yellow]Par Time:[/yellow]", f"{level_data.get('par_time', 120)}s")
        stats_table.add_row(
            "[yellow]Par Commands:[/yellow]", str(level_data.get("par_commands", 5))
        )

        console.print(stats_table)
        console.print(
            f"\n[bold green]📂 Path:[/bold green] "
            f"{self.workspace_path}/level{level_data['id']:02d}\n"
        )

    def _run_level(self, level_data: Dict[str, Any]) -> None:
        """Run the main level interaction loop."""
        console.print(
            "[dim]Type your git commands directly. Special commands: "
            "status, log, graph, hint, check, quit.[/dim]"
        )

        while True:
            try:
                command = Prompt.ask("\n[bold blue]git-quest[/bold blue]").strip()

                if not command:
                    continue
                if command.lower() == "quit":
                    break

                # Handle special commands
                if command.lower() == "status":
                    self._show_status()
                elif command.lower() == "hint":
                    hint = self.game_engine.use_hint()
                    console.print(f"[bold yellow]💡 Hint:[/bold yellow] {hint}")
                elif command.lower() == "check":
                    result = self.game_engine.check_objective()
                    if result["success"]:
                        console.print(f"[bold green]✅ Success![/bold green] {result['message']}")
                        self._handle_level_complete()
                        break
                    else:
                        console.print(
                            f"[bold red]❌ Not yet complete:[/bold red] {result['message']}"
                        )
                else:
                    # Execute as git command via game_engine
                    cmd_output = self.game_engine.run_player_command(command)
                    console.print(cmd_output)

            except KeyboardInterrupt:
                break

    def _show_status(self) -> None:
        """Show stylized repository status."""
        status = self.game_engine.repo_analyzer.analyze_repo(
            self.workspace_path / f"level{self.game_engine.current_level_id:02d}"
        )
        status_table = Table(title="Repository Status")
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="white")

        for key, value in status.items():
            if key != "recent_commits":
                status_table.add_row(key.replace("_", " ").title(), str(value))

        console.print(status_table)

    def _handle_level_complete(self) -> None:
        """Display score and completion details and offer next level."""
        result = self.game_engine.complete_level()
        console.print(
            Panel(
                f"[bold green]Level '{result['level_name']}' Completed![/bold green]\n\n"
                f"[bold white]Total Score:[/bold white] {result['score']['total']}\n"
                f"[bold white]Rating:[/bold white] "
                f"[bold gold1]{result['score']['rating']}[/bold gold1]",
                border_style="green",
            )
        )

        # Check if there's a next level
        progress = self.game_engine.progress_manager.load_progress()
        next_level = self.game_engine.level_loader.get_next_level(progress["levels_completed"])

        if next_level:
            if (
                Prompt.ask(
                    "\n[bold cyan]Proceed to next level?[/bold cyan]",
                    choices=["y", "n"],
                    default="y",
                )
                == "y"
            ):
                self.load_level(next_level["id"])


class MenuController:
    """Handles modernized main menus and user interaction."""

    def __init__(self, app: "CLIApp"):
        self.app = app
        self.game_engine = app.game_engine

    def main_menu(self) -> None:
        """Display stylized main menu."""
        progress = self.game_engine.progress_manager.load_progress()
        completed = len(progress["levels_completed"])
        total = self.game_engine.level_loader.get_level_count()

        console.print(
            Panel.fit(
                "   [bold cyan]GIT QUEST - LEARN GIT[/bold cyan]   ",
                subtitle=f"[green]{completed}/{total} Levels Completed[/green]",
            )
        )

        menu_table = Table(show_header=False, box=None)
        menu_table.add_row("[1]", "Start New Game")
        menu_table.add_row("[2]", "Continue Progress")
        menu_table.add_row("[3]", "Select Level")
        menu_table.add_row("[4]", "Exit")

        console.print(menu_table)

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])

        if choice == "1":
            self.app.level_manager.load_level(1)
        elif choice == "2":
            next_lvl = self.game_engine.level_loader.get_next_level(progress["levels_completed"])
            if next_lvl:
                self.app.level_manager.load_level(next_lvl["id"])
            else:
                console.print(
                    "[bold yellow]🎉 All levels completed! "
                    "Try selecting a level to replay.[/bold yellow]"
                )
        elif choice == "3":
            self.level_select_menu()
        elif choice == "4":
            self.app.quit()

    def level_select_menu(self) -> None:
        """Display a list of levels for the user to select."""
        progress = self.game_engine.progress_manager.load_progress()
        completed_ids = progress["levels_completed"]
        all_levels = self.game_engine.level_loader.get_all_levels()

        table = Table(title="[bold cyan]Select Level[/bold cyan]")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Difficulty", style="magenta")
        table.add_column("Status", justify="center")

        for level in all_levels:
            status = "[green]✓[/green]" if level["id"] in completed_ids else "[red] [/red]"
            table.add_row(
                str(level["id"]), level["name"], level.get("difficulty", "beginner").upper(), status
            )

        console.print(table)

        level_ids = [str(level["id"]) for level in all_levels] + ["0"]
        choice = Prompt.ask("Enter level ID to start (0 to go back)", choices=level_ids)

        if choice != "0":
            self.app.level_manager.load_level(int(choice))


class CLIApp:
    """Main orchestration class for the CLI application."""

    def __init__(self, config: Config, game_engine: GameEngine):
        self.config = config
        self.game_engine = game_engine
        self.level_manager = LevelManager(self)
        self.menu_controller = MenuController(self)

    def start(self) -> None:
        """Start the application loop."""
        while True:
            self.menu_controller.main_menu()

    def quit(self) -> None:
        """Gracefully shutdown the application."""
        console.print("\n[bold yellow]👋 Shutting down Git Quest. Progress saved.[/bold yellow]")
        self.game_engine.quit()
        sys.exit(0)
