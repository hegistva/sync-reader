import os
import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from tr.books import book_manager
from settings import Config

class SearchDialog(QtWidgets.QDialog):
    
    BOOK, AUTHOR, TITLE, LANGUAGES, CHAPTERS = range(5)

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
        self.searchButton.clicked.connect(self.searchBooks)
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
    
    def addSearchResult(self, row):
        row = [QtGui.QStandardItem(item) for item in row]
        row[0].setCheckable(True)
        row[0].setCheckState(Qt.Unchecked)
        self.model.appendRow(row)
        for idx, _ in enumerate(row):
            self.results.resizeColumnToContents(idx)
        
    def createResultModel(self, parent):
        model = QtGui.QStandardItemModel(0, 5, parent)
        model.setHeaderData(self.BOOK, Qt.Horizontal, "Book")
        model.setHeaderData(self.AUTHOR, Qt.Horizontal, "Author")
        model.setHeaderData(self.TITLE, Qt.Horizontal, "Title")
        model.setHeaderData(self.LANGUAGES, Qt.Horizontal, "Languages")
        model.setHeaderData(self.CHAPTERS, Qt.Horizontal, "Chapters")
        return model

    def searchBooks(self):
        rc = self.model.rowCount()
        if rc:
            self.model.removeRows(0, rc)
        keyword = self.searchTerm.text()
        if 3 <= len(keyword):
            results = book_manager.searchLibary(keyword)
            for result in results:
                self.addSearchResult(result.asList())

def showSearch(parent):
    dialog = SearchDialog(parent)
    result = dialog.exec_()
    if result == QtWidgets.QDialog.Accepted:
        for i in range(dialog.model.rowCount()):
            itm = dialog.model.item(i)
            if itm.checkState() == Qt.Checked:
                book_id = itm.text() # selected book identifier
                book_def = book_manager.getNetBook(book_id) # get the book configuration
                lpath = Config.value(Config.LIBRARY) # save location
                os.makedirs(lpath, exist_ok=True)
                fname = os.path.join(lpath, book_id + ".json")
                with open(fname, 'w') as f:
                    f.write(book_def)
                parent.updateLibrary()



            
