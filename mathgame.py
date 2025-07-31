import random
from multiprocessing.connection import answer_challenge

from el_ayuntade_bkm import *
import user_data
import utils

def mathgame_start(command_original):
    command_lower = command_original.lower()
    correct_answers = 0
    question_count = int(command_lower.split(' ')[1]) if len(command_lower.split(' ')) > 1 else 10
    print(neon_text('Welcome to the Math Game!'))
    print(neon_text(f'You will be asked {question_count} questions.'))
    print(neon_text('You can answer with numbers only.'))
    print(neon_text('Let\'s start!\n'))
    for i in range(question_count):
        num1 = random.randint(1, 1000)
        num2 = random.randint(1, 1000)
        sign = random.choice(['+', '-'])
        if sign == '+':
            try:
                user_answer = int(input(neon_text(f'{num1} {sign} {num2} = ')))
            except ValueError:
                print(f'{Colors.RED}Numeric value only.{Colors.RESET}')
                return
            if user_answer == num1 + num2:
                print(neon_text('Correct'))
            else:
                print(neon_text('Incorrect'))
        if sign == '-':
            try:
                user_answer = int(input(neon_text(f'{num1} {sign} {num2} = ')))
            except ValueError:
                print('Numeric value only.')
                return
            if user_answer == num1 - num2:
                print(neon_text('Correct'))
            else:
                print(neon_text('Incorrect'))





