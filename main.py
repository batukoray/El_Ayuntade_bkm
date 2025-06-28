import subprocess
import time
import sys
import math
import os
import json
import user_data
import random
import io

from PIL.SpiderImagePlugin import iforms
from simpleeval import simple_eval
import pywhatkit as kit
from gtts import gTTS
from wikipedia import languages
from googletrans import Translator
import asyncio
import Levenshtein
import pyautogui


class Colors:
    """
    This class contains color codes for terminal text formatting.
    """
    RESET = '\033[0m'
    RED = '\033[31m'

help_content = ('Type "todo help" to see the commands for the TODO app.'
              '\nType "check help" to see the commands for the Checklist app.'
              '\nType open <App Name> to open the desired application.'
              '\nType "exit" to exit the program.'
              '\nType "chat" to access the LLM.'
              '\nType eval <expression> to evaluate a mathematical expression.'
              '\nType "tts <text>" to convert text to speech.'
              '\nType "tr <text> -> <language>" to translate text to a specified language.'
              '\nType "tr <text>" to translate text to English.'
              '\nType "send <phone_number> <message>" to send a WhatsApp message.'
              '\nType "settings help" to see the commands for the Settings app.'
              '\nType "animate" or "animation" or "anim" to see the animated logo.'
              '\nType "clear" or "clr" to clear the screen.'
              '\nType "help" to see this help message again.'
              '\nType "quit" to exit the program.')

# Color theme of the program:
neon_colors = ["\033[35m", "\033[95m","\033[94m",  "\033[94m"]

maintext = r"""
██████  ██╗╔═██ ╔███    ███╗
██═╬═██ ██╚╝██╝ ║████  ████║
██████  █████   ║██╗████╔██║      El Ayuntade By:
██═╬═██ ██╔╗██╗ ║██╚╗██╔╝██║     Batu Koray Masak
██████  ██╝╚═██ ╚██ ╚══╝ ██╝

Type "help" to see the available commands.

"""
goodbye_text = 'Goodbye! | El Ayuntade By: Batu Koray Masak'

def neon_text(text,randomness=True,neon_map_num = 0):
    """
This function takes a text input and returns it with neon colors applied to each character.
    :param text: The text to be colored.
    :param randomness: If True, each character will be colored randomly from the neon_colors list.
    :param neon_map_num: An integer used to map the colors in a specific order.
    :return: A string with neon colors applied to each character.
    """
    if randomness:
        return ''.join(f"{random.choice(neon_colors)}{char}"for char in text) + Colors.RESET
    else:
        return ''.join(f"{neon_colors[(j-neon_map_num) % len(neon_colors)]}{char}" for j, char in enumerate(text))

commands = ['todo','todo ls','todo add','help','exit','chat','quit','open','todo rm','todo changeorder',
            'todo abcorder','todo cbaorder','todo do', 'todo help', 'todo add', 'todo ls', 'todo rm all',
            'eval','clear','clr','open', 'check', 'check ls', 'check add', 'check rm', 'check help', 'check -check', 'check -uncheck', 'animate', 'animation', 'anim','you found the easter egg!']

def analyze_input(text_input):
    """
    This function analyzes the input text and executes the corresponding command.
    :param text_input: The input text from the user.
    :return: void
    """
    command_arr = [n for n in text_input.lower().split(' ') if n != '']
    command_original = ' '.join(text_input.strip().split())
    command_lower = command_original.lower()

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
                        if len(command_arr) == 3 and command_arr[2] == 'all':
                            if not todo_list:
                                print('Your TODO list is already empty.')
                            else:
                                todo_list.clear()
                                todo_save()
                                print('All items were deleted.')
                        else:
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
                        if len(command_arr) == 3 and command_arr[2] == 'all':
                            if not checklist_dict:
                                print('Your checklist is already empty.')
                            else:
                                checklist_dict.clear()
                                checklist_save()
                                print('All items were deleted from the checklist.')
                        else:
                            checklist_delete_function(command_original)
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
            # TODO: Complete the notes app asap.

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
            else:
                settings_help()

        case 'open':
            if len(command_arr) > 1:
                open_function(command_original)
            else:
                print(f'{Colors.RED}Error: You need to specify an application to open.{Colors.RESET}')
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
        case 'send':
            send_whatsapp_function(command_original)
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
            animate_logo(40,arrows=True)
        case _:
            unknown_command(command_original)

