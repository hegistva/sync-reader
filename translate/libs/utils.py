
import itertools

def dependencyGraph(token):
    dep_list = [dependencyGraph(child) for child in token.children]
    dep_list = list(itertools.chain.from_iterable(dep_list))
    dep_list.append(token)
    return dep_list
