import os
import random

BASE_FOLDER_NAME = "words_with_translations"


class CustomException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def cls_win(): os.system('cls')


def repeat_input_until_operation_without_exception(input_hint_to_print, operation_to_call_on_input,
                                                   exception_to_catch, exception_text_to_print):
    while True:
        try:
            user_input = input(input_hint_to_print)
            return user_input, operation_to_call_on_input(user_input)
        except exception_to_catch:
            print(exception_text_to_print)


def read_words_from_files(file_names):
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

        base_word, translation = map(lambda el: el.strip(), words[rand_positions[i]])
        compare_with = translation if base_first else base_word
        user_input = input((base_word if base_first else translation) + ':\n\n').strip()

        if user_input.lower() in map(str.strip, compare_with.split(',')):
            print('\nok\n')
            print(compare_with)
            input('\nenter to next')
        else:
            print('\nnope:(\n')
            print(compare_with)
            answer = input('\nadd to repeat list - enter, skip - 1: ')
            if answer != '1':
                to_repeat.append((base_word, translation))

        cls_win()
    return to_repeat


def run_main_flow():
    try:
        (_, _, filenames) = next(os.walk(BASE_FOLDER_NAME))
    except StopIteration:
        raise CustomException(
            f'folder "{BASE_FOLDER_NAME}" need to be created in current folder and contains at leas one file')

    options = [f'{i + 1}: {os.path.splitext(filenames[i])[0]}' for i in range(len(filenames))]
    print('0: all', *options, sep='\n')

    while True:
        user_input, int_input = repeat_input_until_operation_without_exception(
            '\nenter file number (base word to translation from file №1: "1", translation '
            'to base from file №1: "-1" or "01"): ',
            int, ValueError, '\nplease, enter an integer number')

        file_number = abs(int_input)
        if file_number > len(filenames):
            print("\nthere is no file under this number\n")
        else:
            break

    order_sign = user_input.strip()[0] if len(user_input.strip()) > 1 else 1
    base_first = not ('-' == order_sign or '0' == order_sign)

    words_list = read_words_from_files(filenames if 0 == file_number else [filenames[file_number - 1]])
    if not words_list:
        raise CustomException('chosen file is empty')
    if len(words_list) % 2 != 0:
        raise CustomException("wrong file format - quantity of base words isn't equal quantity of translated words")

    grouped_words = list(zip(words_list[0::2], words_list[1::2]))
    cls_win()

    words_to_repeat = check_words(grouped_words, base_first)
    all_words_to_repeat = words_to_repeat.copy()
    cls_win()
    while len(words_to_repeat) > 0:
        input('words to repeat: ' + str(len(words_to_repeat)) + '\nenter for start')
        cls_win()
        words_to_repeat = check_words(words_to_repeat, base_first)
        cls_win()
    else:
        print("that's all, nice work!")
        if all_words_to_repeat:
            print("repeated words:\n")
            print(*[f'{word_tr[0]} - {word_tr[1]}' for word_tr in all_words_to_repeat], sep='\n')
        else:
            print('all words on the first try')


if __name__ == '__main__':
    repeat = True

    try:

        while repeat:
            run_main_flow()
            repeat = input('\n\n\nenter - continue, 2 - exit: ') != '2'
            cls_win()

    except CustomException as e:
        print("\n\n", str(e))
        input()

    except Exception as ex:
        print("SOMETHING UNPREDICTABLE OCCURRED, CALL FOR SOMEONE WHO KNOW\n\n\n")
        print(ex)
        input()