def clear_last_lines(n):
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

def clear_screen(text = True,randomness=True,clear_technique='os'):
    """
    This function clears the terminal screen.
    :param text: If True, it will print the main text after clearing the screen.
    :param randomness: If True, the main text will be colored randomly. If False, it will use a fixed color pattern.
    :param clear_technique: The technique to clear the screen. 'os' for using os.system, 'ascii' for using ANSI escape codes.
    :return: void
    """
    if clear_technique == 'os':
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For Unix/Linux/Mac
            os.system('clear')
        if text:
            print(f"{neon_text(maintext,randomness)}\033[0m")  # Header
    elif clear_technique == 'ascii':
        clear_last_lines(100)
        if text:
            print(f"{neon_text(maintext,randomness)}\033[0m")
    else:
        raise Exception(f'The clear technique "{clear_technique}" is not supported.')


# TODO App:
todo_list = []

def update_todo_list():
    """
    This function updates the TODO list by reading from a JSON file.
    :return: void
    """
    global todo_list
    if os.path.exists(user_data.TODO_FILE_LOC):
        with open(user_data.TODO_FILE_LOC, "r", encoding="utf-8") as f:
            try:
                todo_list = json.load(f)
            except json.JSONDecodeError:
                todo_list = []
    else:
        todo_list = []

update_todo_list()

def todo_save():
    """
    This function saves the current TODO list to a file in JSON format.
    :return: void
    """
    with open(user_data.TODO_FILE_LOC, "w", encoding="utf-8") as f:
        json.dump(todo_list, f, ensure_ascii=False, indent=2)

def todo_help():
    """
    This function displays the help content for the TODO app.
    :return: void
    """

    print('Type "todo ls" for viewing the TODO list'
        '\nType "todo add <new TODO element>" to add new todo element to the list.'
        '\nType "todo rm <Desired Target>" to delete the desired target.'
        '\nType "todo rm <Desired Index>" to delete the desired index.'
        '\nType "todo rm all" to delete all items from the TODO list.'
        '\nType "todo rm" to view deleting todo elements'
        '\nType "todo changeorder" to change the order of two TODO elements.'
        '\nType "todo abcorder" to sort the TODO list in alphabetical order.'
        '\nType "todo cbaorder" to sort the TODO list in reverse alphabetical order.')

def todo_list_view():
    """
    This function displays the current content of the TODO list.
    :return: void
    """
    update_todo_list()
    if not todo_list:
        print('Your TODO list is empty.')
        return
    print('My TODO List Content:')
    for j in range(len(todo_list)):
        print(f'{j+1}: {todo_list[j]}')

