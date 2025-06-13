import subprocess
import time
import sys
import math
import os
import json
import user_data
import random

class Colors:
    ORANGE = "\033[38;5;208m"
    RESET = "\033[0m"
    RED = "\033[31m"

help_content = ('Type "todo help" to see the commands for the TODO app.'
              '\nType open <App Name> to open the desired application.'
              '\nType "exit" to exit the program.'
              '\nType "chat" to access the LLM.'
              '\nType eval <expression> to evaluate a mathematical expression.'
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

def neon_text(text,randomness=True):
    """
    Returns the text with neon colors.
    If randomness is True, it will randomly choose a color for each character.
    If randomness is False, it will use a fixed color for each character.
    """
    if randomness:
        return "".join(f"{random.choice(neon_colors)}{char}"for char in text) + Colors.RESET
    else:
        return ''.join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate(text))

commands = ['todo','todo ls','todo add','help','exit','chat','quit','open','todo rm','todo changeorder',
            'todo abcorder','todo cbaorder','todo do', 'todo help', 'todo add', 'todo ls', 'todo rm all',
            'eval','clear','clr','open']

def analyze_input(text_input):
    command_arr = [n for n in text_input.lower().split(' ') if n != '']
    command_original = ' '.join(text_input.strip().split())
    command_lower = command_original.lower()

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
                        todo_ls()
                    case 'rm':
                        if len(command_arr) == 3 and command_arr[2] == 'all':
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
                    case _:
                        print(f'{Colors.RED}Unknown TODO command: "{command_arr[1]}". '
                              f'Did you mean "{min(commands, key=lambda cmd: sum(1 for a, b in zip(cmd, command_lower)
                                                                                 if a != b) + abs(len(cmd) - len(command_lower)))}"?'
                                                                                f'{Colors.RESET}')
            else:
                todo_help()
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
        case 'exit' | 'quit':
            if len(command_arr) == 1:
                clear_screen(text=False)
                print(neon_text(goodbye_text))
                sys.exit(0)
            else:
                print(f'{Colors.RED}Error: The "exit" command does not take any arguments.{Colors.RESET}')
        case 'clear' | 'clr':
            if len(command_arr) == 1:
                clear_screen()
            else:
                print(f'{Colors.RED}Error: The "clear" command does not take any arguments.{Colors.RESET}')
        case 'eval':
            if len(command_arr) > 1:
                try:
                    result = eval(command_lower[5:].replace('pi', str(math.pi))
                                  .replace('e', str(math.e))
                                  .replace('^', '**'))
                    if isinstance(result, (int, float)):
                        print(f"{result:,}")
                    else:
                        print(result)
                except Exception:
                    print(f'{Colors.RED}Error: Invalid expression. Please use the format "eval <math_expression>".{Colors.RESET}')
            else:
                print(f'{Colors.RED}Error: The "eval" command requires an expression to evaluate.{Colors.RESET}')
        case _:
            unknown_command(command_original)

def clear_last_lines(n):
    """Move cursor up n lines and clear each of them."""

    for _ in range(n):
        # Move cursor up one line
        sys.stdout.write('\x1b[1A')
        # Clear entire line
        sys.stdout.write('\x1b[2K')

def clear_screen(text = True):
    """Clear the terminal screen."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/Mac
        os.system('clear')
    if text:
        print(f"{neon_text(maintext)}\033[0m")  # Header


todo_list = []
def update_todo_list():
    global todo_list
    if os.path.exists(user_data.DATA_FILE):
        with open(user_data.DATA_FILE, "r", encoding="utf-16") as f:
            try:
                todo_list = json.load(f)
            except json.JSONDecodeError:
                todo_list = []
    else:
        todo_list = []

update_todo_list()

def todo_save():
    with open(user_data.DATA_FILE, "w", encoding="utf-16") as f:
        json.dump(todo_list, f, ensure_ascii=False, indent=2)

def todo_help():

    print('Type "todo ls" for viewing the TODO list'
        '\nType "todo add <new TODO element>" to add new todo element to the list.'
        '\nType "todo rm <Desired Target>" to delete the desired target.'
        '\nType "todo rm" to view deleting todo elements'
        '\nType "todo changeorder" to change the order of two TODO elements.'
        '\nType "todo abcorder" to sort the TODO list in alphabetical order.'
        '\nType "todo cbaorder" to sort the TODO list in reverse alphabetical order.')

def todo_list_view():
    update_todo_list()
    print('My TODO List Content:')
    for i in range(len(todo_list)):
        print(f'{i+1}: {todo_list[i]}')

def todo_ls():
    global todo_list
    update_todo_list()
    if not len(todo_list) == 0:
        todo_list_view()
    else:
        print('Your TODO list is empty.')

def todo_delete_function(command_original):
    global todo_list
    command_lower = command_original.lower()

    if not len(todo_list) == 0:
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

                for index in indexes:
                    try:
                        item = todo_list[int(index)-1]
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


def todo_add(command_original):
    item = command_original[len('todo add '):]
    if item not in todo_list and item != '':
        todo_list.append(item)
        print(f'Added new TODO item: {item}')
        todo_save()
    elif command_original[9:] == '':
        print(f"{Colors.RED}Error: You need to provide a name for the TODO item.{Colors.RESET}")
    else:
        print(f'{Colors.RED}Error: The item "{item}" already exists in your TODO list.{Colors.RESET}')

def todo_changeorder():
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
    global todo_list
    todo_list = sorted(todo_list, key=lambda x: x.lower())
    todo_save()
    print('TODO list sorted in alphabetical order.')
def todo_cbaorder():
    global todo_list
    todo_list = sorted(todo_list, key=lambda x: x.lower(), reverse=True)
    todo_save()
    print('TODO list sorted in reverse alphabetical order.')

def todo_do_function():
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
        for i in range(time_minutes):
            for j in range(240):
                print(neon_text(f'Starting work on "{todo_list[index]}" for {time_minutes} minutes.\nMinutes: {i}, Seconds: {int(j/4)}, Percentage: {((i * 60 + j/4) / (time_minutes * 60)) * 100:.2f}%'))
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
    with open(f'{user_data.PROJECT_LOCATION}/worklogs.txt', "a") as f:
        f.write(f'{message}\n')

def open_function(command_original):
    """
    This is a function to open applications on the system.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return:
    """
    app_name = command_original[5:]
    try:
        subprocess.run(['open', '-a', app_name], check=True)
    except subprocess.CalledProcessError:
        time.sleep(0.1)
    else:
        print(f'Opened "{app_name.capitalize()}".')


def chat_function():
    """
    This function is a placeholder for the AI chat functionality. #TODO: Implement the AI chat feature.
    """
    print(f'{Colors.RED}This feature is  not implemented yet.{Colors.RESET}')

def unknown_command(command_original):
    command_arr = command_original.split(' ')
    if command_original == "":
        return
    # Find the closest command
    closest_command = min(commands, key=lambda cmd: sum(1 for a, b in zip(cmd, command_original) if a != b) + abs(len(cmd) - len(command_original)))
    print(f'{Colors.RED}Unknown command: "{command_arr[0]}". Did you mean "{closest_command}"?{Colors.RESET}')


def main():
    analyze_input(input("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate('>>> ')) + "\033[0m").strip())

if __name__ == "__main__":
    print(f'{neon_text(maintext)}')  # Header
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
