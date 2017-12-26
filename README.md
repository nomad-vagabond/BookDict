# BookDict

BookDict is a Python library for extraction of vocabulary, specific to the target literature (book, article, etc.), recieving translations into the destination language and building a dictionary. It can be helpful for learning lexicon in the specific fields of knowledge. BookDict uses [lingvolive.com](http://lingvolive.com) web API to get translations of words.

## Setup

You can run BookDict with virtual environment or insall required packages globally.

   1. BookDict requires Python 3 so first of all check if it's installed in your system, otherwise:

        ```
        $ sudo apt-get install python3
        ```
        *for Ubuntu*

   2. Setup virtual environment:

        ```
        $ sudo apt-get install python3-venv
        ```

   3. Enter the BookDict directory and create virtual environment:

        ```
        $ python3 -m venv venv
        ```

   4. Activate virtual environment:

        ```
        $ source venv/bin/activate
        ```

   5. Install required packages:

        ```
        $ pip3 install requests epub bs4 nltk
        ```

   6. Run Python and download wordnet dictionary:

        ```python
        >>> import nltk
        >>> nltk.download('wordnet')
        ```

   7. Add [lingvolive.com](http://lingvolive.com) SSL sertificate to your virtual environment by running `add_lingvocert.py` script:

        ```
        $ python3 add_lingvocert.py
        ```

## How to use

   1. Accuire Lingvo API key at [developers.lingvolive.com](developers.lingvolive.com). Put it into the `lingvoapi_key` file  and place it in the repository folder.

   2. Put desired book in the `books` folder (only 'epub' format is currently supported).

   3. Activate virtual environment and run `build.py` script:

        ```
        $ source venv/bin/activate
        $ python3 build.py
        ```

   4. You'll be prompted to enter path to the book file and destination language (only English language is currently supported as the source language). The script will build 3 files in the vocabulary folder:

        - <book_name>.rst - book vocabulary
        - <book_name>.json - translation wildcards recieved from lingvolive.com
        - <book_name>.dict - dictionary of words and translations

Translation process may take some time depending on the amount of words to be translated. This depends on the words excluded from translation. These are basic 3000 English words that are stored in the file `vocabulary/familiar/3000words.rst`. This list may be extended by adding new files to vocabulary/familiar folder. Additional vocabulary can be generated on the first use by running two scripts separately:

   1. Build vocabulary. Edit book name in `readbook.py` and run it:
        ```
        $ python3 readbook.py
        ```
   2. Run through the `<book_name>.rst` file and [comment](http://docutils.sourceforge.net/docs/user/rst/quickref.html#comments) known words by adding `..` in the beginning of a line.

   3. Edit path to vocabulary in `get_translations.py` script and run it:

        ```
        $ python3 get_translations.py
        ```

The additional vocabulary of familiar words will be generated in the `vocabulary/familiar` folder. These words will be excluded from translations. The list will be complemented with new words on the next use.


## Lingvo API

According to the [Terms of Use](https://developers.lingvolive.com/en-us/About/Terms) you can translate up to 50,000 characters per day for free. For this you require API token, which is granted for 24 hours. Thus you need to run `lingvo_api.py` script once a day. The list of supported languages can be found at [lingvolive.com](http://lingvolive.com).

## License (MIT)

Copyright (c) 2017 Vadym Pasko ([vadym-pasko.com](http://vadym-pasko.com))

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
