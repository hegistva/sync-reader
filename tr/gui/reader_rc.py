# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reader.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor

import os

import player
import dl_manager
from res import ICONS
from settings import Config, LANGUAGES

class ReaderWidget(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super(ReaderWidget, self).__init__(parent)
            self._autoScroll = Config.value(Config.AUTO_SCROLL)
            self.readerPane = ReaderPane(parent=parent, autoScroll=self._autoScroll)
            self.readerPane.setReadOnly(True)        
            readerPaneLayout = QtWidgets.QVBoxLayout()
            readerPaneLayout.addWidget(self.readerPane)
            self.setLayout(readerPaneLayout)

        @property
        def autoScroll(self):
            return self.readerPane.autoScroll

        @autoScroll.setter
        def autoScroll(self, value):
            self.readerPane.autoScroll = value
        
class ReaderPane(QtWidgets.QTextEdit):
    def __init__(self, parent=None, autoScroll=True):
        self.autoScroll = autoScroll
        super(ReaderPane, self).__init__(parent)
        # format for highlighting token
        self.tokenFmt = QtGui.QTextCharFormat()
        self.tokenFmt.setForeground(QtCore.Qt.darkRed)
        self.tokenFmt.setFontUnderline(True)
        self.tokenFmt.setUnderlineColor(QtCore.Qt.darkGreen)
        self.tokenFmt.setUnderlineStyle(QtGui.QTextCharFormat.WaveUnderline)
        # self.tokenFmt.setFontWeight(QtGui.QFont.Bold)
        # format for highlighting token
        self.beadFmt = QtGui.QTextCharFormat()
        self.beadFmt.setForeground(QtCore.Qt.darkBlue)
        self.beadFmt.setFontUnderline(False)
        # self.beadFmt.setFontWeight(QtGui.QFont.Normal)
        # default format with no special settings
        self.regularFmt = QtGui.QTextCharFormat()
        self.regularFmt.setForeground(self.textColor())
        self.regularFmt.setFontUnderline(False)
        # self.regularFmt.setFontWeight(QtGui.QFont.Normal)
        # cursors
        self.tokenCursor = self.textCursor()
        self.beadCursor = self.textCursor()
        self.visibleCursor = self.textCursor()
        self.length = 0
        self.bead = None
        
    def setText(self, text):
        self.length = len(text)
        return super(ReaderPane, self).setText(text)
    
    def highlightBead(self, bead):
        self.bead = bead
        start_pos = bead.text_start + bead.offset
        end_pos = bead.text_end + bead.offset
        self.beadCursor.setPosition(0, QTextCursor.MoveAnchor)
        self.beadCursor.setPosition(self.length, QTextCursor.KeepAnchor)
        self.beadCursor.mergeCharFormat(self.regularFmt) # make sure the current selection is normal
        self.beadCursor.setPosition(start_pos, QTextCursor.MoveAnchor)
        self.beadCursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        self.beadCursor.mergeCharFormat(self.beadFmt)
        if self.autoScroll:
            self.visibleCursor.setPosition(min(end_pos + 200, self.length), QTextCursor.MoveAnchor) # for the autoscroll
            self.setTextCursor(self.visibleCursor)

    def highlightToken(self, token):
        fmt = self.beadFmt if (self.tokenCursor.selectionStart() <= self.beadCursor.selectionEnd()) and self.tokenCursor.selectionEnd() >= self.beadCursor.selectionStart() else self.regularFmt
        self.tokenCursor.mergeCharFormat(fmt) # make sure the current selection is normal
        start_pos = token.text_start
        end_pos = token.text_end
        if not self.bead is None:
            start_pos += self.bead.offset
            end_pos += self.bead.offset
        self.tokenCursor.setPosition(start_pos, QTextCursor.MoveAnchor)
        self.tokenCursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        self.tokenCursor.mergeCharFormat(self.tokenFmt)
                    
class Ui_MainWindow(object):
    
    def createToolbar(self, MainWindow):
        # toolbar
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        # play
        self.actionPlay = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "play.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay.setIcon(icon)
        # pause
        self.actionPause = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "pause.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon)
        # previous word
        self.actionPrevWord = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "prev.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevWord.setIcon(icon)
        self.actionPrevWord.triggered.connect(lambda _: self.player.playRelativeToken(-1))    
        # next word
        self.actionNextWord = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "next.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextWord.setIcon(icon)
        self.actionNextWord.triggered.connect(lambda _: self.player.playRelativeToken(1))
        # stop
        self.actionStop = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "stop.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon)
        # prvious sentence
        self.actionPrevSent = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "first.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevSent.setIcon(icon)
        self.actionPrevSent.triggered.connect(lambda _: self.player.playRelativeBead(-1))
        # next sentence
        self.actionNextSent = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "last.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextSent.setIcon(icon)
        self.actionNextSent.triggered.connect(lambda _: self.player.playRelativeBead(1))
        # previous chapter
        self.actionPrevChapter = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "skip_prev.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevChapter.setIcon(icon)
        # next chapter
        self.actionNextChapter = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "skip_next.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextChapter.setIcon(icon)
        # quit
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "exit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon)
        # add
        self.actionAdd = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "add.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd.setIcon(icon)
        # remove
        self.actionRemove = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "remove.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemove.setIcon(icon)
        # download
        self.actionDownload = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "download.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDownload.setIcon(icon)
        # settings
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "settings.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon)
        # zoom in
        self.actionZoomIn = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "zoomin.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon)
        # zoom out
        self.actionZoomOut = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "zoomout.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon)
        
        # build the toolbar
        # actions
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionRemove)
        self.toolBar.addAction(self.actionDownload)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPlay)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPrevChapter)
        self.toolBar.addAction(self.actionPrevSent)
        self.toolBar.addAction(self.actionPrevWord)
        self.toolBar.addAction(self.actionNextWord)
        self.toolBar.addAction(self.actionNextSent)
        self.toolBar.addAction(self.actionNextChapter)        
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)        
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionQuit)
        # volume
        self.volumeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volumeSlider.setRange(0, 200)
        self.volumeSlider.setValue(70)        
        self.toolBar.addSeparator()
        self.toolBar.addWidget(QtWidgets.QLabel("Volume: "))
        self.toolBar.addWidget(self.volumeSlider)
        self.volumeSlider.sliderMoved.connect(self.player.setVolume) # connect to the player
        # translation selector
        self.toolBar.addSeparator()
        self.transLanguage = QtWidgets.QComboBox()        
        selected_lang = Config.value(Config.TRANS_LANG)
        for idx, (code, label) in enumerate(LANGUAGES.items()):
            self.transLanguage.addItem(label, code)
            if code == selected_lang:
                self.transLanguage.setCurrentIndex(idx)
        self.toolBar.addWidget(QtWidgets.QLabel("Translate to: "))
        self.toolBar.addWidget(self.transLanguage)        

    def setupUi(self, MainWindow):
        MainWindow.resize(1280, 800)
        self.player = player.Player(MainWindow, Config.value(Config.SKIP_INTRO))  # Medi palyer
        self.downloadManager = dl_manager.DownloadManager(MainWindow) # download manager
        # main gui window
        self.centralwidget = QtWidgets.QWidget(MainWindow) 
        MainWindow.setCentralWidget(self.centralwidget)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget) # horizontal layout for the browser/reader
                
        # flexible splitter for the browser/reader separator
        self.horizontalSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal) 
        self.mainLayout.addWidget(self.horizontalSplitter) 

        # widget for the navigator tree
        self.navigatorWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalSplitter.addWidget(self.navigatorWidget)
        self.navigatorLayout = QtWidgets.QVBoxLayout() # vertical box for the tree/download progress indicator
        self.navigatorWidget.setLayout(self.navigatorLayout)
        
        # tree view label
        self.lblBooks = QtWidgets.QLabel(self.centralwidget) 
        self.navigatorLayout.addWidget(self.lblBooks) 

        # tree view for the books
        self.bookList = QtWidgets.QTreeView(self.centralwidget) 
        self.navigatorLayout.addWidget(self.bookList)

        # download label
        self.lblDownload = QtWidgets.QLabel(self.centralwidget)
        self.navigatorLayout.addWidget(self.lblDownload)
        self.lblDownload.hide()

        # download progress bar
        self.downloadProgress = QtWidgets.QProgressBar(self.centralwidget)
        self.downloadProgress.setProperty("value", 0)
        self.navigatorLayout.addWidget(self.downloadProgress)
        self.downloadProgress.hide()

        # layout for the selected content and its positions        
        self.progressLayout = QtWidgets.QVBoxLayout()

        # widget for the selected content
        self.contentWidget = QtWidgets.QWidget()
        self.contentWidget.setLayout(self.progressLayout)

        # selected content
        self.selectedContent = QtWidgets.QLabel("Selected Content: None")
        self.progressLayout.addWidget(self.selectedContent)

        # position in the content
        self.chapterSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.centralwidget)
        self.progressLayout.addWidget(self.chapterSlider)
        self.chapterSlider.sliderMoved.connect(self.player.setPosition)

        # split content for the two reader panes
        self.contentPane = QtWidgets.QWidget(self.centralwidget)
        self.contentLayout = QtWidgets.QVBoxLayout()
        self.contentPane.setLayout(self.contentLayout)

        # splitter for the two rreaders        
        self.readerSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        # add the reader pane to the horizontal splitter
        self.contentLayout.addWidget(self.contentWidget)
        self.contentLayout.addWidget(self.readerSplitter)
        self.horizontalSplitter.addWidget(self.contentPane)        
        self.horizontalSplitter.setStretchFactor(1, 1)

        # reader for the 1st language
        self.readerWidget = ReaderWidget()
        self.readerSplitter.addWidget(self.readerWidget)

        # reader for the 2nd language
        self.foreignReaderWidget = ReaderWidget()
        self.readerSplitter.addWidget(self.foreignReaderWidget)
        self.readerSplitter.setStretchFactor(2, 1)

        # status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # create the toolbar
        self.createToolbar(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Book Reader"))
        self.lblBooks.setText(_translate("MainWindow", "Books"))
        self.lblDownload.setText(_translate("MainWindow", "Download Progress"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionPlay.setText(_translate("MainWindow", "Play"))
        self.actionPlay.setToolTip(_translate("MainWindow", "Play Chapter"))
        self.actionPlay.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionPause.setText(_translate("MainWindow", "Pause"))
        self.actionPause.setToolTip(_translate("MainWindow", "Pause"))
        self.actionPause.setShortcut(_translate("MainWindow", "Space"))
        self.actionPrevWord.setText(_translate("MainWindow", "Previous Word"))
        self.actionPrevWord.setToolTip(_translate("MainWindow", "Play the previous word"))
        self.actionPrevWord.setShortcut(_translate("MainWindow", "Left"))
        self.actionNextWord.setText(_translate("MainWindow", "Next Word"))
        self.actionNextWord.setToolTip(_translate("MainWindow", "Play the next word"))
        self.actionNextWord.setShortcut(_translate("MainWindow", "Right"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionStop.setToolTip(_translate("MainWindow", "Stop player"))
        self.actionStop.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionPrevSent.setText(_translate("MainWindow", "Previous Sentence"))
        self.actionPrevSent.setToolTip(_translate("MainWindow", "Play previous sentence"))
        self.actionPrevSent.setShortcut(_translate("MainWindow", "Up"))
        self.actionNextSent.setText(_translate("MainWindow", "Next Sentence"))
        self.actionNextSent.setToolTip(_translate("MainWindow", "Play next sentence"))
        self.actionNextSent.setShortcut(_translate("MainWindow", "Down"))
        self.actionPrevChapter.setText(_translate("MainWindow", "Previous Chapter"))
        self.actionPrevChapter.setToolTip(_translate("MainWindow", "Play previous chapter"))
        self.actionPrevChapter.setShortcut(_translate("MainWindow", "Ctrl+Left"))
        self.actionNextChapter.setText(_translate("MainWindow", "Next Chapter"))
        self.actionNextChapter.setToolTip(_translate("MainWindow", "Play next chapter"))
        self.actionNextChapter.setShortcut(_translate("MainWindow", "Ctrl+Right"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit Application"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionAdd.setToolTip(_translate("MainWindow", "Add book or chapter"))
        self.actionAdd.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionRemove.setText(_translate("MainWindow", "Remove"))
        self.actionRemove.setToolTip(_translate("MainWindow", "Remove book or chapter"))
        self.actionRemove.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionDownload.setText(_translate("MainWindow", "Download"))
        self.actionDownload.setToolTip(_translate("MainWindow", "Download book or chapter"))
        self.actionDownload.setShortcut(_translate("MainWindow", "Ctrl+D"))        
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("MainWindow", "Application Settings"))
        self.actionZoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoomIn.setToolTip(_translate("MainWindow", "Zoom in the reader pane"))
        self.actionZoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.actionZoomOut.setToolTip(_translate("MainWindow", "Zoom out the reader pane"))


