#!/usr/bin/env python

from __future__ import print_function
import lxml
import lxml.etree
import collections
import sys
import tarfile
from collections import defaultdict, Counter
import nltk
import pp
from nltk.tokenize import sent_tokenize
from ref import Ref, ExRef
from functools import partial

from tools import ref_gen, smart_tokenize, filter_out_stopwords, is_word, count_words, print_sorted
from itertools import islice

POPULARITY_TRESHOLD = 5

def merge_dicts(list_of_dicts):
    ret = defaultdict(Counter)
    for dictionary in list_of_dicts:
        for pmid, count_dict in dictionary.items():
            for word, count in count_dict.items():
                ret[pmid][word] += count
    return ret

def calculate_popularity(file_path):
    references_count = Counter()
    for idx, ref in enumerate(ref_gen(file_path)):
        if idx % 100 == 0:
            print("cp %d" % idx)
        references_count[ref.cited_id] += 1
    return references_count

def count_words_in_context(file_path, popular_pmids):
    word_count = defaultdict(Counter)
    for idx, ref in enumerate(ref_gen(file_path)):
        if idx % 100 == 0:
            print(idx)
        if ref.cited_id not in popular_pmids:
            continue
        citing_sentence = ref.get_sentence(0)
        tokens = smart_tokenize(citing_sentence)
        word_count[ref.cited_id] += Counter(tokens)
    return word_count

if __name__ == "__main__":
    file_paths = sys.argv[1:]
    popularities_list = map(calculate_popularity, file_paths) # ((ref_count1, word_count1), (ref_count2, word_count2),...)
    popularity = reduce(lambda c1,c2: c1+c2, popularities_list)
    popular_pmids = set([item[0] for item in popularity.items() if item[1] > POPULARITY_TRESHOLD])

    word_counts = map(partial(count_words_in_context, popular_pmids=popular_pmids), file_paths)
    merged_word_counts = merge_dicts(word_counts)

    for pmid, counts in merged_word_counts.items():
            print(pmid, counts) 

# vim:et:sw=3:ts=4
