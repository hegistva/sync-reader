
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
                align.Alignment.s2t[idxSource].mapTo(align.MapTarget(targetDoc[targetName.start], prob))

def mapNumbers(confidence, sourceMapping, targetMapping):
    for sourceToken in sourceMapping:
        if sourceToken.token.is_digit and not sourceToken.isMapped:
            for targetToken in targetMapping:
                if targetToken.token.is_digit and not targetToken.isMapped:
                    d = Levenshtein.distance(sourceToken.token.text, targetToken.token.text)
                    prob = 1 - d / len(sourceToken.token.text)
                    if prob >= confidence:
                        sourceToken.mapTo(align.MapTarget(targetToken.token, prob))

def mapAtScore(minScore, sourceMapping, targetMapping):
    for mts in sourceMapping:
        if mts.token.is_alpha and not mts.isMapped:
            trans = dico.translateToken(mts.token)
            tgtToken = None
            bestScore = 0.0
            for mtt in targetMapping:
                if mtt.token.is_alpha and not mtt.isMapped:
                    # calculate a socore for the pair
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
                mts.mapTo(align.MapTarget(tgtToken.token, bestScore))