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
                align.Alignment.s2t[idxSource].mapTo(align.MapTarget(targetName.start, 'NER', prob))

def mapNumbers(confidence, sourceMapping, targetMapping):
    for sourceToken in sourceMapping:
        if sourceToken.token.is_digit and not sourceToken.isMapped:
            for targetToken in targetMapping:
                if targetToken.token.is_digit and not targetToken.isMapped:
                    d = Levenshtein.distance(sourceToken.token.text, targetToken.token.text)
                    prob = 1 - d / len(sourceToken.token.text)
                    if prob >= confidence:
                        sourceToken.mapTo(align.MapTarget(targetToken.token.i, 'NUMBER', prob))

def mapBaseStructure(minScore, sourceMapping, targetMapping):
    for mts in sourceMapping:
        if mts.token.is_alpha and not mts.isMapped:
            trans = dico.translateToken(mts.token)
            tgtToken = None
            bestScore = 0.0
            for mtt in targetMapping:
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

def mapDependents(minScore, sourceMapping, targetMapping):
    for mts in sourceMapping:
        if mts.token.is_alpha and mts.isMapped:            
            for dep_source in mts.dependents:
                ms_child = sourceMapping[dep_source.i]
                if dep_source.is_alpha and not ms_child.isMapped: # if source is not mapped yet
                    trans = dico.translateToken(dep_source) # translate
                    tgtToken = None # best target token
                    bestScore = 0.0 # best matching score
                    for dep_target in mts.mapTarget.target.dependents:
                        mt_child = targetMapping[dep_target.i]
                        if dep_target.is_alpha and not mt_child.isMapped: # if target is not mapped yet                                            
                            # calculate a socore for the pair
                            scorePos = 0.5 + 0.5 * (dep_source.pos_ == dep_target.pos_)
                            scorePosition = 1.0 - abs(ms_child.relativePosition - mt_child.relativePosition)
                            score = scorePos * scorePosition
                            if score  > minScore:
                                if (dep_target.text.lower() in trans) or (dep_target.lemma_.lower() in trans):
                                    if score > bestScore:
                                        tgtToken = dep_target
                                        bestScore = score
                    if not tgtToken is None:
                        ms_child.mapTo(align.MapTarget(tgtToken.i, 'DEPENDENT', bestScore))