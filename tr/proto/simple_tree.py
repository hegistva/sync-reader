import sys, os, pprint, time
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app = QtWidgets.QApplication(sys.argv)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# init widgets
view = QtWidgets.QTreeView()

view.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
model =  QtGui.QStandardItemModel()
model.setHorizontalHeaderLabels(['col1', 'col2', 'col3'])
view.setModel(model)
view.setUniformRowHeights(True)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# populate data
for i in range(3):
    parent1 = QtGui.QStandardItem('Family {}. Some long status text for sp'.format(i))
    for j in range(3):
        child1 = QtGui.QStandardItem('Child {}'.format(i*3+j))
        child2 = QtGui.QStandardItem('row: {}, col: {}'.format(i, j+1))
        child3 = QtGui.QStandardItem('row: {}, col: {}'.format(i, j+2))
        parent1.appendRow([child1, child2, child3])
    model.appendRow(parent1)
    # span container columns
    view.setFirstColumnSpanned(i, view.rootIndex(), True)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# expand third container
index = model.indexFromItem(parent1)
view.expand(index)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# select last row
selmod = view.selectionModel()
index2 = model.indexFromItem(child3)
selmod.select(index2, QtCore.QItemSelectionModel.Select|QtCore.QItemSelectionModel.Rows)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
view.show()
sys.exit(app.exec_())