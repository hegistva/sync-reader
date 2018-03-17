import numpy as np
import math
from nltk.translate import gale_church

from tr.libs.trans import utils
from tr.libs.trans import glove
from tr.libs.trans import lemma_mapper


def alignSentences(lang_source, lang_target, text_source, text_target):
    # get spacy models for language processing
    sp_source = utils.getSpacy(lang_source)
    sp_target = utils.getSpacy(lang_target)
    doc_source = sp_source(text_source)
    doc_target = sp_target(text_target)
    
    # if we use english, use load the embeddings in a single step to improve performance
    eng_doc = None
    if lang_source == utils.Lang.ENG:
        eng_doc = doc_source
    elif lang_target == utils.Lang.ENG:
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

def alignSimilar(lang_source, lang_target, text_source, text_target):
    # get spacy models for language processing
    sp_source = utils.getSpacy(lang_source)
    sp_target = utils.getSpacy(lang_target)
    doc_source = sp_source(text_source)
    doc_target = sp_target(text_target)

    source_sents = list(doc_source.sents)
    target_sents = list(doc_target.sents)

    source_lens = np.cumsum([len([word for word in sent if word.is_alpha]) for  sent in source_sents])
    target_lens = np.cumsum([len([word for word in sent if word.is_alpha]) for  sent in target_sents])
    source_lens = source_lens / source_lens[-1]
    target_lens = target_lens / target_lens[-1]

    source_match = 0
    target_match = 0
    matches = []
    while source_match < 5 and target_match < 5:
        source_match, target_match = nextMatch(source_sents, target_sents, source_lens, target_lens, source_match, target_match)
        matches.append((source_match, target_match))
        source_match += 1
        target_match += 1
    printMatches(source_sents, target_sents, matches)

def printMatches(source_sents, target_sents, matches):
    sst = [sent.string for sent in source_sents]
    tst = [sent.string for sent in target_sents]
    prev_m = (-1, -1)
    for m in matches:        
        src = '|'.join(sst[prev_m[0]+1:m[0]+1])
        tgt = '|'.join(tst[prev_m[1]+1:m[1]+1])
        print("\n%s\n=>\n%s\n" % (src, tgt))
        prev_m = m

def nextMatch(source_sents, target_sents, source_lens, target_lens, source_start, target_start):
    s_prev = 0.0 if source_start <= 0 else source_lens[source_start - 1]
    min_dist = 1000.0
    min_s = 0
    min_t = 0
    source_count = min(3, len(source_lens)-source_start)
    target_count = min(3, len(target_lens)-target_start)
    
    if source_count <= 1 or target_count <= 1:
        return (len(source_lens), len(target_lens)) # we are at the end

    allLengths = []
    for si in range(source_count):
        s = si + source_start
        s_length = source_lens[s] - s_prev # relative length of the source expression [0-1]
        allLengths.append(s_length)
    allLengths = np.cumsum(allLengths)
    allLengths = allLengths / allLengths[-1]
    print(allLengths)

    allSims = []
    for ti in range(target_count):
        t = ti + target_start
        tsent = target_sents[t]
        sims = []
        for si in range(source_count):
            s = si + source_start
            ssent = source_sents[s]
            sims.append(sentSimilarity(ssent, tsent))
        sims = np.cumsum(sims)
        sims = sims / sims[-1]
        allSims.append(sims)
    print(allSims)

    # otherwise find the shortest best match
    for si in range(source_count):
        s = si + source_start        
        for ti in range(target_count):
            dist = abs(source_lens[s] - target_lens[t]) # distance (relative) [0-1] the smaller the better
            s_length = source_lens[s] - s_prev # relative length of the source expression [0-1]
            prob =  allSims[ti][si] # probability that the target maps to or before the source
            if dist < min_dist:
                min_dist = dist
                min_s = s
                min_t = t
    return (min_s, min_t)

def sentSimilarity(ssent, tsent):
    sim = 0.0
    cnt = 0
    for s in ssent:
        if s.is_alpha and s.lemma_:
            cnt += 1
            maxProb = 0.0
            for t in tsent:
                if t.is_alpha and t.lemma_:
                    prob = lemma_mapper.getProbability(s.lemma_.lower(), t.lemma_.lower())
                    if prob > maxProb:
                        maxProb = prob
            sim += maxProb
    return sim / cnt