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

from tools import smart_tokenize,  filter_out_stopwords, is_word, count_words, print_sorted
from itertools import islice

def merge_dicts(list_of_dicts):
    ret = defaultdict(int)
    for dictionary in list_of_dicts:
        for key, value in dictionary.items():
            ret[key] += value
    return ret

def process(file_path):
    before_count = Counter()
    cur_count = Counter()
    after_count = Counter()
    with open(file_path, 'r') as content:
        line_gen = (line.strip() for line in content.readlines())
        refgen = (ExRef(line) for line in line_gen)
        for  idx, ref in enumerate(refgen):
            sent_before = ref.get_sentence(-1)
            sent_cur = ref.get_sentence(0)
            sent_after = ref.get_sentence(1)
            if idx % 100 == 0:
                print(idx)
            before_count += Counter(smart_tokenize(sent_before))
            cur_count += Counter(smart_tokenize(sent_cur))
            after_count += Counter(smart_tokenize(sent_after))
    return (before_count, cur_count, after_count)


if __name__ == "__main__":
    counts = map(process, sys.argv[1:])
    before_count = merge_dicts(zip(*counts)[0])
    cur_count = merge_dicts(zip(*counts)[1])
    after_count = merge_dicts(zip(*counts)[2])

    print_sorted(before_count)
    print(">>>>")
    print_sorted(cur_count)
    print(">>>>")
    print_sorted(after_count)
    print(">>>>")

# vim:et:sw=3:ts=4
