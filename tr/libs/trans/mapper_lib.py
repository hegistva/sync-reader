import numpy as np
import Levenshtein
from tr.libs.trans import align
from tr.libs.trans import utils
from tr.libs.trans import lemma_mapper

def mapNamedEntities(confidence, sourceDoc, targetDoc):
    """map named entities from the source document to the target document"""
    targetNames = [sp.text.lower() for sp in targetDoc.ents]
    if len(targetNames) == 0:
        return
    targetEnts = list(targetDoc.ents)

    for sourceName in sourceDoc.ents:
        sourceText = sourceName.text.lower()        
        dists = [Levenshtein.distance(sourceText, targetText) for targetText in targetNames]
        if len(dists) > 0:
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
                        if (mtt.token.text.lower() in mts.translations) or (mtt.token.lemma_.lower() in mts.translations):
                            if score > bestScore:
                                tgtToken = mtt
                                bestScore = score
            if not tgtToken is None:
                mts.mapTo(align.MapTarget(tgtToken.token.i, 'BASE_STRUCT', bestScore))

def mapBaseNoTranslate(minScore):
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and not mts.isMapped:            
            if not mts.translations: # if there is no translation for the term
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
                    tgtMapping = None # best target token
                    bestScore = 0.0 # best matching score
                    for mt_child in mts.mapTarget.target.dependents:
                        if mt_child.token.is_alpha and not mt_child.isMapped: # if target is not mapped yet                                            
                            # calculate a socore for the pair
                            scorePos = 0.5 + 0.5 * (ms_child.token.pos_ == mt_child.token.pos_)
                            scorePosition = 1.0 - abs(ms_child.relativePosition - mt_child.relativePosition)
                            score = scorePos * scorePosition
                            if score  > minScore:
                                if (mt_child.token.text.lower() in ms_child.translations) or (mt_child.token.lemma_.lower() in ms_child.translations):
                                    if score > bestScore:
                                        tgtMapping = mt_child
                                        bestScore = score
                    if not tgtMapping is None:
                        ms_child.mapTo(align.MapTarget(tgtMapping.token.i, 'DEPENDENT', bestScore))

def mapTranslatables(minScore):
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and not mts.isMapped:
            tgtToken = None
            bestScore = 0.0
            for mtt in align.MAPPING.target.tokens:
                if mtt.token.is_alpha and not mtt.isMapped:
                    # calculate a score for the pair
                    scorePos = 0.1 + 0.9 * (mts.token.pos_ == mtt.token.pos_)
                    scorePosition = 1.0 - abs(mts.relativePosition - mtt.relativePosition)
                    score = scorePos * scorePosition
                    if score  > minScore:
                        if (mtt.token.text.lower() in mts.translations) or (mtt.token.lemma_.lower() in mts.translations):
                            if score > bestScore:
                                tgtToken = mtt
                                bestScore = score
            if not tgtToken is None:
                mts.mapTo(align.MapTarget(tgtToken.token.i, 'MAP_TRANSLATABLE', bestScore))

# This does not really work need more structural work before this...
def mapGlove(bestOfN, doMapping=False, debug=False):
    header = ['Source', 'Translation', 'Target', 'Similarity']
    for mts in align.MAPPING.source.tokens:
        if mts.token.is_alpha and not mts.isMapped and mts.translateVectors and mts.token.lemma_:
            mappingTable = []
            candidates = []
            for mtt in align.MAPPING.target.tokens:
                if mtt.token.is_alpha and (not mtt.isMapped) and not mtt.vector is None:
                    # calculate a score for the pair
                    scorePosition = 1.0 - abs(mts.relativePosition - mtt.relativePosition)
                    mostSimilarTranslation = 0.0
                    for translation, vec in mts.translateVectors.items():
                        similarity = np.dot(mtt.vector, vec)
                        mappingTable.append([mts.token.text, translation, mtt.token.text, similarity])
                        mostSimilarTranslation = max(mostSimilarTranslation, similarity)
                    stopSocre = 0.5 + 0.5 * (mts.token.is_stop == mtt.token.is_stop)
                    score = scorePosition * mostSimilarTranslation * stopSocre
                    if mtt.token.lemma_:
                        if doMapping:
                            score = score * lemma_mapper.getProbability(mts.token.lemma_.lower(), mtt.token.lemma_.lower())
                        candidates.append((mtt, score))
            if candidates:
                candidates.sort(key=lambda c: c[1], reverse=True)
                if doMapping:
                    mts.mapTo(align.MapTarget(candidates[0][0].token.i, 'MAP_GLOVE', candidates[0][1]))                
                else:
                    best = candidates[:bestOfN]
                    sum_score=sum([score for (_, score) in best])
                    if sum_score > 0:
                        for mt, lm_score in best:
                            lemma_mapper.addMapping(mts.token.lemma_.lower(), mt.token.lemma_.lower(), probability=lm_score / sum_score)
            if debug:            
                utils.displayTable(mappingTable, header)