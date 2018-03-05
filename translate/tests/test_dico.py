
from translate.libs import dico
import spacy


def testFrenchSentence():
    
    fr = spacy.load('fr')

    text = """Tel était ce dernier fait, qui eut pour résultat de passionner à nouveau l'opinion publique."""

    dico.setDefault('fra', 'eng')

    doc = fr(text)

    for sent in doc.sents:
        print("Sentence: %s" % sent.text)
        for word in sent:
            if word.is_alpha:
                lemma = word.lemma_.lower()
                tr = dico.translateLemma(lemma)
                print("word %s: lemma: %s traslation: %s" % (word.text, lemma, tr))

testFrenchSentence()
# dico.printDict()
        
