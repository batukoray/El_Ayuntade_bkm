import subprocess
import time
import sys
import math
import os
import json
from warnings import catch_warnings
import user_data
import random
import io
import socket
import speedtest
from simpleeval import simple_eval
from gtts import gTTS
from googletrans import Translator
import asyncio
import Levenshtein
import pyautogui

from todo_app import *
from checklist_app import *

from utils import *



def set_command_variables(text_input:str) -> []:
    """
    This function takes a text input and returns a list containing the command array, the original command, and the lowercased command.
    :param text_input:
    :return:
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
        clear_screen(text=True,randomness=True,clear_technique='ascii')
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
        case 'chat':
            if len(command_arr) == 1:
                chat_function()
            else:
                print(f'{Colors.RED}Error: The "chat" command does not take any arguments.{Colors.RESET}') # TODO: Maybe it will take arguments in the future.
        case 'tts':
            text_to_speech_function(command_original)
        case 'tr':
            translate_function(command_original)
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
            unknown_command(command_original)

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

def clear_screen(text = True,randomness=True,clear_technique='os',subtitle=None):
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
        if text:
            print(f"{neon_text(maintext,randomness)}\033[0m")  # Header
            if subtitle is not None:
                clear_last_lines(2)
                print(f"{neon_text('App working with internet connection.' if is_connected_socket() else 'App working without internet connection.' ,randomness)}{Colors.RESET}\n")
    elif clear_technique == 'ascii':
        clear_last_lines(100)
        if text:
            print(f"{neon_text(maintext,randomness)}\033[0m")
            if subtitle is not None:
                print(f"{neon_text(subtitle,randomness)}\033[0m")
    else:
        raise Exception(f'The clear technique "{clear_technique}" is not supported.')


# TODO APP WAS HERE.



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


settings_defaults = {'openappstayontab': False,'default_ollama_model':'deepseek-r1'}  # Default settings

settings_dict = {'openappstayontab': False,'default_ollama_model': 'llama3.2'}
settings_names = ['openappstayontab', 'default_ollama_model']

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
    try:
        subprocess.run(['open', '-a', app_name], check=True)
        update_settings()
        if settings_dict.get('openappstayontab', False):
            current_mouse_loc_x = pyautogui.position().x
            current_mouse_loc_y = pyautogui.position().y
            width, height = pyautogui.size()
            time.sleep(0.3)
            pyautogui.click(x=width / 2, y=height / 2)
            pyautogui.moveTo(x=current_mouse_loc_x, y=current_mouse_loc_y)
    except subprocess.CalledProcessError:
        time.sleep(0.1)
    else:
        print(f'Opened "{app_name.capitalize()}".')

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

import subprocess

def get_ollama_response(prompt: str) -> str:
    # Run ollama, capture its stdout, and decode it as text
    result = subprocess.run(
        ["ollama", "run", settings_dict['default_ollama_model'], f'{chat_logs_llm} {prompt}'],
        capture_output=True,  # capture both stdout & stderr
        text=True,            # return strings instead of bytes
        check=True            # raise CalledProcessError on non-zero exit
    )
    return result.stdout.strip()  # the AI’s reply as a string

chat_logs_llm = ""

def remove_all_thinks(text, start_tag="<think>", end_tag="</think>"):
    while True:
        start = text.find(start_tag)
        if start == -1:
            break
        end = text.find(end_tag, start + len(start_tag))
        if end == -1:
            break
        text = text[:start] + text[end + len(end_tag):]
    return text.replace('\n', '').replace('<think>', '').replace('</think>', '').strip()

def chat_function():
    """
    This function launches an interactive AI chat loop using ollama.
    The user can type messages, and 'exit' or 'quit' to leave chat mode.
    """
    global chat_logs_llm
    waiting_messages = [
        "Pondering the possibilities…",
        "Consulting the data streams…",
        "Crunching the cosmic numbers…",
        "Tuning my neural circuits…",
        "Summoning the answer…",
        "Aligning the quantum bits…",
        "Brewing up a response…",
        "Digging through the archives…",
        "Tuning into the mainframe…",
        "Gearing up intelligence…",
        "Mapping the knowledge graph…",
        "Verifying hypotheses…",
        "Gazing into the algorithmic void…",
        "Honing in on clarity…",
        "Orchestrating wisdom…",
    ]
    prompt = ('Your main purpose is to answer the user\'s questions and being helpful.\n'
              'Avoid long answers; but if the user asks for a long answer, you can give it.\n'
              'You are an assistant, and you will answer the user\'s questions in a friendly manner.\n')

    print(neon_text('LLM chat mode activated. Type "exit" or "quit" to exit the LLM.'))
    while True:
        try:
            user_input = input(f'{neon_text('You:')} {Colors.LIGHT_GRAY}')
            chat_logs_llm += 'User: ' + user_input + "\n"
        except (EOFError, KeyboardInterrupt):
            try:
                subprocess.run(["pkill", "-f", 'Ollama 2'], check=True)
            except subprocess.CalledProcessError:
                continue
            print()
            break
        if user_input.strip().lower() in ("exit", "quit"):
            try:
                subprocess.run(["pkill", "-f", 'Ollama 2'], check=True)
            except subprocess.CalledProcessError:
                continue
            print("Exiting chat mode.")
            break
        try:
            print(neon_text(random.choice(waiting_messages)))
            ollama_answer = get_ollama_response(f'{prompt} {user_input}')
            chat_logs_llm += 'AI: ' + remove_all_thinks(ollama_answer) + "\n"
            clear_last_lines(1)
            print(f"{neon_text('AI:')} {Colors.LIGHT_GRAY}{remove_all_thinks(ollama_answer)}{Colors.RESET}")
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}Error: Chat command failed.{Colors.RESET}")

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
    :param print_log: If True, it will print the log message after playing the text to speech. True in default.
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
            os.system('start -q speech.mp3')
        else:  # For Unix/Linux/Mac
            os.system('mpg123 -q speech.mp3')
    except FileNotFoundError:
        print(f'{Colors.RED}Error: Could not find the audio player. Please install mpg123 or use a different audio player.{Colors.RESET}')
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
            result = asyncio.run(_do_translate(text, 'en')).text
            print(f'En: "{neon_text(result)}"')
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

def main():
    """
    This is the main function that runs the program.
    :return: void
    """
    analyze_input(input(f'{neon_text('>>>')}{Colors.RESET}'))

if __name__ == "__main__":
    try:
        for i in range(12):
            clear_screen(text=False,randomness=True,clear_technique='ascii')
            print(neon_text(maintext,randomness=False,neon_map_num=i))
            time.sleep(0.05)
        clear_screen(text=True,randomness=False,subtitle='Haha this is working')

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
