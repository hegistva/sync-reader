
import spacy
import os
import Levenshtein
import numpy as np
from translate.libs import dico

import colored
import functools

blue = functools.partial(colored.stylize, styles=colored.fore.BLUE)
green = functools.partial(colored.stylize, styles=colored.fore.GREEN)
red = functools.partial(colored.stylize, styles=colored.fore.RED)
yellow = functools.partial(colored.stylize, styles=colored.fore.YELLOW)
orange = functools.partial(colored.stylize, styles=colored.fore.DARK_ORANGE)
white = functools.partial(colored.stylize, styles=colored.fore.WHITE)

def colorForConf(confidence):        
    if confidence < 0.33:
        return orange
    elif confidence < 0.66:
        return yellow
    return green


# Classes to support mapping

class MapTarget(object):
    def __init__(self, target, confidence):
        self.target = target
        self.confidence = confidence
    def __str__(self):
        colorFn = colorForConf(self.confidence)
        return "%s [%s] at %d with confidence %.2f" % (colorFn(self.target.text), colorFn(self.target.lemma_), self.target.i, self.confidence)
        
class MappedToken(object):

    def __init__(self, token, source, ratio):
        self.source = source # source or target token
        self.ratio = ratio # relative position in the document/sentence
        self.token = token # token
        self.alternatives = [] # mapping alternatives (list of MapTarget objects)
        self.is_mapped = False # has the map target been selected yet
        self.mapped = None # map target (MapTarget object)
    
    def mapTo(self, mt, map_back=True):
        self.is_mapped = True
        self.mapped = mt
        if map_back:
            if self.source:
                Alignment.t2s[mt.target.i].mapTo(MapTarget(self.token, mt.confidence), map_back=False)
            else:
                Alignment.s2t[mt.target.i].mapTo(MapTarget(self.token, mt.confidence), map_back=False)

    def __str__(self):
        colorFn = blue
        if not self.is_mapped:
            colorFn = red
        else:
            colorFn = colorForConf(self.mapped.confidence)
        return "%s [%s] at %d (%.2f) mapped to %s" % (colorFn(self.token.text), colorFn(self.token.lemma_), self.token.i, self.ratio, self.mapped)

class Alignment(object):
    s2t = []
    t2s = []

eng = spacy.load('en')
fra = spacy.load('fr')

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
# text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny"""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
# text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline"""

doc_eng = eng(text_eng)
doc_fra = fra(text_fra)

def initMapping(doc, source):
    l = len(doc)
    return [MappedToken(tkn, source, tkn.i / l) for tkn in doc]

def initAlignment():
    Alignment.s2t = initMapping(doc_fra, source=True)
    Alignment.t2s = initMapping(doc_eng, source=False)

initAlignment()

# named entity mappings
eng_names = [sp_eng.text.lower() for sp_eng in doc_eng.ents]

for sp_fra in doc_fra.ents:
    text_fra = sp_fra.text.lower()
    dists = [Levenshtein.distance(text_fra, eng_name) for eng_name in eng_names]
    idx_min = np.argmin(dists)
    eng_ent = doc_eng.ents[idx_min]
    prob = 1 - dists[idx_min] / len(text_fra)
    if  prob >= 0.5:
        for idx_fr in range(sp_fra.start, sp_fra.end):
            for idx_en in range(eng_ent.start, eng_ent.end):
                Alignment.s2t[idx_fr].mapTo(MapTarget(doc_eng[idx_en], prob))


# number mapping
for mf in Alignment.s2t:
    if mf.token.is_digit:
        for token_eng in doc_eng:
            if token_eng.is_digit:
                d = Levenshtein.distance(mf.token.text, token_eng.text)                
                prob = 1 - d / len(mf.token.text)
                if prob >= 0.5:
                    mf.mapTo(MapTarget(token_eng, prob))

# translation based mapping

dico.setDefault('fra', 'eng')

for mf in Alignment.s2t:
    if not mf.is_mapped:
        lemma_fra = mf.token.lemma_.lower()
        tr = dico.translateLemma(lemma_fra)
        tokens_found = []
        for mt in Alignment.t2s: 
            if not mt.is_mapped:
                lemma_eng = mt.token.lemma_.lower()
                if lemma_eng in tr:
                    tokens_found.append(mt)
        if tokens_found and len(tokens_found) < 3:
            closest = min(tokens_found, key = lambda x: abs(mf.ratio - x.ratio))
            mf.mapTo(MapTarget(closest.token,  1.0-abs(mf.ratio-closest.ratio)))

# display alignment
for m in Alignment.s2t:
    print(m)

# visualize the POS tagging resutls

html_fra = spacy.displacy.render(doc_fra, style='dep', options={'compact': True}, page=True)
html_eng = spacy.displacy.render(doc_eng, style='dep', options={'compact': True}, page=True)

VISUAL = 'cache/visual'

os.makedirs(VISUAL, exist_ok=True)

with open(os.path.join(VISUAL, 'fra.html'), 'w') as f:
    f.write(html_fra)

with open(os.path.join(VISUAL, 'eng.html'), 'w') as f:
    f.write(html_eng)


