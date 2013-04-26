#!/usr/bin/env python

from __future__ import print_function
import lxml
import lxml.etree
import collections
import sys
import tarfile
from collections import defaultdict
import nltk
import pp
from nltk.tokenize import sent_tokenize
from ref import Ref

with tarfile.open(sys.argv[1], 'r:gz') as tar:
    contentgen = (tar.extractfile(info).read() for idx, info in enumerate(tar) if info.isfile() and idx < 100000)
    for idx, content in enumerate(contentgen):
        doc = lxml.etree.fromstring(content)
        pmids = doc.xpath("/article/front/article-meta/article-id[@pub-id-type='pmid']")
        if len(pmids) <> 1:
            continue
        pmid = pmids[0].text
        back_refs = doc.xpath("/article/back/ref-list/ref")
        if len(back_refs) == 0:
            continue
        int_ext_ids = {}
        for ref in back_refs:
            int_id_tuple = ref.items()[0]
            ref_int_id = int_id_tuple[1]
            try:
                ref_ext_id = ref.xpath("mixed-citation/pub-id[@pub-id-type='pmid']")[0].text
            except IndexError:
                continue
            int_ext_ids[ref_int_id] = ref_ext_id
        body_refs = [Ref(ref) for ref in doc.xpath("/article/body//xref[@ref-type='bibr']")]
        for ref in body_refs:
            section_title = ref.get_section_title()
            section_title = section_title.replace('\t', ' ')
            section_title = section_title.replace('\n', ' ')
            if section_title.strip() == "":
                print(ref.get_sentence(), ref.element.getparent(), ref.element.getparent().getparent(), ref.element.getparent().getparent().getparent())
            ref_id = ref.element.values()[1]
            try:
                ref_pmc_id = int_ext_ids[ref_id]
            except KeyError:
                continue
            par = ''.join((ref.get_text_before(),'*', ref_pmc_id, '*', ref.get_text_after()))
            par = par.replace('\t', ' ')
            par = par.replace('\n', ' ')
            
            #print("%s\t%s\t%d\t%s\t%s" % (pmid, ref_pmc_id, ref.get_depth(), section_title, par))
# vim:et:sw=3:ts=4
