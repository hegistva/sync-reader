
import colored
import functools
import itertools

from tr.libs.trans import utils
from tr.libs.trans import glove
from tr.libs.trans import dico
from tr.libs.trans import lemma_mapper

blue = functools.partial(colored.stylize, styles=colored.fore.BLUE)
green = functools.partial(colored.stylize, styles=colored.fore.GREEN)
red = functools.partial(colored.stylize, styles=colored.fore.RED)
yellow = functools.partial(colored.stylize, styles=colored.fore.YELLOW)
orange = functools.partial(colored.stylize, styles=colored.fore.DARK_ORANGE)
white = functools.partial(colored.stylize, styles=colored.fore.WHITE)

def colorForConf(confidence):        
    if confidence < 0.33:
        return orange
    elif confidence < 0.66:
        return yellow
    return green


# Classes to support mapping
class MapTarget(object):
    def __init__(self, idxTarget, method, confidence, source=False):
        self.target = MAPPING.source.tokens[idxTarget] if source else MAPPING.target.tokens[idxTarget]
        self.method = method
        self.confidence = confidence
    def __str__(self):
        colorFn = colorForConf(self.confidence)
        return "%s [%s] at %d with method %s, confidence %.2f" % (colorFn(self.target.token.text), colorFn(self.target.token.lemma_), self.target.token.i, self.method, self.confidence)
        
class MappedToken(object):

    def __init__(self, token, documentSize, source):
        self.source = source # source or target token
        self.documentSize = documentSize # document size
        self.relativePosition = token.i / documentSize # relative position in the document/sentence                
        self.graphSize = 0.0 # size of the subgraph starting on this node
        self.token = token # token
        self.alternatives = [] # mapping alternatives (list of MapTarget objects)
        self.isMapped = False # has the map target been selected yet
        self.mapTarget = None # map target (MapTarget object)
        self.mapping = None # reference mapping object
        self.head = None # list parent node
        self.children = [] # list of children
        self.dependents = []  # list of dependent tokens
        self.vector = None # word embedding vector
        self.translations = set() # dico translations
        self.translateVectors = {} # glove vectors for translations
        if self.source and token.is_alpha:
            self.translations = set(dico.translateToken(token))

    def mapTranslateVectors(self, gloveDict):
        self.translateVectors = {}
        for tr in self.translations:
            vec = gloveDict[tr]
            if not vec is None:
                self.translateVectors[tr]=vec
        
    def buildGraph(self, mapping):
        self.mapping = mapping
        self.head = self.mapping[self.token.head.i]
        for child in self.token.children:
            self.children.append(self.mapping[child.i])
        self.dependents = utils.dependencyGraph(self)
        self.graphSize = len(self.dependents) / self.documentSize
        
    def mapTo(self, mt):
        self.isMapped = True
        self.mapTarget = mt
        if self.source:
            if self.token.lemma_ and mt.target.token.lemma_:
                lemma_mapper.addMapping(self.token.lemma_.lower(), mt.target.token.lemma_.lower())            
            MAPPING.target.tokens[mt.target.token.i].mapTo(MapTarget(self.token.i, mt.method, mt.confidence, source=True)) # establish opposite mapping

    def __str__(self):
        colorFn = blue
        if not self.isMapped:
            colorFn = red
        else:
            colorFn = colorForConf(self.mapTarget.confidence)
        return "%s [%s] at %d (%.2f) - size: %.2f - depth: %d is mapped to %s, has mapped parent: %s" % (colorFn(self.token.text), colorFn(self.token.lemma_), self.token.i, self.relativePosition, self.graphSize, utils.nodeDepth(self), self.mapTarget, utils.hasMappedParent(self))

class Mapping(object):
    """"Mapping a langage"""
    def __init__(self, doc, language, source):
        self.langage = language
        self.source = source
        doc_size = len(doc)
        self.tokens = [MappedToken(tkn, doc_size, source) for tkn in doc]
        for mt in self.tokens:
            mt.buildGraph(self.tokens)
        if self.langage == utils.Lang.ENG:
            words = { mt.token.lemma_.lower() for mt in self.tokens if mt.token.is_alpha }
            vecs = glove.getVector(words)
            for mt in self.tokens:
                if mt.token.is_alpha:
                    mt.vector = vecs[mt.token.lemma_.lower()]
        if source:
            trs = [mt.translations for mt in self.tokens] # all translations
            tr_vocab = set(itertools.chain(*trs)) # raze
            tr_vecs = glove.getVector(tr_vocab)
            for mt in self.tokens:
                mt.mapTranslateVectors(tr_vecs)

class Alignment(object):
    def __init__(self, doc_source, lang_source, doc_target, lang_target):
        self.source = Mapping(doc_source, lang_source, source=True)
        self.target = Mapping(doc_target, lang_target, source=False)

# Global mapping object
MAPPING = None

def init(doc_source, lang_source, doc_target, lang_target):
    dico.setDefault(lang_source, lang_target)
    lemma_mapper.setDefault(lang_source, lang_target)
    global MAPPING
    MAPPING = Alignment(doc_source, lang_source, doc_target, lang_target)



