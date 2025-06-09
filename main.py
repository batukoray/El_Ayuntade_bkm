import subprocess
import time
import sys
import builtins
import math
import os
import json
import random



user_prompt = 'Enter a TODO.'
help_content =('   Type todo help to see the commands for the TODO app.'
                '\nType open <App Name> to open the desired application.'
                '\nType "exit" to exit the program.'
                '\nType "chat" to access the LLM.')
# Updated neon colors: purple, pink, navy blue, light green, gold
neon_colors = [
    "\033[35m",  # purple
    "\033[95m",  # bright pink
    "\033[94m",  # bright navy blue
    "\033[94m",  # bright light green
]
text = r"""
██████  ██╗╔═██ ╔███    ███╗
██═╬═██ ██╚╝██╝ ║████  ████║
██████  █████   ║██╗████╔██║
██═╬═██ ██╔╗██╗ ║██╚╗██╔╝██║
██████  ██╝╚═██ ╚██ ╚══╝ ██╝

Robot Human Assist By: Batu Koray Masak

Type "help" to see the available commands.
"""
colored_text = "".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate(text))
print(f"{colored_text}\033[0m")  # Neon cyperpunk header

commands = ['todo ls','todo del','todo add','help','exit','chat','quit']
command = ''

line_count = 0
_orig_print = builtins.print


def print(*args, **kwargs):
    """
    Overrides the built-in print to count how many lines are output.
    Each call to print() is counted as at least one line, plus any embedded '\n'.
    """
    global line_count
    # Call the real print
    _orig_print(*args, **kwargs)

    # Estimate printed lines
    sep = kwargs.get("sep", " ")
    text = sep.join(str(a) for a in args)
    printed_lines = text.splitlines() or [""]
    line_count += len(printed_lines)

# Monkey-patch builtins.print
builtins.print = print

def clear_last_lines(n=1):
    """Move cursor up n lines and clear each of them."""
    global line_count
    for _ in range(n):
        # Move cursor up one line
        sys.stdout.write('\x1b[1A')
        # Clear entire line
        sys.stdout.write('\x1b[2K')
    line_count -= n

todo_list = []
DATA_FILE = "/Users/batukoraymasak/PycharmProjects/todo_app/todos.json"
def update_todo_list():
    global todo_list
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-16") as f:
            try:
                todo_list = json.load(f)
            except json.JSONDecodeError:
                todo_list = []
    else:
        todo_list = []

update_todo_list()

def todo_save_todos():
    with open(DATA_FILE, "w", encoding="utf-16") as f:
        json.dump(todo_list, f, ensure_ascii=False, indent=2)

def todo_help():

    print('Type "todo ls" for viewing the TODO list'
        '\nType "todo add <new TODO element>" to add new todo element to the list.'
        '\nType "todo rm <Desired Target> to delete the desired target.'
        '\nType "todo rm" to view deleting todo elements'
        '\nType "todo changeorder to change the order of two TODO elements.'
        '\nType "todo abcorder" to sort the TODO list in alphabetical order.'
        '\nType "todo cbaorder" to sort the TODO list in reverse alphabetical order.')

def todo_list_view():
    update_todo_list()
    print('My TODO List Content:')

    for i in range(len(todo_list)):
        print(f'{i+1}: {todo_list[i]}')
def todo_ls():
    global todo_list
    if not len(todo_list) == 0:
        todo_list_view()
    else:
        print('Your TODO list is empty.')

def todo_delete_function():
    global line_count
    if not len(todo_list) == 0:
        if len(command) != 7:
            try:
                todo_list.remove(command[8:])
            except ValueError:
                print(f'{command[8:]} was not found.')
            else:
                print(f'{command[8:]} was deleted.')
        else:
            todo_list_view()
            indexes = input(  'Type the index/indexes of the TODO list content or the name of the item that you want to delete. '
                            '\nSeperate the desired indexes with ",".'
                            '\nType "all" to delete all items.'
                            '\nType "exit" if you want to exit.\n')
            line_count += 6
            if not indexes.lower() == 'exit' and not indexes.lower() == 'all':
                indexes = indexes.split(',')
                indexes.sort(reverse=True)

                for index in indexes:
                    try:
                        item = todo_list[int(index)-1]
                        todo_list.remove(todo_list[int(index)-1])
                    except:
                        print('Error: The item you are trying to delete does not exist.')
                    else:
                        print(f'Item  {item} was deleted.')
            elif indexes.lower() == 'all':
                todo_list.clear()
                print('All items were deleted.')
    else:
        print('Your TODO list is empty.')

    todo_save_todos()


def todo_add():
    global commandoriginal
    if commandoriginal[9:] not in todo_list:
        todo_list.append(commandoriginal[9:])
        print(f'Added new TODO item: {commandoriginal[8:]}')
        todo_save_todos()
    else:
        print(f'Error: The item "{command[9:]}" already exists in your TODO list.')

