
import itertools

def dependencyGraph(token):
    dep_list = [dependencyGraph(child) for child in token.children]
    dep_list = list(itertools.chain.from_iterable(dep_list))
    dep_list.append(token)
    return dep_list

def isRootNode(token):
    return token == token.head

def nodeDepth(token):
    if isRootNode(token):
        return 0
    else:
        return 1 + nodeDepth(token.head)


def hasMappedParent(doc, mt):
    """Find out if a token has a mapped parent"""
    if mt.isMapped or isRootNode(mt.token): 
        # if node is mapped or it is root return its status
        return mt.isMapped
    else:
        return hasMappedParent(doc, doc[mt.token.head.i])