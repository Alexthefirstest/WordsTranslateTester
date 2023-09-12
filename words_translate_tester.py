import _thread
import configparser
import os
import random

from gtts import gTTS
from playsound import playsound


class CustomException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def cls_win(): os.system('cls')


def init_global_variables():
    global WORDS_FOLDER_NAME, SOUNDS_FOLDER_NAME, REPEAT_FILE_PREFIX, MEDIA_FORMAT, LANG, TLD, SOUND_ON, BASE_SOUND_PATH

    try:
        config = configparser.ConfigParser()
        config.read('settings.ini')

        SOUND_ON = config['SOUND']['SOUND_ON']
        LANG = config['SOUND']['LANGUAGE_CODE']
        try:
            TLD = config['SOUND']['PRONUNCIATION_CODE']
        except KeyError:
            TLD = ''
        MEDIA_FORMAT = config['SOUND']['MEDIA_FORMAT']

        WORDS_FOLDER_NAME = config['FOLDERS']['WORDS_FOLDER_NAME']
        SOUNDS_FOLDER_NAME = config['FOLDERS']['SOUNDS_FOLDER_NAME']
        REPEAT_FILE_PREFIX = config['FOLDERS']['REPEAT_FILE_PREFIX']

    except KeyError as ke:
        raise CustomException('Something wrong with settings.ini file:\n' + str(ke) + ' looks incorrect')

    BASE_SOUND_PATH = f'{SOUNDS_FOLDER_NAME}/%s_{LANG}_{TLD}.{MEDIA_FORMAT}'


def repeat_input_until_operation_without_exception(input_hint_to_print, operation_to_call_on_input,
                                                   exception_to_catch, exception_text_to_print):
    while True:
        try:
            user_input = input(input_hint_to_print)
            return user_input, operation_to_call_on_input(user_input)
        except exception_to_catch:
            print(exception_text_to_print)


def read_words_from_files(file_names: list):
    words = []

    for file_name in file_names:
        with open(f'{WORDS_FOLDER_NAME}/{file_name}', encoding='utf-8') as w:
            words += w.read().splitlines()
    return words


def write_words_to_file(file_name, words):
    with open(f'{WORDS_FOLDER_NAME}/{file_name}', encoding='utf-8', mode='w') as w:
        w.write('\n'.join(word for line in words for word in line))


def find_or_download_sounds(words):
    counter = 0
    len_words = len(words)
    for word in words:
        counter += 1
        cls_win()
        print(f'checking sound files: {counter}/{len_words} words')
        if not os.path.exists(BASE_SOUND_PATH % word):
            print('\ndownloading "' + word + '"')
            if TLD:
                sound = gTTS(text=word, lang=LANG, tld=TLD, slow=False)
            else:
                sound = gTTS(text=word, lang=LANG, slow=False)

            sound.save(BASE_SOUND_PATH % word)


def make_sound(word):
    _thread.start_new_thread(playsound, (BASE_SOUND_PATH % word,))


def check_words(words: list, foreign_first):
    to_repeat = []
    words_len = len(words)
    rand_positions = random.sample(range(words_len), words_len)

    for i in range(words_len):
        print(f'{i + 1}/{words_len}\n')

        foreign_word, translation = map(lambda el: el.strip(), words[rand_positions[i]])
        compare_with = translation if foreign_first else foreign_word

        if foreign_first:
            print(foreign_word + ':\n')
            make_sound(foreign_word)
            user_input = input().strip()
        else:
            user_input = input(translation + ':\n\n').strip()

        if user_input.lower() in map(str.strip, compare_with.lower().split(',')):
            print('\nok\n')
            print(compare_with)
            if not foreign_first:
                make_sound(foreign_word)

            answer = input('\n0 to hear word, enter to continue: ')
            while '0' in answer:
                make_sound(foreign_word)
                answer = input('\n0 to hear word, enter to continue')

        else:
            print('\nnope:(\n')
            print(compare_with)
            if not foreign_first:
                make_sound(foreign_word)

            while True:
                answer = input('\n0 to hear word, add to repeat list - enter, skip - 1: ')
                if '0' in answer:
                    make_sound(foreign_word)
                    continue
                if answer != '1':
                    to_repeat.append((foreign_word, translation))
                break

        cls_win()
    return to_repeat


def run_main_flow():
    try:
        (_, _, filenames) = next(os.walk(WORDS_FOLDER_NAME))
    except StopIteration:
        raise CustomException(
            f'folder "{WORDS_FOLDER_NAME}" need to be created in current folder and contains at leas one file')

    filenames.sort()
    options = [f'{i + 1}: {os.path.splitext(filenames[i])[0]}' for i in range(len(filenames))]
    print('0: all', *options, sep='\n')

    while True:
        user_input, int_input = repeat_input_until_operation_without_exception(
            '\nenter file number (foreign word to translation from file №1: "1", translation '
            'to foreign from file №1: "-1" or "01"): ',
            int, ValueError, '\nplease, enter an integer number')

        file_number = abs(int_input)
        if file_number > len(filenames):
            print("\nthere is no file under this number\n")
        else:
            break

    order_sign = user_input.strip()[0] if len(user_input.strip()) > 1 else 1
    foreign_first = not ('-' == order_sign or '0' == order_sign)

    words_filename = None if 0 == file_number else filenames[file_number - 1]
    words_list = read_words_from_files([words_filename] if words_filename else filenames)
    if not words_list:
        raise CustomException('chosen file is empty')
    if len(words_list) % 2 != 0:
        raise CustomException("wrong file format - quantity of foreign words isn't equal quantity of translated words")

    foreign_words = words_list[0::2]
    find_or_download_sounds(foreign_words)
    grouped_words = list(zip(foreign_words, words_list[1::2]))
    cls_win()

    words_to_repeat = check_words(grouped_words, foreign_first)
    all_words_to_repeat = words_to_repeat.copy()
    cls_win()
    while len(words_to_repeat) > 0:
        input('words to repeat: ' + str(len(words_to_repeat)) + '\nenter for start')
        cls_win()
        words_to_repeat = check_words(words_to_repeat, foreign_first)
        cls_win()
    else:
        print("that's all, nice work!")
        file_name_to_add_or_remove = words_filename or 'all'

        if all_words_to_repeat:
            print("repeated words:\n")
            print(*[f'{word_tr[0]} - {word_tr[1]}' for word_tr in all_words_to_repeat], sep='\n')

            need_save = input('\n\nsave repeated words to a file - enter, skip - 1: ')
            if need_save != '1':
                write_words_to_file(file_name_to_add_or_remove if REPEAT_FILE_PREFIX in file_name_to_add_or_remove
                                    else REPEAT_FILE_PREFIX + file_name_to_add_or_remove,
                                    all_words_to_repeat)
                print('\ndone\n')
        else:
            print('all words on the first try')

            if REPEAT_FILE_PREFIX in file_name_to_add_or_remove:
                need_remove = input('\n\nremove this file with words to repeat - enter, skip - 1: ')

                if need_remove != '1':
                    os.remove(f'{WORDS_FOLDER_NAME}/{file_name_to_add_or_remove}')

                    print('\ndone\n')


if __name__ == '__main__':
    repeat = True

    try:
        init_global_variables()

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
