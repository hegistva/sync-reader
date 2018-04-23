
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import QTimer
from reader_rc import Ui_MainWindow
import settings
import search
import book_nav
import model
import dl_manager

class ReaderWidget(QMainWindow):
    
    def __init__(self, parent=None):
        super(ReaderWidget, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionPlay.triggered.connect(self.play)
        self.ui.actionDownload.triggered.connect(self.download)
        self.ui.actionSettings.triggered.connect(self.showSettings)
        self.ui.actionAdd.triggered.connect(self.showSearch)
        self.selectedContent = None # selected book/translation/chapter
        self.downloadManager = dl_manager.DownloadManager(self, self.ui.downloadProgress, self.ui.lblDownload) # download manager
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGUI)
        self.timer.start(100)
        book_nav.initNavigator(self.ui.bookList, self)

    def stop(self):
        self.ui.chapterProgress.hide()

    def updateGUI(self):
        self.downloadManager.update() # update the download status

    def updateLibrary(self):
        book_nav.refresh()

    def play(self):
        sender = self.sender()
        print("Playing chaper: %s" % sender.property('model'))
        self.ui.chapterProgress.show()

    def select(self, idx):        
        itm = self.ui.bookList.model().itemFromIndex(idx)
        m = itm.data()
        self.selectedContent = m
        self.ui.selectedContent.setText("Selected Content: %s" % m)

    def download(self):
        if isinstance(self.selectedContent, model.ChapterInfo):
            self.downloadManager.downloadChapter(self.selectedContent)

    def showSettings(self):
        settings.showSettings(self)

    def showSearch(self):
        search.showSearch(self)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = ReaderWidget()
    reader.show()
    sys.exit(app.exec_())
