
import colored
import functools

from translate.libs import utils

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
        self.target = Alignment.s2t[idxTarget] if source else Alignment.t2s[idxTarget]
        self.method = method
        self.confidence = confidence
    def __str__(self):
        colorFn = colorForConf(self.confidence)
        return "%s [%s] at %d with method %s, confidence %.2f" % (colorFn(self.target.token.text), colorFn(self.target.token.lemma_), self.target.token.i, self.method, self.confidence)
        
class MappedToken(object):

    def __init__(self, token, documentSize, source):
        self.source = source # source or target token
        self.relativePosition = token.i / documentSize # relative position in the document/sentence
        self.dependents = utils.dependencyGraph(token) # list of dependent tokens
        self.graphSize = len(self.dependents) / documentSize # size of the subgraph starting on this node
        self.token = token # token
        self.alternatives = [] # mapping alternatives (list of MapTarget objects)
        self.isMapped = False # has the map target been selected yet
        self.mapTarget = None # map target (MapTarget object)
        
    
    def mapTo(self, mt):
        self.isMapped = True
        self.mapTarget = mt
        if self.source:
            Alignment.t2s[mt.target.token.i].mapTo(MapTarget(self.token.i, mt.method, mt.confidence, source=True)) # establish opposite mapping

    def __str__(self):
        colorFn = blue
        if not self.isMapped:
            colorFn = red
        else:
            colorFn = colorForConf(self.mapTarget.confidence)
        return "%s [%s] at %d (%.2f) - size: %.2f is mapped to %s" % (colorFn(self.token.text), colorFn(self.token.lemma_), self.token.i, self.relativePosition, self.graphSize, self.mapTarget)

class Alignment(object):
    s2t = []
    t2s = []

def initMapping(doc, source):
    doc_size = len(doc)
    return [MappedToken(tkn, doc_size, source) for tkn in doc]

def initAlignment(doc_source, doc_target):
    Alignment.s2t = initMapping(doc_source, source=True)
    Alignment.t2s = initMapping(doc_target, source=False)