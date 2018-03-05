import numpy as np
import Levenshtein
from translate.libs import align
from translate.libs import dico

def mapNamedEntities(confidence, sourceDoc, targetDoc):
    """map named entities from the source document to the target document"""
    targetNames = [sp.text.lower() for sp in targetDoc.ents]
    targetEnts = list(targetDoc.ents)

    for sourceName in sourceDoc.ents:
        sourceText = sourceName.text.lower()        
        dists = [Levenshtein.distance(sourceText, targetText) for targetText in targetNames]
        idxMin = np.argmin(dists)
        targetName = targetEnts[idxMin]        
        prob = 1 - dists[idxMin] / len(sourceText)
        if prob >= confidence:
            del targetNames[idxMin] # found a match, remove target
            del targetEnts[idxMin]
            for idxSource in range(sourceName.start, sourceName.end):
                align.MAPPING.source.tokens[idxSource].mapTo(align.MapTarget(targetName.start, 'NER', prob))

def mapNumbers(confidence):
    for sourceToken in align.MAPPING.source.tokens:
        if sourceToken.token.is_digit and not sourceToken.isMapped:
            for targetToken in align.MAPPING.target.tokens:
                if targetToken.token.is_digit and not targetToken.isMapped:
                    d = Levenshtein.distance(sourceToken.token.text, targetToken.token.text)
                    prob = 1 - d / len(sourceToken.token.text)
                    if prob >= confidence:
                        sourceToken.mapTo(align.MapTarget(targetToken.token.i, 'NUMBER', prob))

def mapBaseStructure(minScore):
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and not mts.isMapped:
            trans = dico.translateToken(mts.token)
            tgtToken = None
            bestScore = 0.0
            for mtt in align.MAPPING.target.tokens:
                if mtt.token.is_alpha and not mtt.isMapped:
                    # calculate a score for the pair
                    scorePos = 0.5 + 0.5 * (mts.token.pos_ == mtt.token.pos_)
                    scoreSize = mts.graphSize * mtt.graphSize
                    scorePosition = 1.0 - abs(mts.relativePosition - mtt.relativePosition)
                    score = scoreSize * scorePos * scorePosition
                    if score  > minScore:
                        if (mtt.token.text.lower() in trans) or (mtt.token.lemma_.lower() in trans):
                            if score > bestScore:
                                tgtToken = mtt
                                bestScore = score
            if not tgtToken is None:
                mts.mapTo(align.MapTarget(tgtToken.token.i, 'BASE_STRUCT', bestScore))

def mapBaseNoTranslate(minScore):
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and not mts.isMapped:
            trans = dico.translateToken(mts.token)
            if not trans: # if there is no translation for the term
                tgtToken = None
                bestScore = 0.0
                for mtt in align.MAPPING.target.tokens:
                    if mtt.token.is_alpha and not mtt.isMapped:
                        # calculate a score for the pair
                        scorePos = 0.5 + 0.5 * (mts.token.pos_ == mtt.token.pos_)
                        scoreSize = mts.graphSize * mtt.graphSize
                        scorePosition = 1.0 - abs(mts.relativePosition - mtt.relativePosition)
                        score = scoreSize * scorePos * scorePosition
                        if score  > minScore and score > bestScore:
                            tgtToken = mtt
                            bestScore = score
                if not tgtToken is None:
                    mts.mapTo(align.MapTarget(tgtToken.token.i, 'BASE_NO_TRANSLATE', bestScore))

def mapDependents(minScore):
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and mts.isMapped:            
            for ms_child in mts.dependents:
                if ms_child.token.is_alpha and not ms_child.isMapped: # if source is not mapped yet
                    trans = dico.translateToken(ms_child.token) # translate
                    tgtMapping = None # best target token
                    bestScore = 0.0 # best matching score
                    for mt_child in mts.mapTarget.target.dependents:
                        if mt_child.token.is_alpha and not mt_child.isMapped: # if target is not mapped yet                                            
                            # calculate a socore for the pair
                            scorePos = 0.5 + 0.5 * (ms_child.token.pos_ == mt_child.token.pos_)
                            scorePosition = 1.0 - abs(ms_child.relativePosition - mt_child.relativePosition)
                            score = scorePos * scorePosition
                            if score  > minScore:
                                if (mt_child.token.text.lower() in trans) or (mt_child.token.lemma_.lower() in trans):
                                    if score > bestScore:
                                        tgtMapping = mt_child
                                        bestScore = score
                    if not tgtMapping is None:
                        ms_child.mapTo(align.MapTarget(tgtMapping.token.i, 'DEPENDENT', bestScore))

def mapTranslatables(minScore):
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and not mts.isMapped:
            trans = dico.translateToken(mts.token)
            tgtToken = None
            bestScore = 0.0
            for mtt in align.MAPPING.target.tokens:
                if mtt.token.is_alpha and not mtt.isMapped:
                    # calculate a score for the pair
                    scorePos = 0.1 + 0.9 * (mts.token.pos_ == mtt.token.pos_)
                    scorePosition = 1.0 - abs(mts.relativePosition - mtt.relativePosition)
                    score = scorePos * scorePosition
                    if score  > minScore:
                        if (mtt.token.text.lower() in trans) or (mtt.token.lemma_.lower() in trans):
                            if score > bestScore:
                                tgtToken = mtt
                                bestScore = score
            if not tgtToken is None:
                mts.mapTo(align.MapTarget(tgtToken.token.i, 'ALL_TRANSLATABLE', bestScore))