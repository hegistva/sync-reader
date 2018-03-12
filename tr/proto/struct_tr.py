import os
import spacy
from tr.libs import align
from tr.libs import sentence_mapper
from tr.libs import lemma_mapper

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
text_eng = """A Runaway Reef    THE YEAR 1866 was marked by a bizarre development, an unexplained and downright inexplicable phenomenon that surely no one has forgotten."""
text_eng = """This outrageous animal had to shoulder responsibility for all derelict vessels, whose numbers are unfortunately considerable, since out of those 3,000 ships whose losses are recorded annually at themarine insurance bureau, the figure for steam or sailing ships supposedly lost with all hands, in the absence of any news, amounts to at least 200!"""
# text_eng = """Indeed, from this moment on, any maritime casualty without an established cause was charged to the monster's account."""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
text_fra = """UN ÉCUEIL FUYANT  L'année 1866 fut marquée par un événement bizarre, un phénomène inexpliqué et inexplicable que personne n'a sans doute oublié."""
text_fra = """Ce fantastique animal endossa la responsabilité de tous ces naufrages, dont le nombre est malheureusement considérable ; car sur trois mille navires dont la perte est annuellement relevée au Bureau-Veritas, le chiffre des navires à vapeur ou à voiles, supposés perdus corps et biens par suite d'absence de nouvelles, ne s'élève pas à moins de deux cents !"""
# text_fra = """Depuis ce moment, en effet, les sinistres maritimes qui n'avaient pas de cause déterminée furent mis sur le compte du monstre."""

# map using word vectors
sentence_mapper.mapSentence('fra', 'eng', text_fra, text_eng, doMapping=True, debug=True)

