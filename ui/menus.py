"""
Git Quest - Menu System
Handles all menu displays and user input.
"""

from typing import Any, Dict, List


class MenuSystem:
    """Menu system for the CLI application."""

    def __init__(self) -> None:
        self.box_art = {
            "title": """
 ╔═══════════════════════════════════════════════════════╗
 ║                                                       ║
 ║   ██████╗  ██████╗  ██████╗ ██╗  ██╗███████╗██████╗   ║
 ║   ██╔════╝ ██╔═══██╗██╔════╝ ██║  ██║██╔════╝██╔══██╗  ║
 ║   ███████╗ ██║   ██║██║  ███╗███████║█████╗  ██████╔╝  ║
 ║   ╚════██║ ██║   ██║██║   ██║╚════██║██╔══╝  ██╔══██╗  ║
 ║   ███████║ ╚██████╔╝╚██████╔╝     ██║███████╗██║  ██║  ║
 ║   ╚══════╝  ╚═════╝  ╚═════╝      ╚═╝╚══════╝╚═╝  ╚═╝  ║
 ║                                                       ║
 ║              Q  U  E  S  T                            ║
 ║                                                       ║
 ║         Learn Git Through Interactive Challenges      ║
 ║                                                       ║
 ╚═══════════════════════════════════════════════════════╝
""",
            "level_complete": """
 ╔═══════════════════════════════════════════════════════╗
 ║                                                       ║
 ║                    ✓ COMPLETE!                        ║
 ║                                                       ║
 ╚═══════════════════════════════════════════════════════╝
""",
            "game_over": """
 ╔═══════════════════════════════════════════════════════╗
 ║                                                       ║
 ║                      GAME OVER                        ║
 ║                                                       ║
 ╚═══════════════════════════════════════════════════════╝
""",
        }

    def show_main_menu(self) -> str:
        """
        Display the main menu and get user choice.

        Returns:
            User's choice
        """
        print("""
╔═══════════════════════════════════════════════════════╗
║                    MAIN MENU                          ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║   1. 🆕  New Game                                     ║
║   2. ▶️   Continue                                    ║
║   3. 📁  Level Select                                 ║
║   4. 🏆  Leaderboard                                  ║
║   5. ❓  Help                                         ║
║   6. 🚪  Quit                                         ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
""")
        return input("Enter choice (1-6): ").strip()

    def show_level_menu(self, levels: List[Dict[str, Any]], completed: List[int]) -> int:
        """
        Display level selection menu.

        Args:
            levels: List of level definitions
            completed: List of completed level IDs

        Returns:
            Selected level ID or 0 to go back
        """
        print("\n" + "=" * 60)
        print("📁 LEVEL SELECT")
        print("=" * 60)

        # Group by difficulty
        difficulties = ["beginner", "intermediate", "advanced", "expert"]

        for diff in difficulties:
            diff_levels = [l for l in levels if l.get("difficulty") == diff]
            if diff_levels:
                print(f"\n{diff.upper()}:")
                for level in diff_levels:
                    status = "✓" if level["id"] in completed else " "
                    print(f"  [{status}] {level['id']:2d}. {level['name']}")

        print("\n  0. Back")

        try:
            choice = int(input("\nSelect level: ").strip())
            return choice
        except ValueError:
            return 0

    def show_pause_menu(self) -> str:
        """
        Display pause menu.

        Returns:
            User's choice
        """
        print("""
╔═══════════════════════════════════════════════════════╗
║                    PAUSE MENU                         ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║   1. 📝  Resume                                       ║
║   2. 💡  Get Hint                                     ║
║   3. 🔄  Reset Level                                  ║
║   4. 📊  View Status                                  ║
║   5. 📈  View Graph                                   ║
║   6. 🚪  Quit to Menu                                 ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
""")
        return input("Enter choice (1-6): ").strip()

    def show_difficulty_select(self) -> str:
        """
        Display difficulty selection.

        Returns:
            Selected difficulty
        """
        print("""
╔═══════════════════════════════════════════════════════╗
║                 SELECT DIFFICULTY                     ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║   1. 🟢  Beginner    - Git fundamentals              ║
║   2. 🟡  Intermediate - Common workflows              ║
║   3. 🟠  Advanced    - Complex operations             ║
║   4. 🔴  Expert      - Master challenges              ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
""")
        return input("Select difficulty (1-4): ").strip()

    def show_confirmation(self, message: str) -> bool:
        """
        Show a confirmation prompt.

        Args:
            message: Message to display

        Returns:
            True if confirmed
        """
        response = input(f"\n{message} (y/n): ").strip().lower()
        return response == "y"

    def show_message(self, title: str, message: str, style: str = "info") -> None:
        """
        Display a styled message.

        Args:
            title: Message title
            message: Message content
            style: 'info', 'success', 'warning', 'error'
        """
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}

        icon = icons.get(style, "ℹ️")
        width = max(len(title), len(message)) + 4

        print("\n" + "═" * width)
        print(f"{icon} {title}")
        print("─" * width)
        print(f"   {message}")
        print("═" * width)

    def show_score_summary(self, score_data: Dict[str, Any]) -> None:
        """
        Display score summary.

        Args:
            score_data: Score calculation result
        """
        print("""
╔═══════════════════════════════════════════════════════╗
║                   SCORE SUMMARY                       ║
╠═══════════════════════════════════════════════════════╣
""")
        print(f"║   Base Score:      {score_data.get('base', 0):>10,}                   ║")
        print(f"║   Time Bonus:      {score_data.get('time_score', 0):>+10,}                   ║")
        print(
            f"║   Command Bonus:   {score_data.get('command_score', 0):>+10,}                   ║"
        )
        print(f"║   Hint Penalty:    {score_data.get('hint_penalty', 0):>-10,}                   ║")
        print(
            f"║   Completion:      {score_data.get('completion_bonus', 0):>10,}                   ║"
        )
        print("╠═══════════════════════════════════════════════════════╣")
        print(f"║   TOTAL SCORE:     {score_data.get('total', 0):>10,}                   ║")
        print(f"║   RATING:          {score_data.get('rating', 'N/A'):>10}                   ║")
        print("╚═══════════════════════════════════════════════════════╝")

    def show_level_complete(self, level_name: str, score: int, rating: str) -> None:
        """
        Display level completion screen.

        Args:
            level_name: Name of completed level
            score: Final score
            rating: Performance rating
        """
        print(self.box_art["level_complete"])
        print(f"\n   Level: {level_name}")
        print(f"   Score: {score:,}")
        print(f"   Rating: {rating}")
        print()

    def get_text_input(self, prompt: str, required: bool = True) -> str:
        """
        Get text input from user.

        Args:
            prompt: Input prompt
            required: Whether input is required

        Returns:
            User input
        """
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("This field is required.")

    def get_number_input(
        self, prompt: str, min_val: int | None = None, max_val: int | None = None
    ) -> int:
        """
        Get numeric input from user.

        Args:
            prompt: Input prompt
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            User input
        """
        while True:
            try:
                value = int(input(prompt).strip())
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}.")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")
