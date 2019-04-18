# -*- coding: utf-8 -*-
import sys
from collections import Counter


def generate_ngram(words, n):
    """
        join first n grams then remove first word and join first n words
        which gives next gram do till grams can be found.
        eg: cat loves milk
            input --> cat loves milk
            1st --> cat loves
            remove cat then we get [loves, milk]
            --> loves milk
    """
    while True:
        gram = words[:n]
        if len(gram) == n:
            yield " ".join(gram)
            del words[0]
        else:
            return


def sort_and_save(sequence, filename):
    with open(filename, 'w', encoding='utf8') as out:
        out.write('[')
        for item in Counter(sequence).most_common():
            out.write('"'+item[0]+'",')
        out.write(']')


with open(sys.argv[1], 'r', encoding='utf8') as file:
    words = []
    chars = []
    lines = 0
    for line in file:
        lines += 1
        word = line.strip().split(' ')
        words += word
        for char in word:
            chars += char

    print('number of characters', len(chars))
    print('number of words', len(words))
    print('number of lines', lines)

    sort_and_save(chars, 'out-chars.txt')
    sort_and_save(words, 'out-words.txt')

    ngrams = ((2, 'out-bi-grams.txt'),
              (3, 'out-tri-grams.txt'))
    for _ in ngrams:
        sort_and_save(generate_ngram(words.copy(), _[0]), _[1])
