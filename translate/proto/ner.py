
import spacy
import os
from Levenshtein import distance
import numpy as np
from translate.libs import dico

eng = spacy.load('en')
fra = spacy.load('fr')

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
# text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny"""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
# text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline"""

doc_eng = eng(text_eng)
doc_fra = fra(text_fra)


# named entity mappings
eng_names = [sp_eng.text.lower() for sp_eng in doc_eng.ents]
wordmap = []
mapped_fra = set()
mapped_eng = set()
for sp_fra in doc_fra.ents:
    text_fra = sp_fra.text.lower()
    dists = [distance(text_fra, eng_name) for eng_name in eng_names]
    idx_min = np.argmin(dists)
    eng_ent = doc_eng.ents[idx_min]
    if dists[idx_min] <= (len(text_fra) / 2):
        for idx_fr in range(sp_fra.start, sp_fra.end):
            for idx_en in range(eng_ent.start, eng_ent.end):
                mapped_fra.add(idx_fr)
                mapped_eng.add(idx_en)
                wordmap.append((idx_fr, idx_en))

for idx_fr, idx_en in wordmap:
    print("%s => %s" % (doc_fra[idx_fr], doc_eng[idx_en]))

# translation based mapping

dico.setDefault('fra', 'eng')

for idx_fra, token_fra in enumerate(doc_fra):
    if not idx_fra in mapped_fra:
        lemma_fra = token_fra.lemma_.lower()
        tr = dico.translateLemma(lemma_fra)
        for idx_eng, token_eng in enumerate(doc_eng):
            if not idx_eng in mapped_eng:
                lemma_eng = token_eng.lemma_.lower()
                if lemma_eng in tr:
                    print('EXACT MATCH FOUND!!! %s at %d to %s at %d' % (token_fra.text, idx_fra, token_eng.text, idx_eng))

# visualize the POS tagging resutls

html_fra = spacy.displacy.render(doc_fra, style='dep', options={'compact': True}, page=True)
html_eng = spacy.displacy.render(doc_eng, style='dep', options={'compact': True}, page=True)

VISUAL = 'cache/visual'

os.makedirs(VISUAL, exist_ok=True)

with open(os.path.join(VISUAL, 'fra.html'), 'w') as f:
    f.write(html_fra)

with open(os.path.join(VISUAL, 'eng.html'), 'w') as f:
    f.write(html_eng)


