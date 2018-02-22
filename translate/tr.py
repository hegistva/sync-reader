
import os
import requests
from nltk.translate import gale_church
import spacy

en = spacy.load('en')
fr = spacy.load('fr')

parsers = {
    'en': en,
    'fr': fr
}

books = {
    '20000LeaguesUnderTheSea': {
        'fr': {
            'url': 'http://www.gutenberg.org/cache/epub/5097/pg5097.txt',
            'chapters': [(111, 365), (369, 604), (608, 844), (848, 1138), (1142, 1392),
            (1396, 1798), (1802, 2154), (2158, 2488), (2492, 2797), (2801, 3191)
            ]
        },
        'en': {
            'url': 'http://www.gutenberg.org/cache/epub/2488/pg2488.txt',
            'chapters': [(696, 958), (969, 1215),(1227, 1472), (1482, 1770), (1782, 2036),
            (2046, 2450), (2462, 2805), (2817, 3170), (3182, 3495), (3507, 3899),
            ]
        }
    }
}

BOOKS = './books'
CHAPTERS = 'chapters'
os.makedirs(BOOKS, exist_ok=True)

def chapterFile(chnum):
    return 'chapter_%04d.txt' % chnum

for title, langs in books.items():
    for lang, loc in langs.items():
        langpath = os.path.join(BOOKS, title, lang)
        os.makedirs(langpath, exist_ok=True)
        bookfile = os.path.join(langpath, 'book.txt')
        if not os.path.exists(bookfile):
            r = requests.get(loc['url'])
            with open(bookfile, 'w')  as bf:
                bf.write(r.text)
        ch_path = os.path.join(langpath, CHAPTERS)
        os.makedirs(ch_path, exist_ok=True)
        with open(bookfile, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            for ch_idx, (ch_start_line, ch_end_line) in enumerate(loc[CHAPTERS]):
                ch_file = chapterFile(ch_idx + 1)
                curr_ch = os.path.join(ch_path, ch_file)
                if not os.path.exists(curr_ch):
                    # extract and save chapter
                    ch_cont = ' '.join(lines[ch_start_line-1:ch_end_line+1])
                    with open(curr_ch, 'w') as chf:
                        chf.write(ch_cont)
                        print("Saved chapter %s" % curr_ch)

def analyze(title, chapter, lang):
    ch_file = os.path.join(BOOKS, title, lang, CHAPTERS, chapterFile(chapter))
    with open(ch_file, 'r') as chf:
        raw_text = chf.read()
        parser = parsers[lang]
        doc = parser(raw_text)        
        return doc

def alignSentences(title, chapter, lang_source, lang_target):
    doc_source = analyze(title, chapter, lang_source)
    doc_target = analyze(title, chapter, lang_target)
    sent_source = [sent.string.strip() for sent in doc_source.sents]
    sent_target = [sent.string.strip() for sent in doc_target.sents]
    len_source = [len(sent) for sent in sent_source]
    len_target = [len(sent) for sent in sent_target]
    alignment = gale_church.align_blocks(len_source, len_target)
    src_set = set()
    tgt_set = set()
    blocks = []
    for src_idx, tgt_idx in alignment:
        if src_idx in src_set or tgt_idx in tgt_set:
            src_set.add(src_idx)
            tgt_set.add(tgt_idx)
        else:
            if len(src_set) or len(tgt_set):
                src_block = ' '.join([sent_source[i] for i in sorted(src_set)])
                tgt_block = ' '.join([sent_target[i] for i in sorted(tgt_set)])
                blocks.append("%s => %s" % (src_block, tgt_block))
            src_set.clear()
            tgt_set.clear()
            src_set.add(src_idx)
            tgt_set.add(tgt_idx)
    if len(src_set) or len(tgt_set):
        src_block = ' '.join([sent_source[i] for i in sorted(src_set)])
        tgt_block = ' '.join([sent_target[i] for i in sorted(tgt_set)])
        blocks.append("%s\n=>\n%s" % (src_block, tgt_block))            
    return blocks

blocks = alignSentences('20000LeaguesUnderTheSea', 1, 'fr', 'en')

for idx, block in enumerate(blocks):
    print("BLOCK[%d]\n%s\n" % (idx, block))
