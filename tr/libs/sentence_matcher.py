
from nltk.translate import gale_church

from tr.libs import utils
from tr.libs import glove

def alignSentences(lang_source, lang_target, text_source, text_target):
    # get spacy models for language processing
    sp_source = utils.getSpacy(lang_source)
    sp_target = utils.getSpacy(lang_target)
    doc_source = sp_source(text_source)
    doc_target = sp_target(text_target)
    
    # if we use english, use load the embeddings in a single step to improve performance
    eng_doc = None
    if lang_source == 'eng':
        eng_doc = doc_source
    elif lang_target == 'eng':
        eng_doc = doc_target
    if not eng_doc is None:    
        words = { t.lemma_.lower() for t in eng_doc if t.is_alpha }
        glove.getVector(words)

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