# -*- coding: utf-8 -*-

import time, random, json, epub, os, re

from bs4 import BeautifulSoup as bsoup
from nltk.stem import PorterStemmer, WordNetLemmatizer
# from nltk.corpus import wordnet as wn
from nltk import pos_tag
from singular import singular

# NOUNS = {w.name().split('.', 1)[0] for w in wn.all_synsets('n')}
# VERBS = {w.name().split('.', 1)[0] for w in wn.all_synsets('v')}
# ADJECTIVES = {w.name().split('.', 1)[0] for w in wn.all_synsets('a')}


def load_familiar():
    dirpath = "./vocabulary/familiar/"
    familiar_words = []
    for filename in os.listdir(dirpath):
        with open(dirpath + filename) as fwf:
            familiar_words += fwf.read().split()
    return list(set(familiar_words))

def read_book(bookfile):
    book = epub.open_epub(bookfile)
    compiled = ''
    for item in book.opf.manifest.values():
        data = book.read_item(item)
        soup = bsoup(data, 'html.parser')
        for p in soup.find_all('p'):
            # text = p.get_text().encode('utf-8')
            text = p.get_text()
            # text = text.encode('ascii', errors='ignore').decode('ascii')
            text = ' ' + text + ' '
            compiled += text
    return compiled

def extract_words(text):
    bad_chars = '"(){}<>/\\.1234567890?!,:;'
    words = set()
    for w in text.split():
        # w = word.strip(bad_chars)
        word = "".join(c for c in w if c not in bad_chars)
        word = word.replace('—', '-')
        word = word.strip('-')
        word = word.strip("'")
        # if "-" in word:
        words_ = word.split('-')
        for word_ in words_:
            if len(word_) > 2: 
                word_ = word_.encode('ascii', errors='ignore').decode('ascii')
                words.add(word_)
    return words

def reduce_words(words, common_words):
    reduced = []
    for word in words:
        if word not in common_words:
            reduced.append(word)
    return reduced

def drop_capitals(wordlist):
    return [word for word in wordlist if word.islower() and not word.isupper()]

def lemmatize_words(words):
    lemwords = set()
    lemmatiser = WordNetLemmatizer()
    for wo in words:
        word = wo.replace("'s", "").replace("n't", "")
        # word = word.replace("n't", "")
        noun = lemmatiser.lemmatize(word)
        verb = lemmatiser.lemmatize(noun, pos="v")

        if verb != noun:
            lemwords.add(verb)
        else:
            ptag = pos_tag([noun])[0][1]
            # print("ptag:", ptag)
            if ptag == 'NNS' and noun[-1] == "s":
                # print('plural:', noun)
                # word = word.rstrip("s")
                noun = singular(noun)
                # print('singular:', noun)
                # print()
            lemwords.add(noun)
    return list(lemwords)

def build_vocabulary(words, bookpath):
    dirpath = './vocabulary/'
    bookname = re.findall('.*/(.*)\.', bookpath)[0]
    # bookname = re.findall('/(.*)\.', bookpath)[0]
    output = dirpath + bookname + '.rst'
    if os.path.exists(output):
        renamelist = []
        for filename in os.listdir(dirpath):
            if bookname in filename:
                # print(filename)
                renamelist.append(filename)
        # rev = reversed(sorted(renamelist, key=len))
        # print(reversed(sorted(renamelist, key=len)))
        for filename in reversed(sorted(renamelist, key=len)):
            splitname = filename.split('.')
            nuname = splitname[0] + '0' + '.rst'
            os.rename(dirpath + filename, dirpath + nuname)

    with open(output, 'w') as words_file:
        for word in words:
            words_file.write(word + '\n')

    # os.rename(filename, filename.replace(" ", "-").lower())

def find_words(bookpath):

    book_str = read_book(bookpath)
    words = extract_words(book_str)
    words = drop_capitals(words)
    words = lemmatize_words(words)
    familiar_words = load_familiar()
    words = reduce_words(words, familiar_words)
    # random.shuffle(words)
    words = sorted(words)
    _msg = "Total number of %d unfamiliar words found in book %s"
    print(_msg %(len(words), bookpath))
    # print(words)
    build_vocabulary(words, bookpath)


if __name__ == '__main__': 
    print('Enter path to book file. (Currently only .epub format is supported)')
    book = input()
    find_words(book)
    # find_words("books/Dragon's Egg.epub")




# DEPRECATED


# def lemmatize_words(words):
#     lemwords = set()
#     badwords = set()
#     lemmatiser = WordNetLemmatizer()
#     for word in words:
#         noun = lemmatiser.lemmatize(word, pos='n')
#         verb = lemmatiser.lemmatize(word, pos="v")
#         adjective = lemmatiser.lemmatize(word, pos='a')
#         # if word == 'civilians':
#         #     print('NOUN:', noun)
#         #     print('VERB:', verb)
#         #     print('ADJECTIVE:', adjective)
#         #     print(noun in NOUNS)
#         if noun in NOUNS:
#             lemwords.add(noun)
#         else: 
#             badwords.add(noun)

#         if verb in VERBS:
#             lemwords.add(verb)
#         else: 
#             badwords.add(verb)

#         if adjective in ADJECTIVES:
#             lemwords.add(adjective)
#         else: 
#             badwords.add(adjective)

#     badwords = badwords - lemwords
#     for w in badwords: print(w)
#     return list(lemwords)
