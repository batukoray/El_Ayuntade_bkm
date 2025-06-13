"""
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
            # Print the closest command if the command is not recognized
            unknown_command()
    elif commandarr[0] == 'todo' and len(commandarr) == 1:
        todo_help()

    elif commandarr[0] == 'open':
        open_function()
    elif commandarr[0] == 'help' and len(commandarr) == 1:
        print(help_content)
    elif commandarr[0] == 'chat' and len(commandarr) == 1:
        chat_function()
    elif (commandarr[0] == 'exit' or commandarr[0] == 'quit') and len(commandarr) == 1:
        clear_screen()
        print("".join(f"{neon_colors[i % len(neon_colors)]}{char}" for i, char in
                      enumerate('\nGoodbye! | Robot Human Assist By: Batu Koray Masak')))
        sys.exit(0)
    elif (commandarr[0] == 'clear' or command == 'clr') and len(commandarr) == 1:
        clear_screen()
    elif commandarr[0] == 'eval':
        try:
            result = eval(command[5:].replace('pi', str(math.pi)).replace('e', str(math.e)))
            if isinstance(result, (int, float)):
                print(f"{result:,}")
            else:
                print(result)
        except Exception:
            unknown_command()
    else:
        unknown_command()
"""