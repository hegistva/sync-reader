
import dicoclient
import re
import spacy

fr = spacy.load('fr')

text = """Tel était ce dernier fait, qui eut pour résultat de passionner à nouveau l'opinion publique."""

dc = dicoclient.DicoClient()
dc.open('localhost')
DATABASE = 'fd-fra-eng'

doc = fr(text)

def translateLemma(lemma):
    foreign_defs = dc.define(DATABASE, lemma)
    if foreign_defs.get('error', None) == '552': # NOT FOUND
        frmatches = dc.match(DATABASE, 'lev', lemma)
        print("ALTERNATIVES %s: %s" % (lemma, frmatches))
    else:
        for d in foreign_defs['definitions']:
            words = d['desc'].splitlines()[-1].split(';')
            words = [word.strip() for word in words]
            print(words)

    

for sent in doc.sents:
    print("Sentence: %s" % sent.text)
    for word in sent:
        if word.is_alpha:
            lemma = word.lemma_.lower()
            print("word %s: lemma: %s" % (word.text.lower(), lemma))
            translateLemma(lemma)


        
        
