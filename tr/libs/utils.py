
import itertools
from terminaltables import AsciiTable
import copy
import spacy

class Lang:
    ENG = 'eng'
    FRA = 'fra'

SPACY_LANG = {Lang.ENG: 'en', Lang.FRA: 'fr'}

SPACY_MODELS = {}

def getSpacy(lang):
    ret = SPACY_MODELS.get(lang, None)
    if ret is None:
        ret = spacy.load(SPACY_LANG[lang])
        SPACY_MODELS[lang] = ret
    return ret
    
def dependencyGraph(mt):
    dep_list = [dependencyGraph(child) for child in mt.children]
    dep_list = list(itertools.chain.from_iterable(dep_list))
    dep_list.append(mt)
    return dep_list

def isRootNode(mt):
    return mt == mt.head

def nodeDepth(mt):
    if isRootNode(mt):
        return 0
    else:
        return 1 + nodeDepth(mt.head)

def hasMappedParent(mt):
    """Find out if a token has a mapped parent"""
    if mt.isMapped or isRootNode(mt): 
        # if node is mapped or it is root return its status
        return mt.isMapped
    else:
        return hasMappedParent(mt.head)

def displayTable(tbl, header=None):
    tblcopy = copy.copy(tbl)
    if not header is None:
        tblcopy.insert(0, header)
    print(AsciiTable(tblcopy).table)
