# Pykémon

**Pykémon** is a terminal-based game written in Python, inspired by the classic Pokémon games. This project is developed as part of the DD1349 course, with the aim of exploring game development fundamentals and effective collaboration using GitHub.

## 🎯 Project Goals

- ✅ Build a simplified, text-based Pokémon-style game in Python.
- 🧪 Experiment with potential extensions like:
  - A graphical user interface (GUI)
  - Multiplayer support
- 🤝 Learn how to collaborate efficiently using GitHub:
  - Branching workflows
  - Pull requests
  - Issue tracking
  - Continuous integration / deployment (CI/CD)

## 🕹️ Current Features

- Terminal-based interface
- Basic battle system
- A few sample Pykémon with unique stats and abilities
- Turn-based mechanics
- Player vs Player (PvP) mode
- Online multiplayer functionality

## 🚧 In Development / Planned Features

- Additional Pykémon types and evolutions

## 🚀 Possible Future Features

- Graphical User Interface (possibly with `tkinter`, `pygame`, or another library)
- Save/load system for game state

## 🛠️ Technologies Used

- Python 3.x
- Git & GitHub for version control and collaboration
- [Optional future tools: `pygame`, `tkinter`, socket programming, etc.]

## 🤝 Collaboration Workflow

This project emphasizes learning and applying collaborative software development practices:

- Use of GitHub Projects and Issues for task management
- Feature branches and pull requests for new functionality
- Code reviews to ensure quality and consistency
- GitHub Actions for automated testing (planned)

## 🚀 Getting Started

To run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/stre4k/pykemon.git
   cd pykemon
   ```

2. Navigate to the `src/` directory:
   ```bash
   cd src
   ```

3. Start the game using the main entry point:
   ```bash
   python3 start.py
   ```

4. You will be prompted to:
   - Enter `1` to **host a game** (run as server), or
   - Enter `2` to **join a game** (run as client) and provide a valid IP address to connect to the host. (For example, use 127.0.0.1 or localhost to connect to the local machine).

> ⚠️ **Warning:** Multiplayer mode is currently unstable and may contain bugs. Use with caution!

---

### 🧪 Local Testing

If you'd prefer to run a local single-player variant (for testing or debugging), you can launch the game logic directly:

```bash
python3 main.py
```

