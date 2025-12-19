# El Ayuntade

**El Ayuntade** (Spanish for "The Helper") is a feature-rich, terminal-based personal productivity assistant and command-line interface (CLI) tool. It serves as an all-in-one productivity hub combining task management, AI chat capabilities, translation services, automation, and entertainment features.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### 📋 Productivity Tools

#### **TODO List Manager**
- Add, remove, and view TODO items
- Sort tasks alphabetically (ascending/descending)
- Reorder items dynamically
- Built-in work timer with progress tracking
- Automatic worklog recording with timestamps

#### **Checklist Manager**
- Create and manage checklists with check/uncheck functionality
- Bulk operations (check all, uncheck all, remove checked/unchecked)
- Visual status indicators (✓/✗)
- Support for multiple items (semicolon-separated)

#### **Notes Manager**
- Simple text-based note taking
- Add and remove notes by line number
- Quick view all notes

### 🤖 AI & Intelligence

#### **LLM Chat Integration**
- Interactive chat using Ollama (local AI models)
- Configurable model selection (deepseek-r1, llama3.2, etc.)
- Context-aware conversations with chat history
- Clean output with automatic thinking tag removal

### 🌍 Language & Communication

- **Text-to-Speech (TTS)** - Google Text-to-Speech integration
- **Translation** - Support for 100+ languages via Google Translate
- **Combined TTS+Translation** - Translate and speak text in any language

### 🔧 Automation & System Tools

- **Application Launcher** - Open macOS/Windows apps from CLI
- **Auto-click Center** - Optional PyAutoGUI integration for automated clicking
- **Internet Speed Test** - Measure download/upload speeds and ping
- **Connection Monitor** - Real-time internet connectivity checking

### 🎮 Utilities & Games

- **Mathematical Expression Evaluator** - Safe eval with support for complex expressions and constants (π, e)
- **Math Game** - Interactive quiz with text or voice input modes
- **Coin Flip / Random Choice** - Decision-making tool
- **Settings Manager** - Persistent configuration system

### 🎨 Visual Effects