def todo_add(command_original):
    """
    This function adds a new item to the TODO list based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    item = command_original[len('todo add '):]
    if item.isdigit():
        print(f'{Colors.RED}Error: The item name cannot be a number.{Colors.RESET}')
        return
    if item not in todo_list and item != '':
        todo_list.append(item)
        print(f'Added new TODO item: {item}')
        todo_save()
    elif command_original[9:] == '':
        print(f"{Colors.RED}Error: You need to provide a name for the TODO item.{Colors.RESET}")
    else:
        print(f'{Colors.RED}Error: The item "{item}" already exists in your TODO list.{Colors.RESET}')

def todo_delete_function(command_original):
    """
    This function deletes an item from the TODO list based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    global todo_list
    command_lower = command_original.lower()

    if not len(todo_list) == 0:
        if command_lower[len('todo rm '):].isdigit():
            try:
                index = int(command_original[8:]) - 1
                if 0 <= index < len(todo_list):
                    item = todo_list[index]
                    todo_list.remove(item)
                    print(f'Item "{item}" was deleted.')
                    todo_save()
                else:
                    print(f'{Colors.RED}Error: Index out of range.{Colors.RESET}')
            except ValueError:
                print(f'{Colors.RED}Error: Invalid input. Please enter a valid index.{Colors.RESET}')
            return
        if command_lower != 'todo rm':
            try:
                todo_list.remove(command_original[8:])
            except ValueError:

                try:
                    todo_list.remove(command_lower[8:])
                except ValueError:
                    try:
                        todo_list.remove(command_original[8:].capitalize())
                    except ValueError:
                        print(f'{Colors.RED}{command_lower[8:]} was not found.{Colors.RESET}')
                    else:
                        print(f'{command_original[8:]} was deleted.')
                else:
                    print(f'{command_original[8:]} was deleted.')
            else:
                print(f'{command_original[8:]} was deleted.')
        else:
            todo_list_view()
            indexes = input(  '\nType the index/indexes of the TODO list content or the name of the item that you want to delete. '
                              '\nSeparate the desired indexes with ",".'
                              '\nType "all" to delete all items.'
                              '\nType "exit" if you want to exit.\n')

            if not indexes.lower() == 'exit' and not indexes.lower() == 'all':
                indexes = indexes.split(',')
                indexes.sort(reverse=True)
                try:
                    if int(max(indexes)) > len(todo_list) or int(min(indexes)) < 1:
                        print(f'{Colors.RED}Error: The index you are trying to delete is out of range.{Colors.RESET}')
                        return
                except ValueError:
                    print(f'{Colors.RED}Error: Invalid input.{Colors.RESET}')
                    return

                for index in indexes:
                    try:
                        item = todo_list[int(index) - 1]
                        if 0 <= int(index) <= len(todo_list):
                            todo_list.remove(todo_list[int(index)-1])
                    except (IndexError, ValueError):
                        print(f'{Colors.RED}Error: The item you are trying to delete does not exist{Colors.RESET}')
                    else:
                        print(f'Item  {item} was deleted.')
            elif indexes.lower() == 'all':
                todo_list.clear()
                print('All items were deleted.')
    else:
        print('Your TODO list is empty.')
    todo_save()

def todo_changeorder():
    """
    This function changes the order of two items in the TODO list based on user input.
    :return: void
    """
    if len(todo_list) < 2:
        print(f'{Colors.RED}You need at least two items in your TODO list to change their order.{Colors.RESET}')
        return
    todo_list_view()
    userinput = input('Type the indexes of two TODO items you want to swap, \nseparated by a comma(e.g., "1,2"): ')

    num1 = userinput.split(',')[0].strip()
    num2 = userinput.split(',')[1].strip()
    try:
        temp = todo_list[int(num1) - 1]
        todo_list[int(num1) - 1] = todo_list[int(num2) - 1]
        todo_list[int(num2) - 1] = temp
        todo_save()
        print(f'Swapped items at indexes {num1} and {num2}.')
    except (IndexError, ValueError):
        print(f'{Colors.RED}Error: Invalid input. Please enter valid indexes.{Colors.RESET}')

def todo_abcorder():
    """
    This function sorts the TODO list in alphabetical order.
    :return: void
    """
    global todo_list
    todo_list = sorted(todo_list, key=lambda x: x.lower())
    todo_save()
    print('TODO list sorted in alphabetical order.')

def todo_cbaorder():
    """
    This function sorts the TODO list in reverse alphabetical order.
    :return: void
    """
    global todo_list
    todo_list = sorted(todo_list, key=lambda x: x.lower(), reverse=True)
    todo_save()
    print('TODO list sorted in reverse alphabetical order.')

def todo_do_function():
    """
    This function allows the user to work on a TODO item for a specified amount of time.
    :return: void
    """
    todo_list_view()

    random1 = random.randint(1,10)
    random2 = random.randint(1,90)
    user_input = input('Type the index of the TODO item you are going to work on, and separate minute time with a comma'
                   f'\n(Ex: Type "{random1}, {random2}" for doing the activity at index {random1} for {random2} minutes.)'
                     '\nType "exit" to exit.\n')

    if user_input.lower() == 'exit':
        return
    try:
        user_input = user_input.strip().split(',')
        index = int(user_input[0]) - 1
        time_minutes = int(user_input[1])
        if index < 0 or index >= len(todo_list):
            print(f'{Colors.RED}Error: Index out of range. Please enter a valid index.{Colors.RESET}')
            return
        if time_minutes <= 0:
            print(f'{Colors.RED}Error: Time must be a positive integer.{Colors.RESET}')
            return

        for j in range(time_minutes):
            for k in range(240):
                print(neon_text(f'Starting work on "{todo_list[index]}" for {time_minutes} minutes.\nMinutes: {j}, Seconds: {int(k/4)}, Percentage: {((j * 60 + k/4) / (time_minutes * 60)) * 100:.2f}%'))
                time.sleep(0.25)
                clear_last_lines(2)
        clear_last_lines(1)
        print(neon_text(f'Finished working on "{todo_list[index]}".'))
        write_worklogs(f'{user_data.username} has finished working on the topic {todo_list[index]} for {time_minutes} minutes.')
        todo_list.pop(index)
        todo_save()

    except (ValueError, IndexError):
        print(f'{Colors.RED}Error: Invalid input format. Please use the format "index,time".{Colors.RESET}')
        return

