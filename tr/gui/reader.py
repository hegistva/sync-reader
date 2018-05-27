
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5 import Qt
from PyQt5.QtCore import Qt as CoreQt

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
        self.transChapter = None # translation of the current chapter
        self.ui.actionPlay.triggered.connect(lambda _: self.ui.player.play(self.selectedContent))
        self.ui.actionPause.triggered.connect(self.ui.player.pause)
        self.ui.actionDownload.triggered.connect(self.download)
        self.ui.actionSettings.triggered.connect(self.showSettings)
        self.ui.actionAdd.triggered.connect(self.showSearch)
        self.ui.actionZoomIn.triggered.connect(self.zoomIn)
        self.ui.actionZoomOut.triggered.connect(self.zoomOut)
        self.ui.actionNextChapter.triggered.connect(lambda _: self.playRelativeChapter(1))
        self.ui.actionPrevChapter.triggered.connect(lambda _: self.playRelativeChapter(-1))        
        self.ui.player.position_changed.connect(self.positionChanged)
        self.ui.player.length_changed.connect(self.lengthChanged)
        self.ui.player.token_changed.connect(self.tokenChanged)
        self.ui.player.bead_changed.connect(self.beadChanged)
        self.ui.player.chapter_ended.connect(self.chapterEnded)
        self.ui.downloadManager.completed.connect(self.downloadCompleted)
        self.ui.downloadManager.chapter_completed.connect(self.chapterDownloaded)
        self.ui.downloadManager.progress_changed.connect(self.downloadProgress)
        self.autoPlay = settings.Config.value(settings.Config.AUTO_PLAY)
        self.transLang = settings.Config.value(settings.Config.TRANS_LANG)
        self.ui.transLanguage.currentIndexChanged.connect(self.transLangChanged)
        book_nav.initNavigator(self.ui.bookList, self)
        

    def updateLibrary(self):
        """Update the library"""        
        book_nav.refresh()

    # TODO: Should be in the navigator widget, should be using signals
    def selectionChanged(self, selected, deselected):
        """Select  a node"""
        try:             
            idx = selected.first().indexes()[0]
            itm = self.ui.bookList.model().itemFromIndex(idx)
            m = itm.data()
            self.selectedContent = m
            self.ui.selectedContent.setText("Selected Content: %s" % m)
            if isinstance(self.selectedContent, model.ChapterInfo):
                self.playChapter(self.selectedContent)
        except Exception as e:
            pass
        
    def playChapter(self, chapter):
        self.currentChapter = chapter
        if self.currentChapter.downloaded:
            self.currentChapter.loadMappings()
            self.ui.player.play(self.currentChapter)
            with open(self.currentChapter.contentFile, 'r') as f:
                self.ui.readerWidget.readerPane.setText(f.read())
            # find translation and open if available
            self.transChapter = None
            tr = self.currentChapter.translation.book.getTranslation(self.transLang)
            if not tr is None:
                ch = tr.getChapter(self.currentChapter.idx)
                if not ch is None:
                    self.transChapter = ch
            if self.transChapter and self.transChapter.downloaded:
                self.transChapter.loadMappings()
                with open(self.transChapter.contentFile, 'r') as f:
                    self.ui.foreignReaderWidget.readerPane.setText(f.read())
                
    def playRelativeChapter(self, offset):
        if not self.currentChapter is None:
            # we have a current chapter, find the next one
            next_chapter = self.currentChapter.translation.relativeChapter(self.currentChapter, offset)
            # select it on the tree view triggering the play
            book_nav.SEL_MODEL.select(next_chapter.treeNode.index(), Qt.QItemSelectionModel.SelectCurrent)

    def chapterEnded(self):
        if self.autoPlay:
            # trigger playing the next chapter on autoplay
            self.ui.actionNextChapter.trigger()        

    def lengthChanged(self, new_length):
        self.ui.chapterSlider.setMaximum(new_length)

    def positionChanged(self, new_position):
        self.ui.chapterSlider.setValue(new_position)

    def tokenChanged(self, newToken):
        # highlight the token in the text
        self.ui.readerWidget.readerPane.highlightToken(newToken)
        
    def beadChanged(self, newBead):
        # highlight the bead in the text
        self.ui.readerWidget.readerPane.highlightBead(newBead)
        # highlight bead in the translated chapter
        if self.transChapter and self.transChapter.downloaded:
            tr_bead = self.transChapter.getBead(newBead.id)
            self.ui.foreignReaderWidget.readerPane.highlightBead(tr_bead)
            
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
        self.ui.readerWidget.readerPane.zoomIn(2)
        self.ui.foreignReaderWidget.readerPane.zoomIn(2)

    def zoomOut(self):
        self.ui.readerWidget.readerPane.zoomOut(2)
        self.ui.foreignReaderWidget.readerPane.zoomOut(2)

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
    
    def transLangChanged(self, newIdx):
        # the translation language setting has changed
        self.transLang = self.ui.transLanguage.model().item(newIdx).data(CoreQt.UserRole)
        if self.ui.transLanguage.currentIndex() != newIdx:
            self.ui.transLanguage.setCurrentIndex(newIdx)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = ReaderWidget()
    reader.show()
    sys.exit(app.exec_())
