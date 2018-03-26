import os
import argparse
import sys
import re
import pickle
import glob
from collections import defaultdict

List = []
r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')


def gen_lines(corpus, lc):  # Приводим к нижнему регистру
    for line in corpus:
        if lc:
            yield line.lower()
        else:
            yield line


def gen_tokens(lines):  # Очищаем текст от ненужных слов и символов
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def gen_trigrams(tokens):  # Генератор, который выдаёт 3 друг за другом идущие слова
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$', '$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train(corpus, lc):  # Получает входную директорию,берёт все текстовые файлы из директории и строит модель
    lines = gen_lines(corpus, lc)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)
    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:  # Считаем кол-во пар и троек слов в тексте
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq / bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq / bi[t0, t1])]
    return model


if (__name__ == "__main__"):  # Консольный интерфейс с использованием библиотеки argparse
    parser = argparse.ArgumentParser(description='Generate text model.')
    parser.add_argument(  # Описание команды ввода директорий
        '--input-dir',
        dest='input_dir',
        type=str,
        default="",
        help='input files dir (default: stdin)')
    parser.add_argument(  # Описание команды lc,чтобы видеть все файлы в директорий и взять только файлы формата .txt
        '--lc',
        dest='lc',
        action='store_true',
        help='make whole text lowercase')

    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(
        '--model',
        dest='model',
        type=argparse.FileType('wb'),
        help='output file',
        required=True)
    args = parser.parse_args()
    if not args.input_dir:  # Если нет во входе директории то вводим с клавиатуры
        args.model.write(pickle.dumps(train(sys.stdin)))
    else:
        os.chdir(args.input_dir)  # В обратном случае читаем директорию и берём все текстовые файлы оттуда
        cmd = 'cat ' + ' '.join(
            glob.glob('*.txt')) + ' > /tmp/generated_text.txt'
        mfl = open('/tmp/generated_text.txt', 'r')
        
        # плохая идея, используй os.listdir и проходи по всем файлам
        args.model.write(pickle.dumps(train(mfl, args.lc)))
