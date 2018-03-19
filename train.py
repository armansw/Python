import os
import argparse
import sys
import re
import pickle
from collections import defaultdict

List = []
r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')


def gen_lines(corpus): #Приводим к нижнему регистру
    for line in corpus:
        yield line.lower()


def gen_tokens(lines): #Очищаем текст от ненужных слов и символов
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def gen_trigrams(tokens):#Генератор, который выдаёт 3 друг за другом идущие слова
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$', '$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train(corpus): #Получает входную директорию,берёт все текстовые файлы из директории и строит модель
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)
    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:#Считаем кол-во пар и троек слов в тексте
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq / bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq / bi[t0, t1])]
    return model


if (__name__ == "__main__"): #Консольный интерфейс с использованием библиотеки argparse
    parser = argparse.ArgumentParser(description='Generate text model.')
    parser.add_argument(
        '--input-dir',
        dest='input_dir',
        type=str,
        default="",
        help='input files dir (default: stdin)')
    parser.add_argument(
        '--model',
        dest='model',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output model (default: stdout)')
    parser.add_argument(
        '--lc', dest='lc', type=None, help='make whole text lowercase')
    args = parser.parse_args()
    if not args.input_dir: #Если нет во входе директории то вводим с клавиатуры
        print(train(sys.stdin))
    else:
        os.chdir(args.input_dir) #В обратном случае читаем директорию и берём все текстовые файлы оттуда
        os.system('cat ' + ' '.join(glob.glob('*.txt')) +
                  ' > /tmp/generated_text.txt')
        mfl = open('/tmp/generated_text.txt', 'r')
        args.model.write(pickle.dunps(train(mfl)))
