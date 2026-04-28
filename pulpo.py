import subprocess
import time
import sys
import math
import os
import json
import random
import socket
import atexit
import readline

import speedtest
from simpleeval import simple_eval
from gtts import gTTS
from googletrans import Translator
import asyncio
import Levenshtein
import pyautogui
import user_data

from todo_app import *
from checklist_app import *
from utils import *  # This imports `commands`
from mathgame import *

# ==========================================
# READLINE CONFIGURATION
# ==========================================

HISTORY_FILE = os.path.expanduser('~/.el_pulpo_history')
HISTORY_LENGTH = 1000

try:
    readline.read_history_file(HISTORY_FILE)
except (FileNotFoundError, OSError):
    pass

atexit.register(readline.write_history_file, HISTORY_FILE)
readline.set_history_length(HISTORY_LENGTH)

# Completion settings
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set show-all-if-ambiguous on')
readline.parse_and_bind('set completion-ignore-case on')
readline.parse_and_bind('set colored-stats on')
readline.parse_and_bind('set skip-completed-text on')

# Editing settings
readline.parse_and_bind('set editing-mode emacs')
readline.parse_and_bind('set bell-style visible')
readline.parse_and_bind('"\e[A": history-search-backward')
readline.parse_and_bind('"\e[B": history-search-forward')


def completer(text, state):
    """Context-aware completer using commands from utils.py."""
    buffer = readline.get_line_buffer().lstrip()

    if ' ' in buffer:
        # Completing subcommand
        main_cmd = buffer.split()[0]
        prefix = text.lower()
        options = [
            cmd.split(' ', 1)[1]
            for cmd in commands
            if ' ' in cmd and
               cmd.startswith(main_cmd + ' ') and
               cmd.split(' ', 1)[1].startswith(prefix)
        ]
    else:
        # Completing main command (only top-level, no duplicates)
        seen = set()
        options = []
        for cmd in commands:
            top = cmd.split()[0]
            if top.startswith(text.lower()) and top not in seen:
                seen.add(top)
                options.append(top)

    return options[state] if state < len(options) else None


readline.set_completer(completer)
readline.set_completer_delims(' \t\n')

def set_command_variables(text_input:str) -> []:
    """
    This function takes a text input and returns a list containing the command array, the original command, and the lowercased command.
    :param text_input:
    :return: [command_original, command_lower, command_arr]
    1. command_original: The original command input by the user without multiple whitespaces.
    2. command_lower: The original command input by the user in lowercase without multiple whites
    3. command_arr: The command input by the user split into an array, all in lowercase and without empty strings.
    """
    command_arr = [n for n in text_input.lower().split(' ') if n != '']
    command_original = ' '.join(text_input.strip().split())
    command_lower = command_original.lower()
    return [command_original,command_lower,command_arr]

