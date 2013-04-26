#!/usr/bin/env python

from __future__ import print_function
import collections
import sys
from collections import defaultdict, Counter, namedtuple
from ref import Ref, ExRef

from tools import ref_gen, smart_tokenize, filter_out_stopwords, is_word, count_words, print_sorted

def get_sentiment_words():
    with open("positive.csv", 'r') as source:
        positive_word_lines = [line.strip() for line in source.readlines()]
    positive_words = set([line.split(',')[0].lower() for line in positive_word_lines])

    with open("negative.csv", 'r') as source:
        negative_word_lines = [line.strip() for line in source.readlines()]
    negative_words = set([line.split(',')[0].lower() for line in positive_word_lines])

    return positive_words.union(negative_words)

sentiment_words = get_sentiment_words()


def find_cits_with_sentiment_words(file_path):
    ret = set()
    for idx, ref in enumerate(ref_gen(file_path)):
        if idx % 100 == 0:
            print(idx)
        tokens = set(smart_tokenize(ref.get_sentence()))
        intersect = tokens.intersection(sentiment_words)
        if len(intersect) <> 0:
            ret.add(ref, list(intersect))
    return ret

if __name__ == "__main__":
    file_paths = sys.argv[1:]

    ref_sets_list = map(find_cits_with_sentiment_words, file_paths)
    ref_set = reduce(lambda x,y: x.union(y), ref_sets_list)
    ref_list = sorted(list(ref_set), key=lambda x: x[0].cited_id)

    for ref in ref_list:
        print(ref[0].cited_id, ','.join(ref[1]), ref[0].get_sentence())

# vim:et:sw=3:ts=4
