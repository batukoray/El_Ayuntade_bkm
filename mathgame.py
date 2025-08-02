DIGIT_MAP = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}

def words_to_number(text: str) -> str:
    """
    Convert a space-separated sequence of digit words into a string of digits.
    E.g. "five fifty one" -> "551"
    """
    return "".join(DIGIT_MAP.get(word.lower(), "") for word in text.split())
import random

from el_ayuntade_bkm import *
import user_data
import utils
import time
import speech_recognition

def mathgame_start(command_original):
    if command_original.lower() != 'mathgame -voice':
        mathgame_text_version(command_original)
    else:
        mathgame_voice_version(command_original)

def mathgame_text_version(command_original):
    start = time.perf_counter()
    command_lower = command_original.lower()
    correct_answers = 0
    question_count = int(command_lower.split(' ')[1]) if len(command_lower.split(' ')) > 1 else 10
    print(neon_text('Welcome to the Math Game!'))
    print(neon_text(f'You will be asked {question_count} questions.'))
    print(neon_text('You can answer with numbers only.'))
    print(neon_text('Let\'s start!\n'))
    try:
        for i in range(question_count):
            num1 = random.randint(1, 1000)
            num2 = random.randint(1, 1000)
            sign = random.choice(['+', '-'])
            answer = eval(f'{num1}{sign}{num2}')
            user_answer = int(input(neon_text(f'{num1} {sign} {num2} = ')))
            if user_answer == answer:
                print(neon_text('Correct!'))
                correct_answers += 1
            else:
                print(neon_text(f'Incorrect! The correct answer is {answer}.'))
    except ValueError:
        print(neon_text('Invalid input! Please enter numbers only.'))
        return
    print(neon_text('Game over!'))
    print(neon_text('Here are your results:'))
    print(neon_text(f'You answered {correct_answers} questions correctly out of {question_count} questions.'))
    print(neon_text(f'Your score: {correct_answers / question_count * 100:.2f}%'))
    print(neon_text(f'Time taken: {time.perf_counter() - start:.2f} seconds'))


    end = time.perf_counter()
    print(neon_text(
        f'You answered {correct_answers} questions correctly in {end - start:.2f} seconds. Correction rate: {correct_answers / question_count * 100:.2f}%'))
    print(neon_text(
        f'Seconds per question: {end - start:.2f} / {question_count} = {((end - start) / question_count):.2f}'))

def mathgame_voice_version(command_original):
    recognizer = speech_recognition.Recognizer()
    start = time.perf_counter()
    correct_answers = 0
    question_count = 10
    print(neon_text('You will be asked 10 questions.'))
    print(neon_text('The questions will be spoken to you.'))
    print(neon_text('Speak out your answer.'))
    for i in range(question_count):
        num1 = random.randint(1, 1000)
        num2 = random.randint(1, 1000)
        sign = random.choice(['+', '+'])
        if sign == '+':
            question = f'{num1} {sign} {num2}'
        else:
            question = f'{num1} {sign} {num2}'
        answer = eval(question)
        print(neon_text(question))
        text_to_speech_function(f'tts {question}',print_log=False)
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(neon_text('Listening for your answer...'))
            audio = recognizer.listen(source)
        try:
            user_answer = recognizer.recognize_google(audio)
            print(neon_text(f'You said: {user_answer}'))
            # convert spoken words into digits if needed
            if not user_answer.isdigit():
                user_answer = words_to_number(user_answer)
            # remove commas and spaces from formatted numbers
            user_answer = user_answer.replace(',', '').replace(' ', '')
            if user_answer.isdigit() and int(user_answer) == answer:
                print(neon_text('Correct'))
                correct_answers += 1
            else:
                print(neon_text('Incorrect'))
        except speech_recognition.UnknownValueError:
            print(f'{Colors.RED}Could not understand the audio.{Colors.RESET}')
        except speech_recognition.RequestError as e:
            print(f'{Colors.RED}Could not request results; {e}.{Colors.RESET}')



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
