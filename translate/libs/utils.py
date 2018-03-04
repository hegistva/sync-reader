
import itertools

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