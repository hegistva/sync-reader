import pickle
import os
import atexit

from tr.libs import utils

CACHE = 'cache/lemma'

lemma_mappings = {}

default_db = None

TOTAL = 'TOTAL'

def addMapping(source_lemma, target_lemma, fromLang=None, toLang=None):
    """add a mapping for a lemma"""
    dbName = __useDB(fromLang, toLang)
    if not source_lemma in lemma_mappings[dbName]:
        lemma_mappings[dbName][source_lemma] = {}
    lm = lemma_mappings[dbName][source_lemma]
    lm[target_lemma] = lm.get(target_lemma, 0) + 1
    lm[TOTAL] = lm.get(TOTAL, 0) + 1

def printMapping(lemma=None, fromLang=None, toLang=None):
    dbName = __useDB(fromLang, toLang)
    header = ['source', 'target', 'count', 'prob']
    rows = []
    if lemma is None:
        for source_lemma, mappings in lemma_mappings[dbName].items():
            total = mappings[TOTAL]
            for target_lemma, cnt in mappings.items():
                if not target_lemma == TOTAL:
                    rows.append([source_lemma, target_lemma, cnt, cnt/total])
    else:        
        mappings = lemma_mappings[dbName][lemma]
        total = mappings[TOTAL]
        for target_lemma, cnt in mappings.items():
            if not target_lemma == TOTAL:
                rows.append([lemma, target_lemma, cnt, cnt/total])
    utils.displayTable(tbl=rows, header=header)

def setDefault(fromLang, toLang):
    global default_db
    default_db = __dbName(fromLang, toLang)
    load(fromLang, toLang)

def load(fromLang, toLang):
    dbName = __dbName(fromLang, toLang)
    if not dbName in lemma_mappings:
        try:
            lemma_mappings[dbName] = pickle.load(open(os.path.join(CACHE,dbName), 'rb'))
        except Exception:
            lemma_mappings[dbName] = {}

def reset(fromLang, toLang):
    dbName = __dbName(fromLang, toLang)
    lemma_mappings[dbName] = {}
    file_to_del = os.path.join(CACHE, dbName)
    try:
        os.remove(file_to_del)
        setDefault(fromLang, toLang)
    except Exception as e:
        print('ERROR: could not remove lemma cache under %s: %s' % (file_to_del, e))
        
def __useDB(fromLang, toLang):
    """Find out the database to be used"""
    if fromLang is None or toLang is None:
        if default_db is None:
            raise RuntimeError("Must provide languages or set the dafault language for mapping")
        else:
            return default_db
    else:
        return __dbName(fromLang, toLang)

def __dbName(fromLang, toLang):
    """Caculate the name for a mapping"""
    return "%s-%s" % (fromLang, toLang)

def __saveMapping():
    """Save in memory dictinary cache to disc"""
    for dbName, d in lemma_mappings.items():
        if not d is None:
            os.makedirs(CACHE, exist_ok=True)
            pickle.dump(d, open(os.path.join(CACHE, dbName), 'wb'))

atexit.register(__saveMapping)
