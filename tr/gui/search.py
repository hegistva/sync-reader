import os
import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class SearchDialog(QtWidgets.QDialog):
    
    BOOK, TITLE, LANGUAGES, CHAPTERS = range(4)

    def __init__(self, parent=None):
        super(SearchDialog, self).__init__(parent)
        minWidth = parent.width() * 0.8 if not parent is None else 600
        self.setMinimumWidth(minWidth)
        mainLayout = QtWidgets.QVBoxLayout(self)
        searchLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(searchLayout)
        self.searchTerm = QtWidgets.QLineEdit()
        searchLayout.addWidget(self.searchTerm)
        
        self.searchButton = QtWidgets.QPushButton('Search')
        self.searchButton.clicked.connect(lambda _: self.addSearchResult("Bookid", "Booktitle", "ENG,FRA", "21"))
        searchLayout.addWidget(self.searchButton)
        
        self.results = QtWidgets.QTreeView()
        self.results.setRootIsDecorated(False)
        self.results.setAlternatingRowColors(True)

        self.model = self.createResultModel(self)
        self.results.setModel(self.model)
        
        mainLayout.addWidget(self.results)

        self.setWindowTitle('Find Books')

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Add Selected")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        mainLayout.addWidget(buttons)
    
    def addSearchResult(self, *args):
        row = [QtGui.QStandardItem(item) for item in args]
        row[0].setCheckable(True)
        row[0].setCheckState(Qt.Unchecked)
        self.model.appendRow(row)
        self.results.resizeColumnToContents(0)
        
    def createResultModel(self, parent):
        model = QtGui.QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.BOOK, Qt.Horizontal, "Book")
        model.setHeaderData(self.TITLE, Qt.Horizontal, "Title")
        model.setHeaderData(self.LANGUAGES, Qt.Horizontal, "Languages")
        model.setHeaderData(self.CHAPTERS, Qt.Horizontal, "Chapters")
        return model

        
def showSearch(parent):
    dialog = SearchDialog(parent)
    result = dialog.exec_()
    if result == QtWidgets.QDialog.Accepted:
        print('Book has been selected for import')



            