def write_worklogs(message):
    """
    This function writes a message to the worklogs file.
    :param message: The message to be written to the worklogs file.
    :return: void
    """
    with open(user_data.WORKLOGS_FILE_LOC, "a") as f:
        f.write(message + '\n')


# Checklist App:
checklist_dict = {}

def update_checklist():
    """
    This function updates the checklist items by reading from a JSON file.
    :return: void
    """
    global checklist_dict
    if os.path.exists(user_data.CHECKLIST_FILE_LOC):
        with open(user_data.CHECKLIST_FILE_LOC, "r", encoding="utf-8") as f:
            try:
                checklist_dict = json.load(f)
            except json.JSONDecodeError:
                checklist_dict = {}
    else:
        checklist_dict = {}

update_checklist()

def checklist_save():
    """
    This function saves the current checklist items to a file in JSON format.
    :return: void
    """
    with open(user_data.CHECKLIST_FILE_LOC, "w", encoding="utf-8") as f:
        json.dump(checklist_dict, f, ensure_ascii=False, indent=2)

def checklist_help():
    """
    This function displays the help content for the checklist app.
    :return: void
    """
    print('Type "check ls" to view the checklist items.'
          '\nType "check add <new item>" to add a new item to the checklist.'
          '\nType "check add <item1; item2; item3>" to add multiple items to the checklist.'
          '\nType "check rm <item>" to remove an item from the checklist by its name.'
          '\nType "check rm <item_index>" to remove the referred item from the checklist.'
          '\nType "check rm -checked" to remove all checked items from the checklist.'
          '\nType "check rm -unchecked" to remove all unchecked items from the checklist.'
          '\nType "check rm all" to remove all items from the checklist.'
          '\nType "check help" to see this help message again.'
          '\nType "check -check <item_name or index_of_item>" to mark an item as done.'
          '\nType "check -check <item indexes seperated with commas>" to mark multiple items as done.'
          '\nType "check -check all" to mark all items as done.'
          '\nType "check -uncheck <item_name or index_of_item>" to mark an item as undone.'
          '\nType "check -uncheck <item indexes seperated with commas>" to mark multiple items as undone.'
          '\nType "check -uncheck all" to mark all items as undone.')

def checklist_list_view():
    """
    This function prints the items in the checklist.
    :return: void
    """
    global checklist_dict
    update_checklist()
    if checklist_dict:
        print('Checklist Items:')
        for j in range(len(checklist_dict)):
            item = list(checklist_dict.keys())[j]
            status = '✓' if checklist_dict[item] else '✗'
            print(f'{j + 1}: {item} -> {neon_text(status,randomness=True)}')
    else:
        print('Your checklist is empty.')

