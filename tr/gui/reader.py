
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from reader_rc import Ui_MainWindow
import settings
import search
import book_nav
import dl_manager
import player
import model

class ReaderWidget(QMainWindow):
    
    def __init__(self, parent=None):
        super(ReaderWidget, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.player = player.Player(self.ui.chapterSlider, self.ui.volumeSlider)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionStop.triggered.connect(self.player.stop)
        self.selectedContent = None # selected book/translation/chapter
        self.ui.actionPlay.triggered.connect(lambda _: self.player.play(self.selectedContent))
        self.ui.actionPause.triggered.connect(self.player.pause)
        self.ui.actionDownload.triggered.connect(self.download)
        self.ui.actionSettings.triggered.connect(self.showSettings)
        self.ui.actionAdd.triggered.connect(self.showSearch)
        self.ui.actionZoomIn.triggered.connect(self.zoomIn)
        self.ui.actionZoomOut.triggered.connect(self.zoomOut)
        self.downloadManager = dl_manager.DownloadManager(self, self.ui.downloadProgress, self.ui.lblDownload) # download manager        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGUI)
        self.timer.start(100)
        book_nav.initNavigator(self.ui.bookList, self)

    def updateGUI(self):
        """GUI update function"""
        self.downloadManager.update() # update the download status
        self.player.update()        

    def updateLibrary(self):
        """Update the library"""        
        book_nav.refresh()

    # TODO: Should be in the navigator widget, should be using signals
    def select(self, idx):
        """Select  a node"""
        itm = self.ui.bookList.model().itemFromIndex(idx)
        m = itm.data()
        self.selectedContent = m
        self.ui.selectedContent.setText("Selected Content: %s" % m)        
        if isinstance(self.selectedContent, model.ChapterInfo):
            if self.selectedContent.downloaded:
                self.player.play(self.selectedContent)
                with open(self.selectedContent.contentFile, 'r') as f:
                    self.ui.readerPane.setText(f.read())
                    
                    
    def download(self):
        """Download selected content"""
        self.downloadManager.downloadContent(self.selectedContent)

    def showSettings(self):
        """Show Settings Dialog"""
        settings.showSettings(self)

    def showSearch(self):
        """Show Search Dialog"""
        search.showSearch(self)

    def zoomIn(self):
        self.ui.readerPane.zoomIn(2)

    def zoomOut(self):
        self.ui.readerPane.zoomOut(2)
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = ReaderWidget()
    reader.show()
    sys.exit(app.exec_())
