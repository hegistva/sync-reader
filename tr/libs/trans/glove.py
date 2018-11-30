
import zipfile
import pickle
import os
import atexit

from tr.libs.utils import config

import numpy as np

GLOVE_PATH = '/home/hegistva/programming/python/AI'
GLOVE_TXT_FILE = 'glove.6B.100d.txt'

CACHE = os.path.join(config.ROOT, 'cache/glove')

__glove_dict = None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def load():
    global __glove_dict
    try:
        __glove_dict = pickle.load(open(os.path.join(CACHE, 'words'), 'rb'))
    except Exception as e:        
        print('WARNING: failed to load glove cache: %s' % e) # print warning               
        __glove_dict = {}
    

def __save():
    """Save in memory dictinary cache to disc"""
    if not __glove_dict is None:
        os.makedirs(CACHE, exist_ok=True)
        pickle.dump(__glove_dict, open(os.path.join(CACHE, 'words'), 'wb'))

atexit.register(__save)

def getVector(words):
    """get glove vector for a list of words"""
    if __glove_dict is None:
        load() # load cache if needed
    in_cache = words.intersection(__glove_dict.keys())
    from_cache = { k:v for k, v in __glove_dict.items() if k in in_cache } # items available in cache
    not_in_cache = words.difference(__glove_dict.keys())
    new_word_vecs = __getVectorFromGloveTxtFile(not_in_cache)
    __glove_dict.update(new_word_vecs) # update cache
    from_cache.update(new_word_vecs) 
    return from_cache
    
def __getVectorFromGloveTxtFile(words, path_to_glove=GLOVE_PATH, txt_file=GLOVE_TXT_FILE):
    embedding_weights = {}
    vocab_size = len(words)
    found_count = 0
    txt_path = os.path.join(path_to_glove, txt_file)
    with open(txt_path, 'r') as f:
        for line in f:
            vals = line.split()
            word = vals[0]
            if word in words:
                if is_number(vals[1]):
                    found_count += 1
                    coefs = np.asarray(vals[1:], dtype='float32')
                    coefs /= np.linalg.norm(coefs)
                    embedding_weights[word] = coefs
            if found_count == vocab_size:
                return embedding_weights
    # add words we have not found so we do not search for them forever
    not_found = words.difference(embedding_weights.keys())
    for nfw in not_found:
        embedding_weights[nfw] = None
    return embedding_weights

def printCache():
    if __glove_dict is None:
        load()
    for word, vec in __glove_dict.items():
        print(word, vec)