def checklist_add(command_original):
    """
    This function adds a new item to the checklist based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    item = command_original[len('check add '):]
    # Check if item is fully numerical:
    if item.isdigit():
        print(f'{Colors.RED}Error: The item name cannot be a number.{Colors.RESET}')
        return
    elif ';' in item:
        item_arr = item.split(';')
        successful = True
        for j in item_arr:
            if j.strip() not in checklist_dict and j.strip() != '':
                checklist_dict[j.strip()] = False
            if j.strip() == '':
                print(f"{Colors.RED}Error: You need to provide a name for the checklist item.{Colors.RESET}")
                successful = False
        checklist_save()
        if successful:
            print(f'Added new checklist items: {", ".join(item_arr)}')

        checklist_save()
    elif item and item not in checklist_dict:
        checklist_dict[item] = False  # Default status is unchecked
        checklist_save()
        print(f'Added new checklist item: {item}')
    elif item == '':
        print(f"{Colors.RED}Error: You need to provide a name for the checklist item.{Colors.RESET}")
    else:
        print(f'{Colors.RED}Error: The item "{item}" already exists in your checklist.{Colors.RESET}')

def checklist_delete_function(command_original):
    """
    This function deletes an item from the checklist based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    global checklist_dict
    command_lower = command_original.lower()

    if not checklist_dict:
        print('Your checklist is empty.')
        return

    if command_lower != 'check rm' and command_lower != 'check rm -checked' and command_lower != 'check rm -unchecked':
        item = command_original[len('check rm '):]
        if item in checklist_dict:
            del checklist_dict[item]
            checklist_save()
            print(f'Item "{item}" was deleted from the checklist.')
        elif item.isdigit():
            try:
                index = int(item) - 1
                if 0 <= index < len(checklist_dict):
                    item_to_delete = list(checklist_dict.keys())[index]
                    del checklist_dict[item_to_delete]
                    checklist_save()
                    print(f'Item "{item_to_delete}" was deleted from the checklist.')
                else:
                    print(f'{Colors.RED}Error: Index out of range.{Colors.RESET}')
            except ValueError:
                print(f'{Colors.RED}Error: Invalid index format.{Colors.RESET}')
        else:
            print(f'{Colors.RED}Error: The item "{item}" was not found in the checklist.{Colors.RESET}')
    elif command_lower == 'check rm':
        checklist_list_view()
        item = input('Type the name of the item you want to delete, or the index of the item you want to delete, or "all" to delete all items: ')
        if item.lower() == 'all':
            checklist_dict.clear()
            checklist_save()
            print('All items were deleted from the checklist.')
        elif item in checklist_dict:
            del checklist_dict[item]
            checklist_save()
            print(f'Item "{item}" was deleted from the checklist.')
        elif item.isdigit():
            try:
                index = int(item) - 1
                if 0 <= index < len(checklist_dict):
                    item_to_delete = list(checklist_dict.keys())[index]
                    del checklist_dict[item_to_delete]
                    checklist_save()
                    print(f'Item "{item_to_delete}" was deleted from the checklist.')
                else:
                    print(f'{Colors.RED}Error: Index out of range.{Colors.RESET}')
            except ValueError:
                print(f'{Colors.RED}Error: Invalid index format.{Colors.RESET}')
        else:
            print(f'{Colors.RED}Error: The item "{item}" was not found in the checklist.{Colors.RESET}')
    elif command_lower == 'check rm -checked':
        items_to_remove = [item for item, checked in checklist_dict.items() if checked]
        if items_to_remove:
            for item in items_to_remove:
                del checklist_dict[item]
            checklist_save()
            print(f'Removed {len(items_to_remove)} checked items from the checklist.')
        else:
            print('No checked items to remove.')
    elif command_lower == 'check rm -unchecked':
        items_to_remove = [item for item, checked in checklist_dict.items() if not checked]
        if items_to_remove:
            for item in items_to_remove:
                del checklist_dict[item]
            checklist_save()
            print(f'Removed {len(items_to_remove)} unchecked items from the checklist.')
        else:
            print('No unchecked items to remove.')

def checklist_mark(command_original,check:bool):
    """
    This function marks an item in the checklist as done or not done based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :param check: A boolean value indicating whether to mark the item as done (True) or not done (False).
    :return: void check -check item
    """
    global checklist_dict
    update_checklist()
    item = command_original[len('check -check '):] if check else command_original[len('check -uncheck '):]
    if item.lower() == 'all':
        for key in checklist_dict.keys():
            checklist_dict[key] = check
        checklist_save()
        print(f'All items marked as {"done" if check else "not done"}.')
        return
    if ',' in item:
        items = item.split(',')
        for j in items:
            j = j.strip()
            if j.isdigit():
                index = int(j) - 1
                if 0 <= index < len(checklist_dict):
                    item_name = list(checklist_dict.keys())[index]
                    checklist_dict[item_name] = check
                    print(f'Marked item "{item_name}" as {"done" if check else "not done"}.')
                else:
                    print(f'{Colors.RED}Error: Index out of range.{Colors.RESET}')
            elif j in checklist_dict:
                checklist_dict[j] = check
                print(f'Marked item "{j}" as {"done" if check else "not done"}.')
            else:
                print(f'{Colors.RED}Error: Item "{j}" not found in the checklist.{Colors.RESET}')
    elif item.isdigit():
        index = int(item) - 1
        if 0 <= index < len(checklist_dict):
            item_name = list(checklist_dict.keys())[index]
            checklist_dict[item_name] = check
            print(f'Marked item "{item_name}" as {"done" if check else "not done"}.')
        else:
            print(f'{Colors.RED}Error: Index out of range.{Colors.RESET}')
    else:
        if item in checklist_dict:
            checklist_dict[item] = check
            print(f'Marked item "{item}" as {"done" if check else "not done"}.')
        else:
            print(f'{Colors.RED}Error: Item "{item}" not found in the checklist.{Colors.RESET}')
    checklist_save()

