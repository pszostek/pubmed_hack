from __future__ import print_function
import lxml
import lxml.etree
import collections
import tarfile
from collections import defaultdict
import nltk
import pp
from nltk.tokenize import sent_tokenize
from ref import Ref, ExRef

def ref_gen(file_path):
    with open(file_path, 'r') as content:
        line_gen = (line.strip() for line in content.readlines())
        for line in line_gen:
            yield ExRef(line)

def filter_out_stopwords(words):
    stopwords = set(["a", "able", "about", "across", "after", "al", "all", "almost", "also", "am",
    "among", "an", "and", "any", "are", "as", "at", "be", "because", "been", "but", "by",
    "can", "cannot", "could", "dear", "did", "do", "does", "either", "else", "ever", "et",
    "every", "for", "from", "get", "got", "had", "has", "have", "he", "her", "hers",
    "him", "his", "how", "however", "i", "if", "in","into", "is", "it", "its",
    "just", "least", "let", "like", "likely", "may", "me", "might", "most", "must",
    "my", "neither", "no", "nor", "not", "of", "off", "often", "on", "only", "or",
    "other", "our", "own", "rather", "said", "say", "says", "she", "should",
    "since", "so", "some", "than", "that", "the", "their", "them", "then", "there",
    "these", "they", "this", "tis", "to", "too", "twas", "us", "wants", "was", "we",
    "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will",
    "with", "would", "yet", "you", "your"])
    ret = [w for w in words if w not in stopwords]
    return ret

def is_word(word):
    for char in word:
        if not char.isalpha():
            return False
    return True

def smart_tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = filter_out_stopwords(tokens)
    tokens = [token for token in tokens if is_word(token)]
    return tokens

def count_words(text):
    assert text is None or isinstance(text, basestring)
    if text is None:
        return {}
    tokens = smart_tokenize(text)
    token_count = collections.defaultdict(int)

    for token in tokens:
        token_count[token] += 1
    return token_count

def print_sorted(dictionary):
    assert isinstance(dictionary, dict)
    sorted_tokens = sorted(dictionary.iteritems(), key=lambda x: x[1])
    for token in sorted_tokens:
        print(token)