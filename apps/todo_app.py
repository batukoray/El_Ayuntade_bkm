import os
import json
import random
import time
from main import Colors, neon_text, clear_last_lines
import user_data
import utils
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

def todo_add(command_original:str):
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

def todo_delete_function(command_original:str):
    """
    This function deletes an item from the TODO list based on the command input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    todo_save()
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
                todo_list = []
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

def write_worklogs(message:str):
    """
    This function writes a message to the worklogs file.
    :param message: The message to be written to the worklogs file.
    :return: void
    """
    with open(user_data.WORKLOGS_FILE_LOC, "a") as f:
        f.write(message + '\n')
