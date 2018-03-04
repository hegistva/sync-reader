
import zipfile
import numpy as np

GLOVE_ZIP_FILE = '/home/hegistva/HD/Programming/AI/glove.840B.300d.zip'

# words = ['computer', 'machine', 'cpu', 'gpu', 'tree', 'oak', 'beech', 'elm', 'hickory'] 

def getVector(words, path_to_glove=GLOVE_ZIP_FILE):
    embedding_weights = {}
    vocab_size = len(words)
    found_count = 0
    with zipfile.ZipFile(path_to_glove) as z:
        with z.open('glove.840B.300d.txt') as f:
            for line in f:
                vals = line.split()
                word = str(vals[0].decode('utf-8'))
                if word in words:
                    found_count += 1
                    coefs = np.asarray(vals[1:], dtype='float32')
                    coefs /= np.linalg.norm(coefs)
                    embedding_weights[word] = coefs
                if found_count == vocab_size:
                    break
    return embedding_weights

# vecs = getVector(words)
# for word1, vec1 in vecs.items():
#     for word2, vec2 in vecs.items():
#         print("%s, %s, len: %d, dot: %.4f" % (word1, word2, len(vec1), np.dot(vec1, vec2)))


