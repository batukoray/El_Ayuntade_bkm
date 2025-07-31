import os
import sys
import json
from idlelib.colorizer import ColorDelegator

import user_data
from el_ayuntade_bkm import *
from utils import *


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
          '\nType "check -check <item indexes separated with commas>" to mark multiple items as done.'
          '\nType "check -check all" to mark all items as done.'
          '\nType "check -uncheck <item_name or index_of_item>" to mark an item as undone.'
          '\nType "check -uncheck <item indexes separated with commas>" to mark multiple items as undone.'
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

def checklist_add(command_original:str):
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

def checklist_delete_function(command_original:str):
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
    if command_lower == 'check rm all':
        checklist_dict.clear()
        checklist_save()
        print('All items were deleted from the checklist.')
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

def checklist_changeorder(command_original:str):
    """
    This function changes the order of two items in the checklist based on the index of the given user input.
    :param command_original: The original command input by the user without multiple whitespaces.
    :return: void
    """
    print(f'{Colors.RED}This feature is not working for some reason yet. -bkm, the dev{Colors.RESET}')
    return
    global checklist_dict
    update_checklist()
    if len(checklist_dict) < 2:
        print(f'{Colors.RED}You need at least two items in your checklist to change their order.{Colors.RESET}')
        return

    numbers = command_original[len('check changeorder '):].strip().split(',')
    if len(numbers) != 2:
        print(f'{Colors.RED}Error: You need to provide exactly two indexes to swap.{Colors.RESET}')
        return

    try:
        update_checklist()
        index1 = int(numbers[0].strip()) - 1
        index2 = int(numbers[1].strip()) - 1
        if index1 < 0 or index2 < 0 or index1 >= len(checklist_dict) or index2 >= len(checklist_dict):
            print(f'{Colors.RED}Error: Index out of range.{Colors.RESET}')
            return
        item1 = list(checklist_dict.keys())[index1]
        item2 = list(checklist_dict.keys())[index2]
        temp = checklist_dict[item1]
        checklist_dict[item1] = checklist_dict[item2]
        checklist_dict[item2] = temp


        checklist_save()
        update_checklist()
        print(f'Swapped items "{item1}" and "{item2}".')
    except ValueError:
        print(f'{Colors.RED}Error: Invalid input. Please enter valid indexes.{Colors.RESET}')


def checklist_mark(command_original:str,check:bool):
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