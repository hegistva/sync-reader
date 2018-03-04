
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
    def __init__(self, target, confidence):
        self.target = target
        self.confidence = confidence
    def __str__(self):
        colorFn = colorForConf(self.confidence)
        return "%s [%s] at %d with confidence %.2f" % (colorFn(self.target.text), colorFn(self.target.lemma_), self.target.i, self.confidence)
        
class MappedToken(object):

    def __init__(self, token, source, relativePosition, graphSize):
        self.source = source # source or target token
        self.relativePosition = relativePosition # relative position in the document/sentence
        self.graphSize = graphSize # size of the subgraph starting on this node
        self.token = token # token
        self.alternatives = [] # mapping alternatives (list of MapTarget objects)
        self.isMapped = False # has the map target been selected yet
        self.mapped = None # map target (MapTarget object)
        
    
    def mapTo(self, mt, map_back=True):
        self.isMapped = True
        self.mapped = mt
        if map_back:
            if self.source:
                Alignment.t2s[mt.target.i].mapTo(MapTarget(self.token, mt.confidence), map_back=False)
            else:
                Alignment.s2t[mt.target.i].mapTo(MapTarget(self.token, mt.confidence), map_back=False)

    def __str__(self):
        colorFn = blue
        if not self.isMapped:
            colorFn = red
        else:
            colorFn = colorForConf(self.mapped.confidence)
        return "%s [%s] at %d (%.2f) - size: %.2f is mapped to %s" % (colorFn(self.token.text), colorFn(self.token.lemma_), self.token.i, self.relativePosition, self.graphSize, self.mapped)

class Alignment(object):
    s2t = []
    t2s = []

def initMapping(doc, source):
    l = len(doc)
    return [MappedToken(tkn, source, tkn.i / l, utils.graphSize(tkn) / l) for tkn in doc]

def initAlignment(doc_source, doc_target):
    Alignment.s2t = initMapping(doc_source, source=True)
    Alignment.t2s = initMapping(doc_target, source=False)