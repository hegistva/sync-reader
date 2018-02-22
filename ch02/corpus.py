
import nltk
from nltk.corpus import brown as cb
from nltk.corpus import gutenberg as cg

nltk.data.path.append('/home/hegistva/HD/Programming/Python/nltk_data')

print(dir(cb))

print(cb.categories())

print(cb.fileids())

print(cb.words()[0:20])

print(cb.words(categories='news')[10:30])