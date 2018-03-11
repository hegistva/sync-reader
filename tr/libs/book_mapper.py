from tr.books import book_manager
from tr.libs import sentence_mapper
from tr.libs import sentence_matcher
from tr.libs import lemma_mapper
from tr.libs import align

def mapChapter(source_lang, target_lang, bookid, chapter, debug=False):
    source_path = book_manager.chapterPath(source_lang, bookid, chapter)
    target_path = book_manager.chapterPath(target_lang, bookid, chapter)
    with open(source_path, 'r') as sf, open(target_path, 'r') as tf:        
        source_text = sf.read()
        target_text = tf.read()
        blocks = sentence_matcher.alignSentences(source_lang, target_lang, source_text, target_text)
        for source_block, target_block in blocks:
            sentence_mapper.mapSentence(source_lang, target_lang, source_block, target_block, debug=debug)
    print('Completed mapping chapter %s' % chapter)   
        

def mapBook(source_lang, target_lang, bookid):
    
    lemma_mapper.reset(source_lang, target_lang)
    chlist = book_manager.allChapters(bookid, source_lang)
    for ch in chlist:
        mapChapter(source_lang, target_lang, bookid, ch)        
    lemma_mapper.printMapping()