def todo_changeorder():
    global line_count
    if len(todo_list) < 2:
        print('You need at least two items in your TODO list to change their order.')
        return
    todo_list_view()
    userinput = input('Type the indexes of the two TODO items you want to swap, separated by a comma (e.g., "1,2"): ')
    line_count += 2
    num1 = userinput.split(',')[0].strip()
    num2 = userinput.split(',')[1].strip()
    try:
        temp = todo_list[int(num1) - 1]
        todo_list[int(num1) - 1] = todo_list[int(num2) - 1]
        todo_list[int(num2) - 1] = temp
    except (IndexError, ValueError):
        print('Error: Invalid input. Please enter valid indexes.')

def todo_abcorder():
    global todo_list
    todo_list = sorted(todo_list, key=lambda x: x.lower())
    print('TODO list sorted in alphabetical order.')
def todo_cbaorder():
    global todo_list
    todo_list = sorted(todo_list, key=lambda x: x.lower(), reverse=True)
    print('TODO list sorted in reverse alphabetical order.')

def todo_do_function():
    todo_list_view()
    global line_count
    random1 = random.randint(1,10)
    random2 = random.randint(1,90)
    user_input = input('Type the index of the TODO item you are going to work on, and separate minute time with a comma'
          f'\n(Ex: Type "{random1}, {random2}" for doing the activity at index {random1} for {random2} minutes.)'
            '\nType "exit" to exit.\n')
    line_count += 5
    if user_input.lower() == 'exit':
        return
    try:
        user_input = user_input.strip().split(',')
        index = int(user_input[0]) - 1
        time_minutes = int(user_input[1])
        if index < 0 or index >= len(todo_list):
            print('Error: Index out of range. Please enter a valid index.')
            return
        if time_minutes <= 0:
            print('Error: Time must be a positive integer.')
            return
        print("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate(f'Starting work on "{todo_list[index]}" for {time_minutes} minutes.')))
        for i in range(time_minutes):
            for j in range(60):
                print("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate(f'Minutes: {i}, Seconds: {j}, Percentage: {((i * 60 + j) / (time_minutes * 60)) * 100:.2f}%')))
                time.sleep(1)
                clear_last_lines(1)
        clear_last_lines(1)  # Clear the last line after the timer
        print("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate(f'Finished working on "{todo_list[index]}".')))
        todo_list.pop(index)
        todo_save_todos()

    except:
        print('Error: Invalid input format. Please use the format "index,time".')
        return



def open_function():
    app_name = command[5:].strip()
    try:
        subprocess.run(['open', '-a', app_name], check=True)
    except:
        time.sleep(0.1)
    else:
        print(f'Opened "{app_name.capitalize()}".')


def chat_function():
    # TODO: This feature needs to be implemented.
    print('This feature is  not implemented yet.')

def unknown_command():
    global command
    if command == "":
        return

    typo = False
    possible_command = None
    for thething in commands:
        if thething in command:
            typo = True
            possible_command = thething
            break
        if thething in command:
            typo = True
            possible_command = thething
            break
    if typo:
        print(f'Unknown command: "{command}". Did you mean: "{possible_command}"?')
    else:
        print(f'Unknown command: "{command}". For help, type "help".')


while True:
    command = input("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate('>>> ')) + "\033[0m").strip()
    line_count += 1
    commandarr = [n for n in command.lower().split(' ') if n != '']
    commandoriginal = command.strip()

    command = command.lower().strip()
    # To Do App Commands:
    if commandarr[0] == 'todo' and len(commandarr) > 1:
        if commandarr[1] == 'help':
            todo_help()
        elif commandarr[1] == 'ls':
            todo_ls()
        elif commandarr[1] == 'rm':
            if len(commandarr) > 2 and commandarr[2] == 'all':
                todo_list.clear()
                todo_save_todos()
                print('All items were deleted.')
            else:
                todo_delete_function()
        elif commandarr[1] == 'add':
            todo_add()
        elif commandarr[1] == 'changeorder':
            todo_changeorder()
        elif commandarr[1] == 'abcorder':
            todo_abcorder()
        elif commandarr[1] == 'cbaorder':
            todo_cbaorder()
        elif commandarr[1] == 'do':
            todo_do_function()
        else:
            print(f'Unknown TODO command: "{command[5:].strip()}". For help, type "todo help".')
    elif commandarr[0] == 'todo' and len(commandarr) == 1:
        todo_help()
    elif commandarr[0] == 'open':
        open_function()
    elif commandarr[0] == 'help' and len(commandarr) == 1:
        print(help_content)
    elif commandarr[0] == 'chat' and len(commandarr) == 1:
        chat_function()
    elif commandarr[0] == 'exit' or commandarr[0] == 'quit' and len(commandarr) == 1:
        clear_last_lines(100)
        print("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in enumerate('Robot Human Assist By: Batu Koray Masak')))
        break
    elif commandarr[0] == 'clear' or command == 'clr':
        clear_last_lines(line_count)
    elif command[0:4] == 'eval':
        try:
            result = eval(command[5:].replace('pi', str(math.pi)).replace('e',str(math.e)))
            # if it’s an int or float, format with commas:
            if isinstance(result, (int, float)):
                print(f"{result:,}")
            else:
                print(result)
        except Exception:
            unknown_command()
    else:
        unknown_command()
