import re, os, random
import readbook as rb
import get_translations as gt


print("Enter path to book file. (Currently only 'epub' format is supported an source language must be English)")
book = input()
srclang = 'En'
print("Enter destination language. (Default value is 'Uk')")
dstlang = input()
if not dstlang:
    dstlang = 'Uk'

bookname = re.findall('.*/(.*)\.', book)[0]
wordsfile = "./vocabulary/" + bookname + ".rst"
dumpfile = './vocabulary/' + bookname + ".json"
dictfile = './vocabulary/' + bookname + ".dict"

# print(bookname)
# print(wordsfile)
# print(dumpfile)
# print(dictfile)

# Read book and build vocabulary
rb.find_words(book)

# Get translations from lingvolive.com
words = gt.load_words(wordsfile=wordsfile, store_familiar=True)
if os.path.exists(dumpfile):
    print("""Translations are already recieved. 
             If you would like to recieve them again delete 
             <bookname>.json file first.""")
else:
    random.shuffle(words)
    # print(words)
    # print(len(words))
    gt.translate(words, dumpfile, srclang=srclang, dstlang=dstlang)

# Build dictionary
gt.build_dictionary(dumpfile, dictfile, sortwords='r')

