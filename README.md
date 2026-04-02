# Git Quest

**Learn Git Through Interactive Challenges**

Git Quest is an educational terminal-based game that teaches Git through hands-on challenges. Each level presents a broken or incomplete Git repository, and you must fix it using real Git commands.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git installed and in your PATH

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/git-quest.git
cd git-quest

# Install dependencies
pip install -e .
```

### Running the Game

```bash
# Run using the script installed via pip
git-quest

# Or run via python
python main.py

# Or run as a module
python -m git_quest
```

---

## How to Play

### Starting the Game

Git Quest uses a modern terminal interface powered by `rich`.

```
   ╔══════════════════════════════════╗
   ║      GIT QUEST - LEARN GIT       ║
   ╚══════════════════════════════════╝
      0/50 Levels Completed

   [1] Start New Game
   [2] Continue Progress
   [3] Select Level
   [4] Exit
```

### Gameplay

Each level presents a Git challenge. You'll see:

- **Mission**: What you need to accomplish
- **Story**: Context for the challenge
- **Repository Path**: Where the Git repo is located

Type Git commands directly in the game:

```bash
git-quest> git status
git-quest> git add .
git-quest> git commit -m "initial commit"
```

### In-Level Special Commands

| Command | Description |
|---------|-------------|
| `status` | Show detailed repository analysis |
| `hint` | Get a hint (reduces score) |
| `check` | Check if mission objective is met |
| `quit` | Exit to main menu |

---

## Level Categories

### Beginner (Levels 1-10)
Learn Git fundamentals like committing, branching, and basic merging.

### Intermediate (Levels 11-25)
Master merge conflicts, stashing, and repository navigation.

### Advanced (Levels 26-40)
Handle complex operations like rebasing, interactive rebasing, and squashing.

### Expert (Levels 41-50)
Solve master-level challenges including history recovery and disaster management.

---

## Scoring System

Your performance is rated based on:
- **Base Score**: Varies by level difficulty.
- **Time Taken**: Faster completion yields higher scores.
- **Command Efficiency**: Fewer commands used is better.
- **Hints Used**: Using hints applies a score penalty.

Ratings range from **S** (Elite) to **F** (Failed).

---

## Example Level: First Commit

```
   LEVEL 1: FIRST COMMIT
   
   Story: Every great project starts with a single commit. Make yours!
   
   Difficulty: BEGINNER
   Base Score: 1000
   Par Time: 120s
   
   Path: ./repos/workspace/level01
```

1. Run `git status` to see untracked files.
2. Run `git add .` to stage changes.
3. Run `git commit -m "Initial commit"` to create the commit.
4. Run `check` to complete the level!

---

## Command Line Options

```bash
# Use custom workspace directory
git-quest --workspace ~/my-git-repos

# Use custom data directory
git-quest --data-dir ~/my-game-data
```

---

## Project Structure

```
git-quest/
├── core/                    # Core game engine logic
│   ├── game_engine.py       # Level lifecycle coordination
│   ├── mission_engine.py    # Objective validation
│   ├── score_engine.py      # Score calculation
│   └── progress_manager.py  # Progress persistence
├── git_engine/              # Git operations & analysis
│   ├── repo_manager.py      # Repo creation and cleanup
│   ├── repo_analyzer.py     # Repo state analysis
│   └── git_executor.py      # Low-level git execution
├── level_definitions/       # JSON level configurations
│   ├── level_loader.py      # Level loading system
│   └── levels/              # level01.json ... level50.json
├── ui/                      # User interface
│   └── cli_app.py           # Rich-powered CLI application
├── utils/                   # System utilities
├── data/                    # Game data (auto-generated)
└── repos/                   # Git repositories (auto-generated)
```
