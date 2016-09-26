import re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords  # Import the stop word list
from stemming.porter2 import stem
import Config
from Utils import textmining


def textCleaner(input):
    # 1. Remove HTML
    # To avoid joining of words when html is cleaned we add spaces
    input = input.replace("<"," <")
    input = input.replace(">", "> ")
    html_free_text = BeautifulSoup(input, "html.parser").get_text()
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", html_free_text)
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    # 5. Remove stop words
    if Config.STEMMING:
        meaningful_words = [stem(w) for w in words if not w in stops]
    else:
        meaningful_words = [w for w in words if not w in stops]
    # 6. Stem the words to get rid of variations of the same word
    # 7. Translate the list to a string separated by spaces
    return meaningful_words


def parseinput(input):
    input = input.lower()
    if Config.STEMMING:
        input = [stem(w) for w in ",".split(input)].join(" ")
    output = [x.strip() for x in input.split(',')]
    return output
