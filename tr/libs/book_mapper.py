from tr.books import book_manager
from tr.libs import sentence_mapper
from tr.libs import sentence_matcher
from tr.libs import lemma_mapper
from tr.libs import align

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