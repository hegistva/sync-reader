
import spacy

eng = spacy.load('en_core_web_md')

doc = eng(u'dog cat banana')

for t1 in doc:
    for t2 in doc:
        print("%s -> %s: %.2f" % (t1.text, t2.text, t1.similarity(t2)))

fra = spacy.load('fr_core_news_md')
doc = fra(u'chien chat fraise')

for t1 in doc:
    for t2 in doc:
        print("%s -> %s: %.2f" % (t1.text, t2.text, t1.similarity(t2)))
