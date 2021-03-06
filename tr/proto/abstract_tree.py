
# https://www.hardcoded.net/articles/using_qtreeview_with_qabstractitemmodel

from PyQt5 import Qt

class TreeNode(object):
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def __getChildren(self):
        raise NotImplementedError()

class TreeModel(Qt.QAbstractItemModel):
    def __init__(self):
        QAbstractItemModel.__init__(self):
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        raise NotImplementedError()

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.subnodes[row])
    
    def parent(self, index):
        if not index.isValid():
            return Qt.QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return Qt.QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        Qt.QAbstractItemModel.reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        return len(node.subnodes)

class NamedElement(object):
    def __init__(self, name, subelements):
        self.name = name
        self.subelements = subelements

class NameNode(TreeNode):
    def __init__(self, ref, parent, row):
        self.ref = ref
        TreeNode.__init__(self, parent, row)

class NamesModel(TreeModel):
    def __init__(self, rootElements):
        self.rootElements = rootElements
        TreeModel.__init__(self)

    def _getRootNodes(self):
        return [NamedNode(elem, None, index)
            for index, elem in enumerate(self.rootElements)]

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole and index.column() == 0:
            return node.ref.name
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole \
            and section == 0:
            return 'Name'
        return None
