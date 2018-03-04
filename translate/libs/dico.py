
import dicoclient
import pickle
import os
import atexit
import itertools

dc = dicoclient.DicoClient()
dc.open('localhost')

CACHE = 'cache/dictionaries'

trans_dicts = {}

default_db = None

def translateToken(token, fromLang=None, toLang=None):
    tr = translateLemma(token.text.lower())
    if not tr:
        tr = translateLemma(token.lemma_.lower())
    return tr

def translateLemma(lemma, fromLang=None, toLang=None):
    """public function to translate a lemma"""
    dbName = __useDB(fromLang, toLang)
    if lemma in trans_dicts[dbName]:
        return trans_dicts[dbName][lemma]
    else:
        v = __translateLemma(lemma, dbName)
        trans_dicts[dbName][lemma] = v
        return v

def printDict(fromLang = None, toLang = None):
    dbName = __useDB(fromLang, toLang)
    print(trans_dicts[dbName])

def setDefault(fromLang, toLang):
    global default_db
    default_db = __dbName(fromLang, toLang)
    load(fromLang, toLang)

def load(fromLang, toLang):
    dbName = __dbName(fromLang, toLang)
    if not dbName in trans_dicts:
        try:
            trans_dicts[dbName] = pickle.load(open(os.path.join(CACHE,dbName), 'rb'))
        except Exception:
            trans_dicts[dbName] = {}

def __useDB(fromLang, toLang):
    """Find out the database to be used"""
    if fromLang is None or toLang is None:
        if default_db is None:
            raise RuntimeError("Must provide languages or set the dafault language for translation!")
        else:
            return default_db
    else:
        return __dbName(fromLang, toLang)

def __dbName(fromLang, toLang):
    """Caculate the name for a dictionary"""
    return "fd-%s-%s" % (fromLang, toLang)

def __saveDicts():
    """Save in memory dictinary cache to disc"""
    global trans_dicts
    for dbName, d in trans_dicts.items():
        os.makedirs(CACHE, exist_ok=True)
        pickle.dump(d, open(os.path.join(CACHE, dbName), 'wb'))

atexit.register(__saveDicts)

def __translateLemma(lemma, dbName):
    """Internal function to"""
    foreign_defs = dc.define(dbName, lemma)
    if foreign_defs.get('error', None) == '552': # NOT FOUND
        frmatches = dc.match(dbName, 'lev', lemma)
        if frmatches.get('error', None) == '552':
            return []
        else:
            matches = frmatches.get('matches', None)
            if matches:
                alternatives = matches.get(dbName, [])
                trs = [__translateLemma(alt, dbName) for alt in alternatives] # translations                    
                return list(itertools.chain.from_iterable(trs))
            else:
                return []
    else:
        for d in foreign_defs['definitions']:
            words = d['desc'].splitlines()[-1].split(';')
            words = [word.split('.')[-1].strip() for word in words]
            return words


        
        
