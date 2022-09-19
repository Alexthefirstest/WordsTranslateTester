import os
import random

BASE_FOLDER_NAME = "words_with_translations"


class CustomException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def cls_win(): os.system('cls')


def process_input(input_text, operation, exception_to_catch, exception_text):
    while True:
        try:
            user_input = input(input_text)
            operation(user_input)
        except exception_to_catch:
            print(exception_text)
            continue

        return user_input


def read_data(file_names):
    words = []

    for file_name in file_names:
        with open(f'{BASE_FOLDER_NAME}/{file_name}', encoding='utf-8') as w:
            words += w.read().splitlines()
    return words


def check_words(words: list, base_first):
    to_repeat = []
    words_len = len(words)
    rand_positions = random.sample(range(words_len), words_len)
    for i in range(words_len):
        print(f'{i + 1}/{words_len}\n')

        a, b = map(lambda el: el.strip().lower(), words[rand_positions[i]])
        compare_with = b if base_first else a
        user_input = input((a if base_first else b) + ':\n').strip().lower()

        if user_input == compare_with:
            print('\nok\n')
            print(compare_with)
            input('\nenter to next')
        else:
            print('\nnope:(\n')
            print(compare_with)
            answer = input('\nadd to repeat list - 1, skip - enter: ')
            if answer == '1':
                to_repeat.append((a, b))

        cls_win()
    return to_repeat


def start_main_flow():
    try:
        (_, _, filenames) = next(os.walk(BASE_FOLDER_NAME))
    except StopIteration:
        raise CustomException(f'folder "{BASE_FOLDER_NAME}" need to be created in current folder')

    options = [f'{i + 1}: {os.path.splitext(filenames[i])[0]}' for i in range(len(filenames))]
    print('0: all', *options, sep='\n')

    while True:
        user_input = process_input('\nenter file number (base word to translation from file №1: "1", translation '
                                   'to base from file №1: "-1"): ',
                                   int, ValueError, '\nplease, enter an integer number')

        file_number = abs(int(user_input))
        if file_number > len(filenames):
            print("\nthere is no file under this number\n")
        else:
            break

    base_first = not '-' == user_input[0]

    words_list = read_data(filenames if 0 == file_number else [filenames[file_number - 1]])
    if not words_list:
        raise CustomException('chosen file is empty')
    if len(words_list) % 2 != 0:
        raise CustomException('wrong file format - quantity of base words != quantity of translated words')

    grouped_words = list(zip(words_list[0::2], words_list[1::2]))
    cls_win()

    words_to_repeat = check_words(grouped_words, base_first)
    cls_win()
    while len(words_to_repeat) > 0:
        input('words to repeat: ' + str(len(words_to_repeat)) + '\nenter for start')
        cls_win()
        words_to_repeat = check_words(words_to_repeat, base_first)
        cls_win()
    else:
        print("that's all, nice job!")


if __name__ == '__main__':
    repeat = True

    try:

        while repeat:
            start_main_flow()
            repeat = input('\n\nenter - continue, 2 - exit: ') != '2'
            cls_win()

    except CustomException as e:
        print("\n\n", str(e))
        input()

    except Exception as ex:
        print("SOMETHING UNPREDICTABLE OCCURRED, CALL FOR SOMEONE WHO KNOW\n\n\n")
        print(ex)
        input()
