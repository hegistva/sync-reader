
import os
from nltk.translate import gale_church
import spacy
from tr.libs import sentence_mapper
from tr.libs import lemma_mapper

eng = spacy.load('en')
fra = spacy.load('fr')

parsers = {
    'eng': eng,
    'fra': fra
}

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
                blocks.append((src_block, tgt_block))
            src_set.clear()
            tgt_set.clear()
            src_set.add(src_idx)
            tgt_set.add(tgt_idx)
    if len(src_set) or len(tgt_set):
        src_block = ' '.join([sent_source[i] for i in sorted(src_set)])
        tgt_block = ' '.join([sent_target[i] for i in sorted(tgt_set)])
        blocks.append((src_block, tgt_block))
    return blocks

def mapChapter(source_lang, target_lang, book, chapter):
    blocks = alignSentences(book, chapter, source_lang, target_lang)
    for source_sent, target_sent in blocks:
        sentence_mapper.mapSentence(source_lang, target_lang, source_sent, target_sent)
    lemma_mapper.printMapping()

mapChapter('fra', 'eng', '20000LeaguesUnderTheSea', 1)
