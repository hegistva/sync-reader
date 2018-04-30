import os

from tr.books import book_manager
from tr.libs.trans import sentence_mapper
from tr.libs.trans import sentence_matcher
from tr.libs.trans import lemma_mapper
from tr.libs.trans import align

def mapChapter(source_lang, target_lang, bookid, chapter, doMapping, debug=False):
    source_path = book_manager.chapterPath(source_lang, bookid, chapter)
    target_path = book_manager.chapterPath(target_lang, bookid, chapter)
    with open(source_path, 'r') as sf, open(target_path, 'r') as tf:        
        source_text = sf.read()
        target_text = tf.read()
        blocks = sentence_matcher.alignSentences(source_lang, target_lang, source_text, target_text)        
        for source_block, target_block in blocks:
            sentence_mapper.mapSentence(source_lang, target_lang, source_block, target_block, doMapping=doMapping, debug=debug)
    print('Completed mapping chapter %s' % chapter)   
        

def mapBook(source_lang, target_lang, bookid, chapters=None, chapterToPrint=None):    
    lemma_mapper.reset(source_lang, target_lang)
    chlist = book_manager.allChapters(bookid, source_lang)
    for ch in chlist:
        if chapters is None or ch in chapters:
            mapChapter(source_lang, target_lang, bookid, ch, doMapping=False, debug=False)
    for ch in chlist:
        if chapters is None or ch in chapters:
            debug = (ch == chapterToPrint)
            mapChapter(source_lang, target_lang, bookid, ch, doMapping=True, debug=debug)
    # lemma_mapper.printMapping()

# get the simple sentece level mapping between the source an the target
def beadMapChapter(source_lang, target_lang, bookid, chapter, saveResults=False):
    source_path = book_manager.chapterPath(source_lang, bookid, chapter)
    target_path = book_manager.chapterPath(target_lang, bookid, chapter)
    with open(source_path, 'r') as sf, open(target_path, 'r') as tf:        
        source_text = sf.read()
        target_text = tf.read()
        blocks = sentence_matcher.alignment(source_lang, target_lang, source_text, target_text)
    if saveResults:
        source_file = os.path.join(book_manager.chaptersPath(source_lang, bookid),book_manager.beadFile(chapter))
        target_file = os.path.join(book_manager.chaptersPath(target_lang, bookid),book_manager.beadFile(chapter))
        with open(source_file, 'w') as sourcef, open(target_file, 'w') as targetf:
            for block in blocks:
                sourcef.write("%d,%d\n" % block[:2])
                targetf.write("%d,%d\n" % block[2:])
    print('Completed bead mapping chapter %s' % chapter)
    return blocks

# run the sentence maping for a book
def beadMapBook(source_lang, target_lang, bookid, chapters=None):
    chlist = book_manager.allChapters(bookid, source_lang)
    for ch in chlist:
        if chapters is None or ch in chapters:
            beadMapChapter(source_lang, target_lang, bookid, ch, saveResults=True)