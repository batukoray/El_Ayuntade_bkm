import random
import sys

class Colors:
    """
    This class contains color codes for terminal text formatting.
    """
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    LIGHT_GRAY = '\033[37m'

help_content = ('Type "todo help" to see the commands for the TODO app.'
              '\nType "check help" to see the commands for the Checklist app.'
              '\nType open <App Name> to open the desired application.'
              '\nType "exit" to exit the program.'
              '\nType "chat" to access the LLM.'
              '\nType eval <expression> to evaluate a mathematical expression.'
              '\nType "tts help" to see the commands for the Text-to-Speech app.'
              '\nType "tr help" to see the commands for the Translation app.'
              '\nType "settings help" to see the commands for the Settings app.'
              '\nType "animate" or "animation" or "anim" to see the animated logo.'
              '\nType "clear" or "clr" to clear the screen.'
              '\nType "coin" to flip a coin.'
              '\nType "quit" to exit the program.')

# Color theme of the program:
neon_colors = ["\033[35m", "\033[95m","\033[94m",  "\033[94m"]
yellow_colors = [
    "\033[93m",           # Bright yellow (standard)
    "\033[38;5;220m",     # Goldenrod / amber
    "\033[38;5;214m",     # Deep orange / tangerine
    "\033[38;5;226m"      # Neon lemon yellow
]

maintext = r"""
██████  ██╗╔═██ ╔███    ███╗
██═╬═██ ██╚╝██╝ ║████  ████║
██████  █████   ║██╗████╔██║      El Ayuntade By:
██═╬═██ ██╔╗██╗ ║██╚╗██╔╝██║     Batu Koray Masak
██████  ██╝╚═██ ╚██ ╚══╝ ██╝

Type "help" to see the available commands.

"""
goodbye_text = 'Goodbye! | El Ayuntade By: Batu Koray Masak'

def neon_text(text,randomness=True,neon_map_num = 0,colors='neon'):
    """
This function takes a text input and returns it with neon colors applied to each character.
    :param text: The text to be colored.
    :param randomness: If True, each character will be colored randomly from the neon_colors list. It is true in default.
    :param neon_map_num: An integer used to map the colors in a specific order. Is 0 in default. Only effective if randomness is False.
    :param colors: The colors to use. Default is 'neon'. Choices are 'neon' or 'yellow'. TODO: Add more colors.
    :return: A string with neon colors applied to each character.
    """
    if randomness:
        if colors == 'neon':
            return ''.join(f"{random.choice(neon_colors)}{char}"for char in text) + Colors.RESET
        elif colors == 'yellow':
            return ''.join(f"{random.choice(yellow_colors)}{char}"for char in text) + Colors.RESET
    else:
        if colors == 'neon':
            return ''.join(f"{neon_colors[(j-neon_map_num) % len(neon_colors)]}{char}" for j, char in enumerate(text)) + Colors.RESET
        elif colors == 'yellow':
            return ''.join(f"{yellow_colors[(j-neon_map_num) % len(yellow_colors)]}{char}" for j, char in enumerate(text)) + Colors.RESET

commands = [
    # Top-level
    'help', 'exit', 'quit', 'clear', 'clr', 'eval', 'open', 'o',
    'coin', 'tts', 'tr', 'chat', 'send', 'animate', 'animation', 'anim',
    'speedtest', 'mathgame',
    # Todo
    'todo', 'todo help', 'todo ls', 'todo add', 'todo rm', 'todo rm all',
    'todo changeorder', 'todo abcorder', 'todo cbaorder', 'todo do',
    # Check
    'check', 'check help', 'check ls', 'check add', 'check rm',
    'check changeorder', 'check -check', 'check -uncheck',
    # Notes
    'notes', 'notes help', 'notes ls', 'notes add', 'notes rm',
    # Settings
    'settings', 'settings help', 'settings ls', 'settings edit',
    'settings add', 'settings reset',
]

def clear_last_lines(n:int):
    """
    This function clears the last n lines in the terminal.
    :param n: The number of lines to clear.
    :return: void
    """

    for _ in range(n):
        # Move cursor up one line
        sys.stdout.write('\x1b[1A')
        # Clear entire line
        sys.stdout.write('\x1b[2K')