from train import train
import argparse
import sys
import random
import pickle


def unirand(
        seq):  # Возвращаем случайное слово после данного слова.Слово случайным образом выбирается из списка слов с ненулевой вероятностью
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = random.uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token


def generate_sentence(model, t0, length):  # Генерирует модель
    phrase = ''
    t1 = '$'
    if length == 0:
        length = random.randint(1, 10)
    for _ in range(length):
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize() + '\n'


if __name__ == '__main__':  # Консольный интерфейс приложения
    parser = argparse.ArgumentParser(description='Generate text model.')
    parser.add_argument(  # Команда ввода начального слова
        '--seed',
        dest='seed',
        type=str,
        default="$",
        help='starting word (default: random)')
    parser.add_argument(  # Команда ввода файла
        '--output',
        dest='output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output model (default: stdout)')
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(  # Команда ввода модели
        '--model',
        dest='model',
        type=argparse.FileType('rb'),
        help='input model',
        required=True)
    requiredNamed.add_argument(  # Команда ввода длины сгенерированного текста
        '--length',
        dest='length',
        type=int,
        help='length of the sequence to be generated',
        required=True)
    args = parser.parse_args()
    args.output.write(
        generate_sentence(pickle.load(args.model), args.seed, args.length))
