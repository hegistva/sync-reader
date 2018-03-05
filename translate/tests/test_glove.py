
from translate.libs import glove
import numpy as np

words = {'computer', 'machine', 'cpu', 'gpu', 'tree', 'oak', 'beech', 'elm', 'hickory'}

vecs = glove.getVector(words)

for word1, vec1 in vecs.items():
    for word2, vec2 in vecs.items():
        print("%s, %s, len: %d, dot: %.4f" % (word1, word2, len(vec1), np.dot(vec1, vec2)))


