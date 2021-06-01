import argparse
import re
import random
import pickle
import collections


def is_upper(current_string):
    use_upper = False
    # это подсказка, что следующее слово нужно будет писать с большой буквы
    index_last_symbol = int(len(current_string.split(" "))) - 1
    last_word = current_string.split(" ")[index_last_symbol]
    if str(last_word) in ['.', '!', '?', '...', '@']:
        use_upper = True
    return use_upper


def do_punctuation(string_with_space):
    # изначально строка содержит пробел между последним словом предложения и
    # знаком препинания. Поэтому надо его убрать, чтобы стало красиво
    last_word = string_with_space.split(" ")[-1]
    if str(last_word) in ['.', '!', '?', ',']:
        string_with_space = string_with_space[:-2] + string_with_space[- 1:]
        # убрали пробел между словом и знаком
    elif str(last_word) in ['...']:
        string_with_space = string_with_space[:- 4] + string_with_space[- 3:]
    elif str(last_word) in ['@']:
        string_with_space = string_with_space[:- 2] + '\n'
        # убрали пробел и добавили перенос на новую строку
    return string_with_space


def do_conclusion(last_word, current_string):
    # Хотим, чтобы текст всегда заканчивался красиво.
    # То есть каким-то знаком препинания. Нам не нужно такое, что
    # последнее предложение началось и оборвалось на одном слове.
    # и мы должны учеть то, что предпоследний символ
    # уже заканчивает предложение, а два таких рядом идти не могут
    if last_word not in [',', '@', '.', '!', '...', '?']:
        current_string = current_string + str(random.choice(['.', '!', '...', '?']))
    else:
        if last_word in ['!', '.', '?']:
            current_string = current_string[:- 2] + current_string[- 1:] + '\n'
        elif last_word in [',']:
            current_string = current_string[:- 2] + "." + '\n'
        elif last_word in ['...']:
            current_string = current_string[:- 4] + current_string[- 3:] + '\n'
        elif last_word in ['@']:
            current_string = current_string[:- 2] + '\n' + '\n'
    return current_string


def generator(first_word, length, model):
    current_word = first_word
    #Первый пробел - это начало каждого нового абзаца.
    new_string = " " + first_word.capitalize()
    #length -2 потому что последним словом будет знак препинания, чтобы было красиво
    for i in range(length - 2):
        if current_word not in model:
            # если первое слово ввели с клавиатуры и его нет в модели
            # или такое слово, на котором текст заканчивался и после него ничего нет
            next_word = random.choice(list(model.keys()))
            while next_word in [',', '.', '!', '?', '@', '-']:
                next_word = random.choice(list(model.keys()))
        else:
            list_next_words = []
            for word in model[current_word]:
                # вставим следующее слово столько раз, какая у него частота
                for count in range (model[current_word][word]):
                    list_next_words.append(word)
            # как в задании А)
            next_word = random.choice(list_next_words)
        use_upper = is_upper(new_string)
        new_string = do_punctuation(new_string)
        current_word = next_word
        if use_upper is True:
            next_word = next_word.capitalize()
        new_string = new_string + " " + next_word
    new_string = do_conclusion(current_word, new_string)
    return new_string


def load_dict(file_name):
    # строим словарь по файлу с моделью
    with open(file_name, 'rb') as file:
        model = pickle.load(file)
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, type=str,
                        help="The way to file, where your model is")
    parser.add_argument('--seed', type=str, default=None, help="First word")
    parser.add_argument('--length', required=True, type=int,
                        help="Length of text is generated")
    parser.add_argument("--output", "--output-dir", type=str, default=None,
                        help="File where you want to write rezult")
    args = parser.parse_args()
    model = load_dict(args.model)
    length = args.length
    assert length > 0, "Please, write length > 0"
    if args.seed is None:
        first_word = random.choice(list(model.keys()))
        while first_word in [',', '.', '!', '?', '@']:
            first_word = random.choice(list(model.keys()))
    else:
        first_word = args.seed
    if args.output is None:
        print(generator(first_word, length, model))
    else:
        with open(args.output, 'w', encoding='UTF-8') as file:
            file.write(generator(first_word, length, model))


if __name__ == '__main__':
    main()