def analyze_input(text_input):
    """
    This function analyzes the input text and executes the corresponding command.
    :param text_input: The input text from the user.
    :return: void
    """
    command_arr = set_command_variables(text_input)[2]
    command_lower = set_command_variables(text_input)[1]
    command_original = set_command_variables(text_input)[0]

    # If the command is empty, return
    if command_lower == '':
        clear_last_lines(1)
        return
    # To Do App Commands:
    match command_arr[0]:
        case 'todo':
            if len(command_arr) >= 2:
                match command_arr[1]:
                    case 'help':
                        todo_help()
                    case 'ls':
                        todo_list_view()
                    case 'rm':
                        todo_delete_function(command_original)

                    case 'add':
                        todo_add(command_original)
                    case 'changeorder':
                        todo_changeorder()
                    case 'abcorder':
                        todo_abcorder()
                    case 'cbaorder':
                        todo_cbaorder()
                    case 'do':
                        todo_do_function()
                    # TODO: Add more commands here.
                    case _:
                        unknown_command(command_original,app_name='todo')
            else:
                todo_help()
        case 'check':
            if len(command_arr) >= 2:
                match command_arr[1]:
                    case 'help':
                        checklist_help()
                    case 'ls':
                        checklist_list_view()
                    case 'add':
                        checklist_add(command_original)
                    case 'rm':
                        checklist_delete_function(command_original)
                    case 'changeorder':
                        checklist_changeorder(command_original)
                    case '-check':
                        checklist_mark(command_original,check=True)
                    case '-uncheck':
                        checklist_mark(command_original,check=False)
                    case _:
                        unknown_command(command_original,app_name='check')

            else:
                checklist_help()
        case 'notes':
            if len(command_arr) >= 2:
                match command_arr[1]:
                    case 'add':
                        notes_add(command_original)
                    case 'rm':
                        notes_remove_lines(command_original)
                    case 'ls':
                        notes_list_view()
            # TODO: Complete the notes app asap.
        case 'coin':
            coin_flip_function(command_original)
        case 'settings':
            if len(command_arr) >= 2:
                match command_arr[1]:
                    case 'edit':
                        settings_edit(command_original)
                    case 'help':
                        settings_help()
                    case 'ls':
                        settings_list_view()
                    case 'add':
                        settings_edit(command_original)
                    case 'reset':
                        userinput = input('Are you sure you want to reset the settings to defaults? (y): ')
                        if userinput.lower() == 'y':
                            global settings_dict
                            settings_dict = settings_defaults.copy()
                            settings_save()
                            print('Settings have been reset to defaults.')
                        else:
                            print('Settings were not reset to defaults.')
                        del userinput
                    case _:
                        unknown_command(command_original,app_name='settings')
            else:
                settings_help()
        case 'open':
            if len(command_arr) > 1:
                open_function(command_original)
            else:
                print(f'{Colors.RED}Error: You need to specify an application to open.{Colors.RESET}')
        case 'o':
            open_function(set_command_variables(command_original.replace('o ','open '))[0])
        case 'speedtest':
            measure_speed()

        case 'help':
            if len(command_arr) == 1:
                print(help_content)
            else:
                print(f'{Colors.RED}Error: The "help" command does not take any arguments.{Colors.RESET}')
        case 'tts':
            text_to_speech_function(command_original)
        case 'tr':
            translate_function(command_original)

        case 'mathgame':
            mathgame_start(command_original)
        case 'exit' | 'quit':
            if len(command_arr) == 1:
                clear_screen(text=False)
                print(neon_text(goodbye_text))
                sys.exit(0)
            else:
                print(f'{Colors.RED}Error: The "exit" command does not take any arguments.{Colors.RESET}')
        case 'clear' | 'clr':
            if len(command_arr) == 1:
                clear_screen(text=True,randomness=True,clear_technique='os')
            else:
                print(f'{Colors.RED}Error: The "clear" command does not take any arguments.{Colors.RESET}')
        case 'eval':
            if len(command_arr) > 1:
                expr = command_original[len('eval '):].strip()
                expr = expr.replace('^','**')
                names = {'pi':math.pi,'e':math.e}
                try:
                    result = simple_eval(expr,names=names)
                    if isinstance(result,(int, float)):
                        print(f'{result:,}')
                    else:
                        print(result)
                except Exception:
                    print(f'{Colors.RED}Error: Invalid expression. Please use the format "eval <math_expression>".{Colors.RESET}')
            else:
                print(f'{Colors.RED}Error: The "eval" command requires an expression to evaluate.{Colors.RESET}')
        case 'animate' | 'animation' | 'anim':
            if len(command_arr) == 1:
                animate_logo(40,arrows=True)
            elif len(command_arr) == 2:
                try:
                    animate_logo(int(float(command_arr[1])*20),arrows=True)
                except:
                    print(f'{Colors.RED}Format error. Make sure you write "{command_arr[0]} <animation seconds>".{Colors.RESET}')
        case _:
            try:
                expr = command_original
                expr = expr.replace('^', '**')
                names = {'pi': math.pi, 'e': math.e}
                try:
                    result = simple_eval(expr, names=names)
                    if isinstance(result, (int, float)):
                        print(f'{result:,}')
                    else:
                        print(result)
                except Exception:
                    unknown_command(command_original)
                    readline.remove_history_item(readline.get_current_history_length() - 1)
            except Exception:
                unknown_command(command_original)
                readline.remove_history_item(readline.get_current_history_length() - 1)

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

