
import spacy
import os
from Levenshtein import distance
import numpy as np

eng = spacy.load('en')
fra = spacy.load('fr')

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""

doc_eng = eng(text_eng)
doc_fra = fra(text_fra)

eng_names = [sp_eng.text.lower() for sp_eng in doc_eng.ents]
fra_names = [sp_fra.text.lower() for sp_fra in doc_fra.ents]

print('FRENCH:')
print(fra_names)
print('ENGLISH:')
print(eng_names)

wordmap = []

for sp_fra in doc_fra.ents:
    text_fra = sp_fra.text.lower()
    dists = [distance(text_fra, eng_name) for eng_name in eng_names]
    idx_min = np.argmin(dists)
    eng_ent = doc_eng.ents[idx_min]
    if dists[idx_min] <= (len(text_fra) / 2):
        for idx_fr in range(sp_fra.start, sp_fra.end):
            for idx_en in range(eng_ent.start, eng_ent.end):
                wordmap.append((idx_fr, idx_en))

for idx_fr, idx_en in wordmap:
    print("%s => %s" % (doc_fra[idx_fr], doc_eng[idx_en]))

html_fra = spacy.displacy.render(doc_fra, style='dep', options={'compact': True}, page=True)
html_eng = spacy.displacy.render(doc_eng, style='dep', options={'compact': True}, page=True)

VISUAL = 'cache/visual'

os.makedirs(VISUAL, exist_ok=True)

with open(os.path.join(VISUAL, 'fra.html'), 'w') as f:
    f.write(html_fra)

with open(os.path.join(VISUAL, 'eng.html'), 'w') as f:
    f.write(html_eng)


