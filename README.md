# WordsTranslateTester

to start - dist/words_translate_tester.exe

dist/words_with_translations - folder with .txt files (or any other extension). files should contain words with translations in format:

    word1
    translation1
    word2
    translation2_1, translation2_2 (for 'ok' during answerring print one of translations(2_1 or 2_2))

words_translate_tester.exe and  words_with_translations should be in the same folder


compile new exe if needed:
pyinstaller --onefile words_translate_tester.py