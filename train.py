import argparse
import os
import re
import pickle
import collections
import sys


def build_model(words, model):

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        if current_word in model:
            model[current_word][next_word] +=1
            # увеличим счетчик следующего после него слова
        else:
            model[current_word] = collections.Counter()
            model[current_word][next_word] += 1
            # если слова нет, создадим новое поле и добавим в
            # его значение следующее
    return model


def make_clear_line(line, use_lower):
    list_of_clear_words = []
    if use_lower is True:
        line = line.lower()
    # очистим строку
    newline = re.sub(r'\n', ' @', line)
    r_alphabet = re.findall(r'[a-zA-Zа-яА-Я0-9-]+|[.?,!@]+', newline)
    list_of_clear_words += r_alphabet
    return list_of_clear_words


def save_model(model, model_path):
    with open(model_path, 'wb') as file:
        pickle.dump(model, file, 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "--inpur-dir", type=str, default=None,
                        help="The path where you want " +
                        "to give the text")
    parser.add_argument("--lc", default=False, help="Do lowercase",
                        action='store_true')
    parser.add_argument("--model",  required=True, type=str,
                        help="The path where you want " +
                        "to save the model.", default="")
    args = parser.parse_args()
    use_lower = False
    if args.lc:
        use_lower = True
    lines = list()
    directory = args.input
    model = dict()
    if directory is None:
        lines =sys.stdin.readlines()
        for line in lines:
            list_of_clear_words = make_clear_line(line, use_lower)
            model = build_model(list_of_clear_words, model)
        # ввод из консоли
    else:
        file_names = os.listdir(directory)
        # это все файлы в введенной директории. Выберем текстовые
        txt_file_names = list(filter(lambda x: x.endswith('.txt'), file_names))
        for file_name in txt_file_names:
            path = os.path.join(directory,file_name)
            # path = directory + "/" + file_name
            # сделали путь для файла
            with open(path, 'r', encoding="UTF-8") as file:
                for line in file:
                    list_of_clear_words = make_clear_line(line, use_lower)
                    model = build_model(list_of_clear_words, model)
    save_model(model, args.model)


if __name__ == '__main__':
    main()
