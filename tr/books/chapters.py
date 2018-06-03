

import re
import json
import os
import csv

from tr.books import book_manager

class Chapter(object):
    
    @staticmethod
    def fields():
        return ['id', 'firstLine', 'lastLine', 'audioFile']

    def __init__(self, idx, audio_fn):
        self.id = idx
        self.audioFile = audio_fn
        self.firstLine = -1
        self.lastLine = -1

    def row(self):
        return [self.id, self.firstLine, self.lastLine, self.audioFile]

    def __str__(self):
        return "Chapter %s [%s-%s] (%s)" % (self.id, self.firstLine, self.lastLine, self.audioFile)
    
def extract(bookid, lang, ch_re, audio_pattern, first_line, last_line):
    """extract the chapter boundaries of a book"""
    p = re.compile(ch_re)
    book_file = book_manager.bookPath(bookid, lang)
    last_non_empty = -1
    chs = []
    ch = None
    ch_idx = 0 
    with open(book_file, 'r') as bf:
        lines = bf.readlines()
        for idx, line in enumerate(lines):
            line_num = idx + 1
            if line_num < first_line:
                continue
            if line_num == last_line:
                ch.lastLine = line_num
                chs.append(ch)
                break
            l = line.strip()
            m = p.match(l)
            if not m is None:
                ch_idx += 1
                if not ch is None:
                    ch.lastLine = last_non_empty
                    chs.append(ch)                
                ch = Chapter(ch_idx, audio_pattern % ch_idx)
            else:
                if l:
                    last_non_empty = line_num
                    if not ch is None and ch.firstLine == -1:
                        ch.firstLine = line_num
    ch_file = os.path.join(os.path.dirname(book_file), "chapters.csv")
    with open(ch_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(Chapter.fields())
        for c in chs:
            writer.writerow(c.row())
                            