def clear_screen(text=True,randomness=True,clear_technique='os',subtitle=None,internet_indicator=False):
    """
    This function clears the terminal screen.
    :param text: If True, it will print the main text after clearing the screen. If False, it will not print the main text/branding. True in default.
    :param randomness: If True, the main text will be colored randomly. If False, it will use a fixed color pattern. True in default.
    :param clear_technique: The technique to clear the screen. 'os' for using os.system, 'ascii' for using ANSI escape codes. "os" in default.
    :param subtitle: If True, the main text will be colored subtitle. True in default.
    :return: void
    """
    if clear_technique == 'os':
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For Unix/Linux/Mac
            os.system('clear')
    elif clear_technique == 'ascii':
        clear_last_lines(50)
    if text:
        print(neon_text(maintext,randomness))  # Header
    if internet_indicator:
        clear_last_lines(1)
        print(f"{neon_text('App working with internet connection.' if is_connected_socket() else 'App working without internet connection.', randomness)}{Colors.RESET}\n")
    if subtitle is not None:
        clear_last_lines(1)
        print(f"\n{neon_text(subtitle, randomness)}\033[0m\n")  # Subtitle

# Notes app start

def notes_add(command_original:str):
    """
    This function adds a new note to the notes file.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    note = command_original[len('notes add '):]
    if note.strip() == '':
        print(f'{Colors.RED}Error: You need to provide a name for the note.{Colors.RESET}')
        return
    with open(user_data.NOTES_FILE_LOC, 'a', encoding='utf-8') as f:
        f.write(f'{note}\n')
    print(f'Added new note: {note}')

def notes_remove_lines(command_original:str):
    """
    This function removes a line from the notes file based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    linecount = int(command_original[len('notes rm '):].strip())
    if linecount <= 0:
        print(f'{Colors.RED}Error: The line number must be a positive integer.{Colors.RESET}')
        return
    try:
        with open(user_data.NOTES_FILE_LOC, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if linecount > len(lines):
            print(f'{Colors.RED}Error: The line number is out of range.{Colors.RESET}')
            return
        removed_line = lines.pop(linecount - 1)
        with open(user_data.NOTES_FILE_LOC, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'Removed line {linecount}: {removed_line.strip()}')
    except FileNotFoundError:
        print(f'{Colors.RED}Error: The notes file does not exist.{Colors.RESET}')

def notes_list_view():
    """
    This function prints the notes in the notes file.
    :return: void
    """
    if not os.path.exists(user_data.NOTES_FILE_LOC):
        print('Your notes file is empty.')
        return
    with open(user_data.NOTES_FILE_LOC, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        print('Your notes file is empty.')
        return
    print('Notes:')
    for j, line in enumerate(lines, start=1):
        print(f'{j}: {line.strip()}')

# Notes app end

# Setting functions start


settings_defaults = {'openappstayontab': False}  # Default settings

settings_dict = {'openappstayontab': False}
settings_names = ['openappstayontab']

def update_settings():
    """
    This function updates the settings by reading from a JSON file.
    :return: void
    """
    global settings_dict
    if os.path.exists(user_data.SETTINGS_FILE_LOC):
        with open(user_data.SETTINGS_FILE_LOC, "r", encoding="utf-8") as f:
            try:
                settings_dict = json.load(f)
            except json.JSONDecodeError:
                settings_dict = {}
    else:
        settings_dict = {}

update_settings()

def settings_save():
    """
    This function saves the current settings to a file in JSON format.
    :return: void
    """
    with open(user_data.SETTINGS_FILE_LOC, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, ensure_ascii=False, indent=2)

def settings_help():
    """
    This function displays the help content for the settings app.
    :return: void
    """
    print('Type "settings edit <setting_name> <new_value_of_setting>" to add a new setting.'
          '\nType "settings help" to see this help message again.'
          '\nType "settings ls" to list all settings.'
          '\nType "settings rm <setting_name>" to remove a setting.'
          '\nType "settings rm all" to remove all settings.'
          '\nSetting names: ' + ', '.join(settings_names))

def settings_list_view():
    """
    This function prints the settings in the settings file.
    :return: void
    """
    update_settings()
    if settings_dict:
        print('Settings:')
        for key, value in settings_dict.items():
            print(f'{key}: {value}')
    else:
        print('Your settings are empty.')

def settings_edit(command_original:str):
    """
    This function adds a new setting to the settings file.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    setting = command_original[len('settings edit '):].lower()
    if setting.strip() == '':
        print(f'{Colors.RED}Error: You need to provide the name of the setting.{Colors.RESET}')
        return
    setting_name = setting.split(' ')[0].strip()
    try:
        match setting.split(' ')[1].strip():
            case 'true':
                setting_value = True
            case 'false':
                setting_value = False
            case _:
                if setting.split(' ')[1].strip().isdigit():
                    setting_value = int(setting.split(' ')[1].strip())
                else:
                    setting_value = setting.split(' ')[1].strip().lower()

    except IndexError:
        print(f'{Colors.RED}Error: You need to provide a value for the setting.{Colors.RESET}')
        return
    except ValueError:
        setting_value = int(setting.split(' ')[1].strip())
    settings_dict[setting_name] = setting_value
    settings_save()
    print(f'Edited setting: {setting_name} with value {setting_value}')

def open_function(command_original:str):
    """
    This is a function to open applications on the system.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    app_name = command_original[5:]
    if app_name == '':
        print(f'{Colors.RED}Error: You need to provide the name of the application to open.{Colors.RESET}')
        return
    # Check the os of the user here please
    # Macos:
    if os.name == 'posix':
        try:
            subprocess.run(['open', '-a', app_name], check=True)
            print(neon_text(f'Opened the application "{app_name}" successfully.'))
        except subprocess.CalledProcessError:
            print(f'{Colors.RED}Error: Could not open the application "{app_name}". Please make sure it is installed.{Colors.RESET}')
    # Windows:
    elif os.name == 'nt':
        try:
            subprocess.run(['start', app_name], shell=True, check=True)
            print(neon_text(f'Opened the application "{app_name}" successfully.'))
        except subprocess.CalledProcessError:
            print(f'{Colors.RED}Error: Could not open the application "{app_name}". Please make sure it is installed.{Colors.RESET}')
    else:
        print(f'{Colors.RED}Error: Your operating system is not supported for this command.{Colors.RESET}')
        return
    # Click the middle of the screen if the setting is enabled
    time.sleep(0.1) # Wait a bit for the app to open
    if settings_dict['openappstayontab'] == True:
        pyautogui.click(x=pyautogui.size().width/2, y=pyautogui.size().height/2)

def animate_logo(n=12,arrows=False):
    """
    This function animates the logo by printing it with different neon colors.
    :param n: The number of iterations for the animation.
    :param arrows: If True, it will print arrows after the main text.
    :return: void
    """
    try:
        for j in range(n):
            clear_screen(text=False,randomness=True,clear_technique='ascii')
            if arrows:
                print(neon_text(f'{maintext}\n>>>',randomness=False,neon_map_num=j),end='')
            else:
                print(neon_text(maintext,randomness=False,neon_map_num=j))
            time.sleep(0.05)
        clear_screen(text=True,randomness=False)
    except KeyboardInterrupt:
        clear_screen(text=False)
        print(neon_text(goodbye_text))
        sys.exit(0)

def coin_flip_function(command_original:str):
    """
    This function simulates a coin flip and prints the result.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    choices = command_original[len('coin '):].split()
    if not choices:
        result = random.choice(['Heads', 'Tails'])
        print(neon_text(f'Coin Flip Result: {result}'))
    elif len(choices) > 1:
        result = random.choice(command_original[len('coin '):].split(' '))
        print(neon_text(f'Coin Flip Result: {result}.')+'\nKeep in mind that randomness doesn\'t have any meaning. It is just a superstition. -bkm')
    elif len(choices) == 1:
        print(f'{Colors.RED}Error: You have to enter at least 2 items.{Colors.RESET}')
    else:
        print(f'{Colors.RED}Error: Invalid input. Please use the format "coin" or "coin <option1> <option2> <option n>".{Colors.RESET}')

def text_to_speech_function(command_original:str,print_log=True):
    """
    This function converts text to speech using gTTS and plays it.
    :param command_original: The original command input by the user without multiple whitespaces.
    :param print_log: If True, it will print the log message after playing the text to speech.
    :return: void
    """
    text= command_original[len('tts '):]
    if text == 'help':
        print('Type "tts <text>" to convert text to speech.')
        return
    tts = gTTS(text=text, lang='en')
    tts.save('speech.mp3')
    try:
        if os.name == 'nt':  # For Windows
            subprocess.run(['start', 'speech.mp3'], shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform == 'darwin':  # For macOS
            subprocess.run(['afplay', 'speech.mp3'], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:  # For Linux
            subprocess.run(['mpg123', '-q', 'speech.mp3'], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(f'{Colors.RED}Error: Could not find the audio player. On Linux, install mpg123.{Colors.RESET}')
    except subprocess.CalledProcessError as e:
        print(f'{Colors.RED}Error playing audio: {e}{Colors.RESET}')
    except Exception as e:
        print(f'{Colors.RED}Error: {e}{Colors.RESET}')
    else:
        if print_log:
            print('Text to speech played successfully.')
    # Clean up the audio file after playing
    if os.path.exists('speech.mp3'):
        os.remove('speech.mp3')

def translate_function(command_original: str):
    """
    This function translates text to a specified language using Google Translate.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    # Strip off the "tr " prefix
    cmd = command_original[len('tr '):].strip()
    if not cmd:
        print(f'{Colors.RED}Error: The "tr" command requires text to translate.{Colors.RESET}')
        return
    elif cmd.lower() == 'help':
        print('Type "tr <text> -> <language>" to translate text to a specified language.'
              '\nType "tr <text>" to translate text to English.'
              '\nType "tr <text> -> tts" to translate text to English and convert it to speech.')
        return
    # Ensure the user typed "text -> lang"
    text = cmd.split('->')[0].strip()
    if '->' not in cmd:
        try:
            async def _do_translate(t, lang):
                tr = Translator()
                return await tr.translate(t, dest=lang)
            result = asyncio.run(_do_translate(text, 'tr')).text
            print(f'Tr: "{neon_text(result)}"')
        except Exception:
            print(f'{Colors.RED}Internet error: Possible lossy internet connection{Colors.RESET}')
        return

    text, language = map(str.strip, cmd.split('->', 1))
    if not language == 'tts':
        try:
            async def _do_translate(t, lang):
                tr = Translator()
                return await tr.translate(t, dest=lang)
            result = asyncio.run(_do_translate(text, language)).text
            print(f'{language.capitalize()}: "{neon_text(result)}"')
        except Exception as e:
            print(f"{Colors.RED}Translation failed: {e}{Colors.RESET}")
    else:
        try:
            async def _do_translate(t, lang):
                tr = Translator()
                return await tr.translate(t, dest=lang)
            result = asyncio.run(_do_translate(text, 'en'))
            print(f'Translation: {neon_text(result.text)}')

            text_to_speech_function(f'tts {result.text}', print_log=False)
        except Exception as e:
            print(f"{Colors.RED}Translation failed: {e}{Colors.RESET}")
def levenshtein(s: str, t: str) -> int:
    """Compute the Levenshtein edit distance between strings s and t."""
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)

    rows = len(s) + 1
    cols = len(t) + 1
    dist = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        dist[i][0] = i
    for j in range(cols):
        dist[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if s[i-1] == t[j-1] else 1
            dist[i][j] = min(
                dist[i-1][j] + 1,      # deletion
                dist[i][j-1] + 1,      # insertion
                dist[i-1][j-1] + cost  # substitution
            )
    return dist[-1][-1]

def is_connected_socket(host="8.8.8.8", port=53, timeout=3):
    """
    Returns True if we can open a TCP socket to host:port within timeout.
    Default is Google DNS (8.8.8.8:53).
    :param host: The host to check.
    :param port: The port to check.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except OSError:
        return False


def measure_speed():
    print(neon_text('Measuring internet speed...(25 seconds)'))
    successful = True
    try:
        st = speedtest.Speedtest()
        st.get_best_server()                # pick closest test server
        download = st.download()            # bits/sec
        upload   = st.upload()
        ping      = st.results.ping        # ms
    except KeyboardInterrupt:
        print(f'{Colors.RED}Internet connection interrupted.{Colors.RESET}')
        successful = False
    except Exception as e:
        print(f'{Colors.RED}Internet connection error. {Colors.RESET}')
        successful = False

    clear_last_lines(1)
    if successful:
        print(neon_text(f'Download: {download/1e6:.2f} Mbps'))
        print(neon_text(f'Upload: {upload/1e6:.2f} Mbps'))
        print(neon_text(f'Ping: {ping:.1f} ms'))
        if download/1e6 < 10 and upload/1e6 < 10 and ping > 50:
            print(f'Conclusion: {Colors.RED}Your internet connection is unstable or slow.{Colors.RESET}')
    """
    print(f"Download: {download/1e6:.2f} Mbps")
    print(f"Upload:   {upload/1e6:.2f} Mbps")
    print(f"Ping:     {ping:.1f} ms")
    """


def unknown_command(command_original, app_name=None):
    """
    This function handles unknown commands by suggesting the closest command
    from the predefined list, using Levenshtein distance.
    """
    parts = command_original.strip().split()
    if not parts:
        return

    if app_name is None:
        # Compare full commands
        closest = min(commands, key=lambda cmd: levenshtein(command_original, cmd))
        print(f'{Colors.RED}Unknown command: "{parts[0]}". Did you mean "{closest}"?{Colors.RESET}')

    elif app_name == 'todo':
        # Suggest a todo subcommand
        pool = [c.split(' ', 1)[1] for c in commands if c.startswith('todo ')]
        target = parts[1] if len(parts) > 1 else ''
        closest = min(pool, key=lambda sub: levenshtein(target, sub))
        print(f'{Colors.RED}Unknown TODO command: "{target}". Did you mean "todo {closest}"?{Colors.RESET}')

    elif app_name == 'check':
        # Suggest a checklist subcommand
        pool = [c.split(' ', 1)[1] for c in commands if c.startswith('check ')]
        target = parts[1] if len(parts) > 1 else ''
        closest = min(pool, key=lambda sub: levenshtein(target, sub))
        print(f'{Colors.RED}Unknown checklist command: "{target}". Did you mean "check {closest}"?{Colors.RESET}')

    elif app_name == 'settings':
        # Suggest a settings subcommand
        pool = [c.split(' ', 1)[1] for c in commands if c.startswith('settings ')]
        target = parts[1] if len(parts) > 1 else ''
        closest = min(pool, key=lambda sub: levenshtein(target, sub))
        print(f'{Colors.RED}Unknown settings command: "{target}". Did you mean "settings {closest}"?{Colors.RESET}')


def _safe_load_json(file_path, fallback):
    """
    Safely loads a JSON file. If the file is missing, empty, or invalid, returns fallback.
    """
    try:
        if not os.path.exists(file_path):
            return fallback
        if os.path.getsize(file_path) == 0:
            return fallback
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return fallback


def _format_todos_for_llm(todos):
    """
    Converts the todos data into a compact Markdown section for Claude.
    """
    lines = ['## Todos']

    if not todos:
        lines.append('No todos.')
        return lines

    if isinstance(todos, dict):
        todo_items = todos.get('todos', todos.get('items', todos.get('data', [])))
    else:
        todo_items = todos

    if not todo_items:
        lines.append('No todos.')
        return lines

    if isinstance(todo_items, dict):
        todo_items = list(todo_items.values())

    for item in todo_items:
        if isinstance(item, dict):
            text = (
                item.get('text')
                or item.get('task')
                or item.get('title')
                or item.get('name')
                or str(item)
            )
            done = bool(item.get('done', item.get('completed', item.get('checked', False))))
            mark = 'x' if done else ' '
            lines.append(f'- [{mark}] {text}')
        else:
            lines.append(f'- [ ] {item}')

    return lines


def _format_notes_for_llm(notes):
    """
    Converts the notes data into a compact Markdown section for Claude.
    """
    lines = ['## Notes']

    if not notes:
        lines.append('No notes.')
        return lines

    if isinstance(notes, dict):
        note_items = notes.get('notes', notes.get('items', notes.get('data', [])))
    else:
        note_items = notes

    if not note_items:
        lines.append('No notes.')
        return lines

    if isinstance(note_items, str):
        note_items = [line for line in note_items.splitlines() if line.strip()]

    if isinstance(note_items, dict):
        note_items = list(note_items.values())

    for i, note in enumerate(note_items, start=1):
        if isinstance(note, dict):
            title = note.get('title') or note.get('name') or f'Note {i}'
            body = note.get('body') or note.get('text') or note.get('content') or ''
            lines.append(f'### {title}')
            if body:
                lines.append(str(body))
        else:
            lines.append(f'{i}. {note}')

    return lines


def _format_checklists_for_llm(checklists):
    """
    Converts checklist data into a compact Markdown section for Claude.
    """
    lines = ['## Checklists']

    if not checklists:
        lines.append('No checklists.')
        return lines

    if isinstance(checklists, dict):
        checklist_groups = checklists.get('checklists', checklists.get('items', checklists))
    else:
        checklist_groups = checklists

    if isinstance(checklist_groups, list):
        for group_index, group in enumerate(checklist_groups, start=1):
            if isinstance(group, dict):
                name = group.get('name') or group.get('title') or f'Checklist {group_index}'
                items = group.get('items') or group.get('tasks') or group.get('sections') or []
            else:
                name = f'Checklist {group_index}'
                items = [group]

            lines.append(f'### {name}')
            _append_checklist_items(lines, items)
        return lines

    if isinstance(checklist_groups, dict):
        if all(isinstance(value, bool) for value in checklist_groups.values()):
            for name, checked in checklist_groups.items():
                mark = 'x' if checked else ' '
                lines.append(f'- [{mark}] {name}')
        else:
            for name, items in checklist_groups.items():
                lines.append(f'### {name}')
                _append_checklist_items(lines, items)
        return lines

    lines.append(str(checklist_groups))
    return lines


def _append_checklist_items(lines, items):
    """
    Appends checklist items to a Markdown line list.
    """
    if not items:
        lines.append('- [ ] No items.')
        return

    if isinstance(items, dict):
        items = list(items.values())

    if not isinstance(items, list):
        items = [items]

    for item in items:
        if isinstance(item, dict):
            text = (
                item.get('text')
                or item.get('task')
                or item.get('title')
                or item.get('name')
                or str(item)
            )
            checked = bool(item.get('checked', item.get('done', item.get('completed', False))))
            mark = 'x' if checked else ' '
            lines.append(f'- [{mark}] {text}')
        else:
            lines.append(f'- [ ] {item}')


def concatonate_files():
    """
    Creates one Claude-readable Markdown overview file from todos, notes, and checklists.
    The source JSON files remain the source of truth; LLM_data.md is only a generated snapshot.
    """
    user_data_dir = os.path.dirname(user_data.TODO_FILE_LOC)
    llm_file_path = os.path.join(user_data_dir, 'LLM_data.md')

    todos = _safe_load_json(user_data.TODO_FILE_LOC, [])
    notes = _safe_load_json(user_data.NOTES_FILE_LOC, [])
    checklists = _safe_load_json(user_data.CHECKLIST_FILE_LOC, [])

    overview_lines = [
        '# El Pulpo Current Context',
        '',
        f'Generated at: {time.strftime("%Y-%m-%d %H:%M:%S")}',
        '',
    ]

    overview_lines.extend(_format_todos_for_llm(todos))
    overview_lines.append('')
    overview_lines.extend(_format_notes_for_llm(notes))
    overview_lines.append('')
    overview_lines.extend(_format_checklists_for_llm(checklists))

    overview_text = '\n'.join(overview_lines)

    try:
        with open(llm_file_path, 'w', encoding='utf-8') as f:
            f.write(overview_text)
    except OSError:
        pass


def main():
    """
    This is the main function that runs the program.
    :return: void
    """
    analyze_input(input(f"{neon_text('>>>',randomness=False,neon_map_num=4)}{Colors.RESET}"))
    concatonate_files()

if __name__ == "__main__":
    try:
        for i in range(12):
            clear_screen(text=False,randomness=False,clear_technique='ascii')
            print(neon_text(maintext,randomness=False,neon_map_num=i))
            time.sleep(0.05)
        clear_screen(text=True,randomness=False,internet_indicator=False)
    except KeyboardInterrupt:
        clear_screen(text=False)
        print(neon_text(goodbye_text))
        sys.exit(0)

    while True:
        try:
            main()
        except KeyboardInterrupt:
            clear_screen(text=False)
            print(neon_text(goodbye_text))
            break
        # Catch the specific control+d exception
        except EOFError:
            clear_screen(text=False)
            print(neon_text(goodbye_text))
            break