# TODO: more functions needed

# Checklist app end

# Notes app start

def notes_add(command_original):
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

# Notes app end

# Setting functions start

settings_dict = {'openappstayontab': False}  # Default setting
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

def settings_edit(command_original):
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
        setting_value = False if setting.split(' ')[1].strip() == 'false' else True
    except IndexError:
        print(f'{Colors.RED}Error: You need to provide a value for the setting.{Colors.RESET}')
        return
    except ValueError:
        setting_value = int(setting.split(' ')[1].strip())
    settings_dict[setting_name] = setting_value
    settings_save()
    print(f'Edited setting: {setting_name} with value {setting_value}')

def open_function(command_original):
    """
    This is a function to open applications on the system.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    app_name = command_original[5:]
    try:
        subprocess.run(['open', '-a', app_name], check=True)
        update_settings()
        if settings_dict.get('openappstayontab', False):
            current_mouse_loc_x = pyautogui.position().x
            current_mouse_loc_y = pyautogui.position().y
            width, height = pyautogui.size()
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


def chat_function():
    """
    This function is a placeholder for the AI chat feature.
    :return: void
    """
    print(f'{Colors.RED}This feature is  not implemented yet.{Colors.RESET}')

def send_whatsapp_function(command_original:str):
    message = command_original.split("'")[1].strip()
    reciever = command_original.split('to')[1].split('at')[0].strip()
    timeless = True
    if 'at' in command_original:
        timeless = False
        time = command_original.split('at')[1].strip()
    print(reciever)
    if timeless:
        kit.sendwhatmsg_instantly(reciever,message,wait_time=8,tab_close=True)

def text_to_speech_function(command_original:str):
    """
    This function converts text to speech using gTTS and plays it.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    text= command_original[len('tts '):]
    tts = gTTS(text=text, lang='en')
    tts.save('speech.mp3')
    try:
        if os.name == 'nt':  # For Windows
            os.system('start -q speech.mp3')
        else:  # For Unix/Linux/Mac
            os.system('mpg123 -q speech.mp3')
    except FileNotFoundError:
        print(f'{Colors.RED}Error: Could not find the audio player. Please install mpg123 or use a different audio player.{Colors.RESET}')
    else:
        print(f'Played audio for: "{neon_text(text)}"')
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

    # Ensure the user typed "text -> lang"
    text = cmd.split('->')[0].strip()
    if '->' not in cmd:
        try:
            async def _do_translate(t, lang):
                tr = Translator()
                return await tr.translate(t, dest=lang)


            result = asyncio.run(_do_translate(text, 'en'))
            print(result.text)
        except Exception as e:
            print(f"{Colors.RED}Translation failed: {e}{Colors.RESET}")
        return

    text, language = map(str.strip, cmd.split('->', 1))
    try:
        async def _do_translate(t, lang):
            tr = Translator()
            return await tr.translate(t, dest=lang)
        result = asyncio.run(_do_translate(text, language))
        print(result.text)
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

def main():
    """
    This is the main function that runs the program.
    :return: void
    """
    analyze_input(input(neon_text('>>>')))

if __name__ == "__main__":
    try:
        for i in range(12):
            clear_screen(text=False,randomness=True,clear_technique='ascii')
            print(neon_text(maintext,randomness=False,neon_map_num=i))
            time.sleep(0.05)
        clear_screen(text=True,randomness=False)
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
