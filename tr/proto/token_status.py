
from nltk.translate.ibm5 import IBMModel5
from nltk.translate.api import AlignedSent
from terminaltables import AsciiTable
from tr.libs import utils
import spacy

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
# text_eng = """A Runaway Reef    THE YEAR 1866 was marked by a bizarre development, an unexplained and downright inexplicable phenomenon that surely no one has forgotten."""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
# text_fra = """UN ÉCUEIL FUYANT  L'année 1866 fut marquée par un événement bizarre, un phénomène inexpliqué et inexplicable que personne n'a sans doute oublié."""

en = spacy.load('en')
fr = spacy.load('fr')

ed = en(text_eng)
fd = fr(text_fra)

def printTokens(doc):
    tbldata = [[token.text, token.pos_, len(list(token.children)), token.head.text, utils.nodeDepth(token)] for token in doc]
    utils.displayTable(tbldata, ['Text', 'Part of Sentence', 'ChildCount', 'Head', 'Depth'])
    
printTokens(fd)
printTokens(ed)

