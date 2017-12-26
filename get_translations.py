import json, random, time, re, os
import lingvo_api

_sleeptimes = [1,3,10,30,60]

def translate_words_recursive(words, dumpfile, srclang='En', dstlang='Uk', stime_idx=0):
    if stime_idx > 4:
        return

    translations = []
    delayed = []

    stimes = [st for st in _sleeptimes[:stime_idx+1]]
    
    for i, word in enumerate(words):
        print(i, word)
        if i == 300: 
            print("Sleeping for 1 minute...")
            time.sleep(60)
        time.sleep(0.5)
        translation = lingvo_api.get_translation(word, srclang=srclang, dstlang=dstlang)
        if type(translation) is int:
            print('Server says:', translation)
            if translation == 429:
                for j, stime in enumerate(stimes):
                    print("waiting for %d seconds" %stime)
                    time.sleep(stime)
                    translation = lingvo_api.get_translation(word, srclang=srclang,
                                                                   dstlang=dstlang)
                    if type(translation) is int:
                        print('Server says:', translation)
                        if translation == 429 and j == len(stimes)-1:
                            delayed.append(word)
                    else:
                        # translations.append(translation)
                        trans_json = json.dumps(translation,
                                            indent=4, ensure_ascii=False)
                        with open(dumpfile, 'a') as transdump:
                            transdump.write(trans_json + ',\n')
                        break 
        else:
            trans_json = json.dumps(translation, indent=4, ensure_ascii=False)
            with open(dumpfile, 'a') as transdump:
                transdump.write(trans_json + ',\n')

    print("len(delayed):", len(delayed))
    translate_words_recursive(delayed, dumpfile, srclang=srclang, dstlang=dstlang, 
                                                 stime_idx=stime_idx+1)


def load_words(wordsfile, store_familiar=True, 
               famfile="./vocabulary/familiar/familiar_words.rst"):
    unfamiliar = []
    familiar = []
    if store_familiar:
        try:
            with open(famfile) as fam:
                familiar = fam.readlines()
        except: pass
    
    with open(wordsfile) as words_file:
        words = words_file.readlines()
    
    for word in words:
        if word[:2] == '..':
            familiar.append(word[3:])
        else:
            unfamiliar.append(word.strip('\n'))

    if store_familiar:
        familiar = sorted(list(set(familiar)))
        with open(famfile, 'w') as fam:
            for famword in familiar:
                fam.write(famword)

    print("Total number of unfamiliar words in book is %d" %len(unfamiliar))
    return unfamiliar

def translate(words, dumpfile, srclang='En', dstlang='Uk'):


    with open(dumpfile, 'w') as transdump:
        transdump.write('')
    # translate_words(words[:1000])
    translate_words_recursive(words, dumpfile, srclang=srclang, dstlang=dstlang)

    with open(dumpfile, 'r+') as transdump:
        tolist = "[\n" + transdump.read()[:-2] + "\n]"
        transdump.seek(0, 0)
        transdump.write(tolist)

def build_dictionary(dumpfile, dictfile, blocknum=9, sortwords='a', insertline=True):

    with open(dumpfile) as transdump:
        translations = json.loads(transdump.read())

    items = []
    for item in translations:
        line = item['Heading'] + " - " + item['Translation']
        items.append(line)

    items = list(set(items))
    if sortwords == 'a':
        items = sorted(items)
    elif sortwords == 'r':
        random.shuffle(items)

    if insertline:
        addchar = '\n'
    else:
        addchar = ''

    if not blocknum:
        blocknum = len(items) + 1

    with open(dictfile, 'w') as worddict:
        i = 0
        j = 0
        blockwords = []
        for line in items:
            blockwords.append(line.split(' - ')[0])
            worddict.write(line + addchar)
            if (i == blocknum) or (j == len(items)-1):
            # if j == 3:
                worddict.write('\n')
                random.shuffle(blockwords)
                for bword in blockwords:
                    worddict.write(bword + addchar)
                worddict.write('\n\n')
                i = 0
                blockwords = []
            
            i += 1
            j += 1

    print("Dictionary is successfully built.")

if __name__ == '__main__': 

    # print('Enter path to book file. (Currently only .epub format is supported)')
    # book = input()

    wordsfile = "./vocabulary/Dragon's Egg.rst"
    words = load_words(wordsfile=wordsfile, store_familiar=True)

    bookname = re.findall('.*/(.*)\.', wordsfile)[0]
    dumpfile = './vocabulary/' + bookname + ".json"

    if os.path.exists(dumpfile):
        print("""Translations are already recieved. 
                 If you would like to recieve them again delete 
                 <bookname>.json file first.""")
    else:
        random.shuffle(words)
        # print(words)
        # print(len(words))
        translate(words, dumpfile, srclang='En', dstlang='Ru')

    dictfile = './vocabulary/' + bookname + ".dict"
    build_dictionary(dumpfile, dictfile, sortwords='r')






# DEPRECATED

# def translate_words(words, wordnum=0, dumpfile="translations.txt"):

#     translations = []
#     _sleeptimes = [3,10,30,60]
#     if wordnum:
#         stop = wordnum
#     else:
#         stop = len(words) - wordnum

#     # print("stop:", stop)

#     for i, word in enumerate(words):
#         if i == stop:
#             break
#         translation = lingvo_api.get_translation(word)
#         if type(translation) is int:
#             print(translation)
#             if translation == 429:
#                 for stime in _sleeptimes:
#                     time.sleep(stime)
#                     translation = lingvo_api.get_translation(word)
#                     if type(translation) is not int:
#                         break
#         translations.append(translation)
#         with io.open(dumpfile, 'w', encoding='utf8') as transdump:
#             translations_json = json.dumps(translations, sort_keys=True, 
#                                             indent=4, ensure_ascii=False)
#             transdump.write(translations_json)

#     # with io.open(dumpfile, 'w', encoding='utf8') as transdump:
#         # for item in translations:
#         # transdump.write(translations_json)


