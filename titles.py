#!/usr/bin/env python

from __future__ import print_function
import lxml.etree
import sys
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import sent_tokenize
from ref import Ref, ExRef

from tools import ref_gen, filter_out_stopwords, is_word, count_words, print_sorted
from itertools import islice
from multiprocessing import Pool

def merge_dicts(list_of_dicts):
    ret = defaultdict(lambda: defaultdict(int))
    for dictionary in list_of_dicts:
        for pmid, titles in dictionary.items():
            for title, count in titles.items():
                ret[pmid][title] += count
    return ret

def count_paragraph_titles_for_citations(file_path):
    id_titles_dict = defaultdict(Counter) #e.g. {"1233242":{"introduction":1234. "background":123}}
    for idx, ref in enumerate(ref_gen(file_path)):
        if idx % 100 == 0:
            print(idx)
        title = ref.title.lower()
        id_titles_dict[ref.cited_id][title] += 1
    return id_titles_dict
    
if __name__ == "__main__":
    title_counts_dicts = map(count_paragraph_titles_for_citations, sys.argv[1:])
    title_counts_dict = merge_dicts(title_counts_dicts)
    articles = [(pmid, counts) for (pmid, counts) in title_counts_dict.items() if sum([item[1] for item in counts.items()]) > 20]
    for pmid, titles_dict in sorted(articles, key=lambda x: sum([item[1] for item in x[1].items()])):
        print(pmid, [(title, count) for (title, count) in sorted(titles_dict.items(), key=lambda x: -x[1])])
# vim:et:sw=3:ts=4