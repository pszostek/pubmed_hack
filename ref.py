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

"""Extracted Reference abstraction"""
class ExRef(object):
    def __init__(self, line):
        parts = line.split('\t')
        try:
            (self.id, self.cited_id, self.level, self.title, self.par) = parts
        except ValueError:
            print(parts)
            raise

    def get_text_before(self):
        id_idx = self.par.index(self.cited_id)
        return self.par[:id_idx-1]

    def get_text_after(self):
        id_idx = self.par.index(self.cited_id)
        return self.par[id_idx+len(self.cited_id)+1:]

    def get_sentence(self, offset=None):
        sentences_before = sent_tokenize(self.get_text_before())
        sentences_after = sent_tokenize(self.get_text_after())
        sentences_before[-1] += ' ' + sentences_after[0]
        sentences_after = sentences_after[1:]
        #sentences_before[-1] contains the citation
        #sentences_after[0] contains 1st sentence after citation
        #sentences_before[-2] contains the last sentence before citaion
        if offset is None or offset == 0:
            return sentences_before[-1]
        else:
            if offset > 0:
                try:
                    return sentences_after[offset-1]
                except IndexError:
                    return None
            else: #offset < 0
                try:
                    return sentences_before[offset-1]
                except IndexError:
                    return None

"""In-text reference abstraction"""
class Ref(object):
    def __init__(self, element):
        assert isinstance(element, lxml.etree._Element)
        self.element = element

    def get_paragraph(self):
        return ' '.join([text.encode('utf-8') for text in self.element.getparent().itertext()])

    def get_text_before(self):
        parent = self.element.getparent()

        parent_texts = list([text.encode('utf-8') for text in parent.itertext()])
        if parent_texts.count(self.get_text()) > 1:
            parent_children = parent.getchildren()
            this_index = 0
            for child in parent_children:
                if child.text and child.text.encode('utf-8') == self.get_text():
                    this_index += 1
                    if child == self.element:
                        break
            ret = []
            like_this_so_far = 0
            for text in parent_texts:
                if text == self.get_text():
                    like_this_so_far += 1
                if like_this_so_far == this_index:
                    break
                ret.append(text)
            return ' '.join(ret)
        else:
            try:
                ref_idx = parent_texts.index(self.get_text())
            except ValueError:
                return ''
            except AttributeError:
                return ''
            return ' '.join(parent_texts[:ref_idx])

    def get_text_after(self):
        parent = self.element.getparent()
        parent_texts = list([text.encode('utf-8') for text in parent.itertext()])
        if parent_texts.count(self.get_text()) > 1:
            parent_children = parent.getchildren()
            this_index = 0
            for child in parent_children:
                if child.text and child.text.encode('utf-8') == self.get_text():
                    this_index += 1
                    if child == self.element:
                        break
            ret = []
            like_this_so_far = 0
            for idx, text in enumerate(parent_texts):
                if text == self.get_text():
                    like_this_so_far += 1
                if like_this_so_far == this_index:
                    return ' '.join(parent_texts[idx+1:])
        else:
            try:
                ref_idx = parent_texts.index(self.get_text())
            except ValueError:
                return ''
            except AttributeError:
                return ''
            return ' '.join(parent_texts[ref_idx+1:])

    def get_text(self):
        return self.element.text.encode('utf-8') if self.element.text else ''

    def get_sentence(self, offset=None):
        sentences_before = sent_tokenize(self.get_text_before())
        sentences_after = sent_tokenize(self.get_text_after())
        sentences_before[-1] += ' ' + sentences_after[0]
        sentences_after = sentences_after[1:]
        #sentences_before[-1] contains the citation
        #sentences_after[0] contains 1st sentence after citation
        #sentences_before[-2] contains the last sentence before citaion
        if offset is None or offset == 0:
            return sentences_before[-1]
        else:
            if offset > 0:
                try:
                    return sentences_after[offset-1]
                except IndexError:
                    return None
            else: #offset < 0
                try:
                    return sentences_before[offset-1]
                except IndexError:
                    return None
    
    def get_section_title(self):
        try:
            title = self.element.getparent().getparent().xpath("title")[0].text.encode('utf-8').strip()
            return title if title <> None else ""
        except:
            return ""
    
    def get_depth(self):
        depth = 0
        cur = self.element
        while cur.tag <> 'body':
            cur = cur.getparent()
            if cur.tag == "sec":
                depth += 1
        return depth