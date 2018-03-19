from train import train
from random import uniform

def unirand(seq): #Возвращаем случайное слово после данного слова.Слово случайным образом выбирается из списка слов с ненулевой вероятностью
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token



def generate_sentence(model): #Генерирует модель
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()



if __name__ == '__main__':
    model = train(open('tolstoy.txt', 'r'))
    for i in range(10):
        print(generate_sentence(model))
