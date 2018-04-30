
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from reader_rc import Ui_MainWindow
import settings
import search
import book_nav
import model
import res

class ReaderWidget(QMainWindow):
    
    def __init__(self, parent=None):
        super(ReaderWidget, self).__init__(parent)

        self.auidoMap = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)        
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionStop.triggered.connect(self.ui.player.stop)
        self.selectedContent = None # selected book/translation/chapter
        self.currentChapter = None # currently playing chapter
        self.ui.actionPlay.triggered.connect(lambda _: self.ui.player.play(self.selectedContent))
        self.ui.actionPause.triggered.connect(self.ui.player.pause)
        self.ui.actionDownload.triggered.connect(self.download)
        self.ui.actionSettings.triggered.connect(self.showSettings)
        self.ui.actionAdd.triggered.connect(self.showSearch)
        self.ui.actionZoomIn.triggered.connect(self.zoomIn)
        self.ui.actionZoomOut.triggered.connect(self.zoomOut)
        self.ui.player.position_changed.connect(self.positionChanged)
        self.ui.player.length_changed.connect(self.lengthChanged)
        self.ui.player.token_changed.connect(self.tokenChanged)
        self.ui.downloadManager.completed.connect(self.downloadCompleted)
        self.ui.downloadManager.chapter_completed.connect(self.chapterDownloaded)
        self.ui.downloadManager.progress_changed.connect(self.downloadProgress)
        book_nav.initNavigator(self.ui.bookList, self)
        

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
            self.currentChapter = self.selectedContent
            if self.currentChapter.downloaded:
                self.ui.player.play(self.currentChapter)
                with open(self.currentChapter.contentFile, 'r') as f:
                    self.ui.readerPane.setText(f.read())
                self.currentChapter.loadMappings()

    def lengthChanged(self, new_length):
        self.ui.chapterSlider.setMaximum(new_length)

    def positionChanged(self, new_position):
        self.ui.chapterSlider.setValue(new_position)

    def tokenChanged(self, newToken):
        # highlight the token in the text
        self.ui.readerPane.highlight(newToken.text_start, newToken.text_end)
        self.ui.readerPane.ensureCursorVisible()
        
    def download(self):
        """Download selected content"""
        self.ui.downloadManager.downloadContent(self.selectedContent)

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

    def downloadCompleted(self):
        # if download is complete reset and hide the GUI elements
        self.ui.downloadProgress.setValue(0)
        self.ui.downloadProgress.hide()
        self.ui.lblDownload.setText('Downloads')
        self.ui.lblDownload.hide()

    def downloadProgress(self, sum_speed, percent_complete):
        # download is in progress
        if not self.ui.downloadProgress.isVisible():
            #  show progress bar
            self.ui.downloadProgress.show()
            self.ui.lblDownload.show()
        # set progress message and progress
        self.ui.downloadProgress.setValue(percent_complete)

    def chapterDownloaded(self, chapter):
        # a chapter download, update the view
        if chapter.treeNode:
            if chapter.downloaded:
                chapter.treeNode.setIcon(res.play_icon)
            else:
                chapter.treeNode.setIcon(res.dl_icon)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = ReaderWidget()
    reader.show()
    sys.exit(app.exec_())
