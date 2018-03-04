
def graphSize(token):
    size = 0
    for child in token.children:
        size += 1
        size += graphSize(child)
    return size