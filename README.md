<div align="center">

# El Pulpo

**A Modular Command-Line Productivity Suite**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20|%20Windows%20|%20Linux-lightgrey)](https://github.com/batukoray/El_Pulpo)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## Abstract

**El Pulpo** is a terminal-based personal productivity assistant designed to consolidate essential daily utilities into a single, cohesive command-line interface. The application integrates task management, note-taking, language services, and mathematical utilities, enabling users to maintain workflow efficiency without context-switching between multiple applications.

---

## Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Module Documentation](#module-documentation)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)
9. [Author](#author)

---

## Features

| Module | Description |
|--------|-------------|
| **Task Management** | Create, organize, and track TODO items with sorting and timed work sessions |
| **Checklist System** | Maintain checklists with check/uncheck functionality and batch operations |
| **Notes** | Quick note-taking with line-based management |
| **Translation** | Real-time text translation via Google Translate API |
| **Text-to-Speech** | Convert text to audio output using gTTS |
| **Math Evaluation** | Evaluate mathematical expressions with support for constants (pi, e) |
| **Speed Test** | Measure internet connection speed (download, upload, ping) |
| **App Launcher** | Open system applications directly from the terminal |
| **Math Game** | Mental arithmetic training module |

---

## System Requirements

- Python 3.8 or higher
- macOS, Windows, or Linux
- Internet connection (required for translation, TTS, and speed test features)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/batukoray/El_Pulpo.git
cd El_Pulpo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python el_pulpo.py
```

---

## Usage

Upon execution, the application presents an interactive command prompt. Commands follow a consistent syntax:
```
<module> <action> [arguments]
```

### Quick Reference
```bash
help                        # Display available commands
todo add <task>             # Add a new task
todo ls                     # List all tasks
check add <item>            # Add checklist item
check -check <index>        # Mark item as complete
notes add <content>         # Add a note
tr <text> -> <language>     # Translate text
tts <text>                  # Text-to-speech
eval <expression>           # Evaluate math expression
speedtest                   # Run internet speed test
open <application>          # Launch system application
exit                        # Terminate session
```

---

## Module Documentation

### Task Management (`todo`)

The TODO module provides comprehensive task tracking with the following capabilities:

| Command | Description |
|---------|-------------|
| `todo ls` | Display all tasks |
| `todo add <task>` | Add a new task |
| `todo rm <index>` | Remove task by index |
| `todo rm all` | Clear all tasks |
| `todo changeorder` | Swap two task positions |
| `todo abcorder` | Sort tasks alphabetically |
| `todo cbaorder` | Sort tasks reverse-alphabetically |
| `todo do` | Start a timed work session |

### Checklist (`check`)

The checklist module supports stateful item tracking:

| Command | Description |
|---------|-------------|
| `check ls` | Display checklist with status indicators |
| `check add <item>` | Add single item |
| `check add <a; b; c>` | Add multiple items (semicolon-separated) |
| `check -check <index>` | Mark item as complete |
| `check -uncheck <index>` | Mark item as incomplete |
| `check -check all` | Mark all items complete |
| `check rm <index>` | Remove item |
| `check rm -checked` | Remove all completed items |

### Notes (`notes`)

| Command | Description |
|---------|-------------|
| `notes ls` | Display all notes |
| `notes add <content>` | Add a new note |
| `notes rm <line>` | Remove note by line number |

### Translation (`tr`)

| Command | Description |
|---------|-------------|
| `tr <text>` | Translate to Turkish (default) |
| `tr <text> -> <lang>` | Translate to specified language |
| `tr <text> -> tts` | Translate and speak result |

### Text-to-Speech (`tts`)

| Command | Description |
|---------|-------------|
| `tts <text>` | Convert text to speech |

### Mathematical Evaluation (`eval`)

| Command | Description |
|---------|-------------|
| `eval <expression>` | Evaluate expression |
| Supports | `+`, `-`, `*`, `/`, `^`, `pi`, `e` |

---

## Configuration

User data is stored in the `user_datas/` directory:
```
user_datas/
├── todos.json        # Task data
├── checklists.json   # Checklist data
├── notes.json        # Notes data
├── settings.json     # User preferences
└── worklogs.json     # Work session logs
```

Settings can be modified via:
```bash
settings ls                          # View current settings
settings edit <key> <value>          # Modify setting
settings reset                       # Restore defaults
```

---

## Project Structure
```
El_Pulpo/
├── el_pulpo.py          # Main application entry point
├── todo_app.py          # Task management module
├── checklist_app.py     # Checklist module
├── mathgame.py          # Math game module
├── utils.py             # Utility functions and constants
├── user_data.py         # File path configurations
├── requirements.txt     # Python dependencies
└── user_datas/          # User data storage (auto-generated)
```

---

## Contributing

Contributions are welcome. Please adhere to the following guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes with descriptive messages
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Batu Koray Masak**

Özyeğin University  
AI & Data Engineering | Computer Science

---