- **Neon Text Rendering** - Colorful terminal output with multiple color schemes
- **ASCII Art Logo** - Custom branded interface
- **Animated Logo** - Smooth color-cycling animation on startup

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Ollama (for AI chat features) - [Install from ollama.ai](https://ollama.ai)

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd el_ayuntade_bkm
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
```

3. **Activate the virtual environment:**
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the application:**
```bash
python el_ayuntade_bkm.py
```

## 📚 Usage

### Quick Start

After launching the application, you'll see an animated logo and the main prompt:

```
╔════════════════════════════════════════╗
║        Welcome to El Ayuntade          ║
║         Your CLI Productivity Hub      ║
╚════════════════════════════════════════╝

Type 'help' for available commands or 'exit' to quit.
```

### Command Reference

#### **TODO Commands**
```bash
todo add <task>              # Add a new TODO item
todo remove <number>         # Remove TODO by index
todo show                    # Display all TODOs
todo sort asc/desc          # Sort alphabetically
todo change <old> <new>     # Reorder items
todo work <minutes>         # Start work timer
```

#### **Checklist Commands**
```bash
check add <item>            # Add checklist item
check remove <number>       # Remove by index
check <number>              # Toggle check/uncheck
check show                  # Display checklist
check all                   # Check all items
check uncheck all          # Uncheck all items
check remove checked       # Remove all checked items
```

#### **Notes Commands**
```bash
notes add <text>           # Add a note
notes remove <number>      # Remove note by index
notes show                 # View all notes
```

#### **AI Chat**
```bash
chat                       # Start interactive AI chat session
# In chat: Type messages to chat with AI
# In chat: Type 'exit' or 'quit' to leave chat
```

#### **Language Tools**
```bash
tts <text>                 # Convert text to speech
tr <text> -> <language>    # Translate text
# Example: tr Hello world -> spanish
```

#### **System Tools**
```bash
open <app_name>            # Launch application
speedtest                  # Run internet speed test
eval <expression>          # Calculate math expression
# Example: eval 2 * (3 + 4)
```

#### **Games & Utilities**
```bash
mathgame [count]           # Start math quiz (optional question count)
coin <option1> <option2>   # Flip coin between choices
animate [seconds]          # Display animated logo
```

#### **Settings**
```bash
settings show              # Display current settings
settings set <key> <value> # Update a setting
settings reset             # Reset to defaults

# Available settings:
# - ollama_model: AI model to use (default: deepseek-r1:1.5b)
# - auto_click_center: Enable/disable auto-clicking (true/false)
```

#### **General Commands**
```bash
help                       # Show help message
clear / clr               # Clear screen
exit / quit               # Exit application
```

## 🗂️ Project Structure

```
el_ayuntade_bkm/
├── el_ayuntade_bkm.py      # Main entry point & command router
├── todo_app.py             # TODO list application logic
├── checklist_app.py        # Checklist application logic
├── mathgame.py             # Math game implementation
├── utils.py                # Utility functions (colors, rendering)
├── user_data.py            # Configuration & file paths
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── user_datas/             # Data storage directory
│   ├── todos.json         # TODO items storage
│   ├── checklists.json    # Checklist items storage
│   ├── notes.json         # Notes storage
│   ├── settings.json      # User settings
│   └── worklogs.json      # Work session logs
└── .venv/                 # Virtual environment
```

## 🔧 Dependencies

### Core Dependencies
- **simpleeval** (1.0.3) - Safe mathematical expression evaluation
- **gTTS** (2.5.4) - Google Text-to-Speech
- **googletrans** (4.0.2) - Translation API
- **SpeechRecognition** - Voice input support
- **PyAutoGUI** (0.9.54) - GUI automation
- **Pillow** (≥8.0.0) - Image processing
- **Levenshtein** (0.27.1) - Fuzzy string matching
- **speedtest-cli** (2.1.3) - Internet speed testing
- **pywhatkit** (5.4) - Additional automation features
- **wikipedia** (1.4.0) - Wikipedia integration

### External Tools
- **Ollama** - Required for AI chat features ([ollama.ai](https://ollama.ai))

## 💡 Examples

### Managing TODOs
```bash
> todo add Buy groceries
✓ Added: Buy groceries

> todo add Finish project report
✓ Added: Finish project report

> todo show
━━━━━━━━━━━━━━━━━━━━━━━━━━
TODO LIST (2 items)
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Buy groceries
2. Finish project report

> todo work 25
[Timer runs for 25 minutes with progress bar]
✓ Work session completed! Logged to worklog.
```

### Using AI Chat
```bash
> chat
╭─────────────────────────────────────╮
│   Chat with AI (using deepseek-r1)  │
╰─────────────────────────────────────╯

You: What is the capital of France?
AI: The capital of France is Paris...

You: exit
Exiting chat...
```

### Translation & TTS
```bash
> tr Good morning -> french
Translation: Bonjour

> tts Hello world
[Speaks "Hello world" using text-to-speech]
```

### Math Evaluation
```bash
> eval 2 ** 10
Result: 1024

> eval sqrt(144) + pi
Result: 15.141592653589793
```

## ⚙️ Configuration

Settings are stored in `user_datas/settings.json` and persist across sessions.

### Default Settings
```json
{
  "ollama_model": "deepseek-r1:1.5b",
  "auto_click_center": false
}
```

### Changing Settings
```bash
> settings set ollama_model llama3.2
✓ Setting updated: ollama_model = llama3.2

> settings set auto_click_center true
✓ Setting updated: auto_click_center = true
```

## 🎨 Color Schemes

El Ayuntade features vibrant terminal output with multiple color schemes:

- **Neon Colors** - Purple, blue, magenta gradient
- **Yellow Colors** - Amber, tangerine, lemon
- **Randomized** - Dynamic color selection for each character

## 🐛 Error Handling

The application includes smart error handling:

- **Typo Detection** - Suggests similar commands using Levenshtein distance
- **Graceful Exits** - Handles Ctrl+C and Ctrl+D
- **Input Validation** - Validates all user inputs
- **Colored Messages** - Clear visual distinction for errors and success

Example:
```bash
> tood show
❌ Unknown command: 'tood'
💡 Did you mean: 'todo'?
```

## 🚀 Platform Support

- **macOS** - Full support (primary platform)
- **Windows** - Full support with platform-specific adaptations
- **Linux/Unix** - Basic support

## 📝 Data Persistence

All user data is stored in JSON format in the `user_datas/` directory:

- **todos.json** - TODO items
- **checklists.json** - Checklist items
- **notes.json** - User notes
- **settings.json** - Application settings
- **worklogs.json** - Work session logs with timestamps

Data is automatically saved after each operation.

## 🤝 Contributing

Contributions are welcome! This project is currently in active development with ongoing refactoring on the `oop-refactor` branch.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Batu Koray Masak**

## 🔮 Future Enhancements

- [ ] OOP refactoring (in progress on `oop-refactor` branch)
- [ ] Plugin system for custom commands
- [ ] Cloud synchronization for data
- [ ] Multi-user support
- [ ] Web interface
- [ ] Mobile companion app
- [ ] Enhanced AI capabilities with more models
- [ ] Task scheduling and reminders
- [ ] Integration with popular productivity tools

## 🙏 Acknowledgments

- Built with Python and love ❤️
- Powered by Ollama for AI features
- Uses various open-source libraries from the Python ecosystem

---

**Happy productivity with El Ayuntade! 🎉**

For questions, issues, or feature requests, please open an issue on the repository.
