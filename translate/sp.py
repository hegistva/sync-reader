
import spacy
import numpy

nlp = spacy.load('fr')


raw_text=r"A prendre la moyenne des observations faites à diverses reprises -- en rejetant les évaluations timides qui assignaient à cet objet une longueur de deux cents pieds et en repoussant les opinions exagérées qui le disaient large d'un mille et long de trois -- on pouvait affirmer, cependant, que cet être phénoménal dépassait de beaucoup toutes les dimensions admises jusqu'à ce jour par les ichtyologistes -- s'il existait toutefois."

doc = nlp(raw_text)
for tok in doc:
    print(tok.text)