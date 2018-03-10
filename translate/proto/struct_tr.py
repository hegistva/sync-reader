import os
import spacy
from translate.libs import align
from translate.libs import mapper

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
text_eng = """A Runaway Reef    THE YEAR 1866 was marked by a bizarre development, an unexplained and downright inexplicable phenomenon that surely no one has forgotten."""
# text_eng = """This outrageous animal had to shoulder responsibility for all derelict vessels, whose numbers are unfortunately considerable, since out of those 3,000 ships whose losses are recorded annually at themarine insurance bureau, the figure for steam or sailing ships supposedly lost with all hands, in the absence of any news, amounts to at least 200!"""
# text_eng = """Indeed, from this moment on, any maritime casualty without an established cause was charged to the monster's account."""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
text_fra = """UN ÉCUEIL FUYANT  L'année 1866 fut marquée par un événement bizarre, un phénomène inexpliqué et inexplicable que personne n'a sans doute oublié."""
# text_fra = """Ce fantastique animal endossa la responsabilité de tous ces naufrages, dont le nombre est malheureusement considérable ; car sur trois mille navires dont la perte est annuellement relevée au Bureau-Veritas, le chiffre des navires à vapeur ou à voiles, supposés perdus corps et biens par suite d'absence de nouvelles, ne s'élève pas à moins de deux cents !"""
# text_fra = """Depuis ce moment, en effet, les sinistres maritimes qui n'avaient pas de cause déterminée furent mis sur le compte du monstre."""

en = spacy.load('en')
fr = spacy.load('fr')

ed = en(text_eng)
fd = fr(text_fra)

vocab_en = { tok.lemma_ for tok in ed if tok.is_alpha}
vocab_fr = { tok.lemma_ for tok in fd if tok.is_alpha}

align.init(fd, 'fra', ed, 'eng')

# map named entities
mapper.mapNamedEntities(confidence=0.5, sourceDoc=fd, targetDoc=ed)

# map numbers
mapper.mapNumbers(confidence=0.5)

# structural mapping with exact dictionary match
scores = [0.05, 0.01, 0.005]
for score in scores:
    mapper.mapBaseStructure(minScore=score)

# map in dependents
for score in scores:
    mapper.mapDependents(minScore=score)

# TODO map base structure using translation + glove

# map base strutcure if the word is not in the dictionary
mapper.mapBaseNoTranslate(minScore=0.3)

# map dependents again
for score in scores:
    mapper.mapDependents(minScore=score)

# map dependents again
for score in [0.5, 0.1]:
    mapper.mapTranslatables(minScore=score)

# map using word vectors
for score in [0.5, 0.4]:
    mapper.mapGlove(minScore=score)

# display source
print('SOURCE')
for m in align.MAPPING.source.tokens:
    print(m)

html_fra = spacy.displacy.render(fd, style='dep', options={'compact': True}, page=True)
html_eng = spacy.displacy.render(ed, style='dep', options={'compact': True}, page=True)

VISUAL = 'cache/visual'

os.makedirs(VISUAL, exist_ok=True)

with open(os.path.join(VISUAL, 'fra.html'), 'w') as f:
    f.write(html_fra)

with open(os.path.join(VISUAL, 'eng.html'), 'w') as f:
    f.write(html_eng)

