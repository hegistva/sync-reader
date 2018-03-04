
from terminaltables import AsciiTable
import spacy
import itertools
import numpy as np
import Levenshtein

from translate.libs import dico
from translate.libs import glove
from translate.libs import align

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
# text_eng = """A Runaway Reef    THE YEAR 1866 was marked by a bizarre development, an unexplained and downright inexplicable phenomenon that surely no one has forgotten."""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
# text_fra = """UN ÉCUEIL FUYANT  L'année 1866 fut marquée par un événement bizarre, un phénomène inexpliqué et inexplicable que personne n'a sans doute oublié."""

en = spacy.load('en')
fr = spacy.load('fr')

ed = en(text_eng)
fd = fr(text_fra)

vocab_en = { tok.lemma_ for tok in ed if tok.is_alpha}
vocab_fr = { tok.lemma_ for tok in fd if tok.is_alpha}

dico.setDefault('fra', 'eng')

trs = [dico.translateLemma(lemma) for lemma in vocab_fr]
tr_vocab = set(itertools.chain(*trs))

align.initAlignment(fd, ed)

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

def mapAtScore(minScore):
    for mts in align.Alignment.s2t:
        if mts.token.is_alpha and not mts.isMapped:
            trans = dico.translateToken(mts.token)
            tgtToken = None
            bestScore = 0.0
            for mtt in align.Alignment.t2s:
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

# map named entities
mapNamedEntities(confidence=0.5, sourceDoc=fd, targetDoc=ed)

# map numbers
mapNumbers(confidence=0.5, sourceMapping=align.Alignment.s2t, targetMapping=align.Alignment.t2s)

# structural mapping with exact dictionary match
mapAtScore(0.05)
mapAtScore(0.01)
mapAtScore(0.005)

# map in children

# display alignment
for m in align.Alignment.s2t:
    print(m)



# vectors = glove.getVector(vocab_en | tr_vocab)

# for word, vec in vectors.items():
#    print(word)
