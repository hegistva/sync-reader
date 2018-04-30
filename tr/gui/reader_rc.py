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

class ReaderPane(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(ReaderPane, self).__init__(parent)
        # format for highlighting token
        self.tokenFmt = QtGui.QTextCharFormat()
        self.tokenFmt.setForeground(QtCore.Qt.darkRed)
        self.tokenFmt.setFontWeight(QtGui.QFont.Bold)
        # format for highlighting token
        self.beadFmt = QtGui.QTextCharFormat()
        self.beadFmt.setForeground(QtCore.Qt.darkBlue)
        self.beadFmt.setFontWeight(QtGui.QFont.Normal)
        # default format with no special settings
        self.regularFmt = QtGui.QTextCharFormat()
        self.regularFmt.setForeground(self.textColor())
        self.regularFmt.setFontWeight(QtGui.QFont.Normal)
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
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        self.player = player.Player(MainWindow)
        self.downloadManager = dl_manager.DownloadManager(MainWindow)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName('mainLayout')        
        self.horizontalSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.horizontalSplitter.setObjectName("horizontalSplitter") 
        self.mainLayout.addWidget(self.horizontalSplitter)
        self.navigatorWidget = QtWidgets.QWidget(self.centralwidget)
        self.navigatorLayout = QtWidgets.QVBoxLayout()
        self.navigatorLayout.setObjectName("navigatorLayout")
        self.lblBooks = QtWidgets.QLabel(self.centralwidget)
        self.lblBooks.setObjectName("lblBooks")
        self.navigatorLayout.addWidget(self.lblBooks)
        self.bookList = QtWidgets.QTreeView(self.centralwidget)
        self.bookList.setObjectName("bookList")
        self.navigatorLayout.addWidget(self.bookList)
        self.lblDownload = QtWidgets.QLabel(self.centralwidget)
        self.lblDownload.setObjectName("lblDownload")
        self.navigatorLayout.addWidget(self.lblDownload)
        self.downloadProgress = QtWidgets.QProgressBar(self.centralwidget)
        self.downloadProgress.setProperty("value", 0)
        self.downloadProgress.setObjectName("downloadProgress")
        self.navigatorLayout.addWidget(self.downloadProgress)
        self.navigatorWidget.setLayout(self.navigatorLayout)
        self.horizontalSplitter.addWidget(self.navigatorWidget)
        self.progressLayout = QtWidgets.QVBoxLayout()
        self.progressLayout.setObjectName("progressLayout")

        self.selectedContent = QtWidgets.QLabel("Selected Content: None")
        self.selectedContent.setObjectName("selectedContent")

        self.progressLayout.addWidget(self.selectedContent)

        self.chapterSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.centralwidget)
        self.progressLayout.addWidget(self.chapterSlider)
        self.chapterSlider.sliderMoved.connect(self.player.setPosition)

        self.amplitudeChart = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amplitudeChart.sizePolicy().hasHeightForWidth())
        self.amplitudeChart.setSizePolicy(sizePolicy)
        self.amplitudeChart.setMinimumSize(QtCore.QSize(0, 0))
        self.amplitudeChart.setMaximumSize(QtCore.QSize(2000, 2000))
        self.amplitudeChart.setBaseSize(QtCore.QSize(0, 0))
        self.amplitudeChart.setObjectName("amplitudeChart")
        self.progressLayout.addWidget(self.amplitudeChart)
        self.audioTokens = QtWidgets.QHBoxLayout()
        self.audioTokens.setObjectName("audioTokens")
        self.progressLayout.addLayout(self.audioTokens)
        self.textTokens = QtWidgets.QHBoxLayout()
        self.textTokens.setObjectName("textTokens")
        self.progressLayout.addLayout(self.textTokens)
        self.readerPane = ReaderPane(self.centralwidget)
        self.readerPane.setReadOnly(True)
        self.readerPane.setObjectName("readerPane")        
        self.readerSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.readerSplitter.setObjectName('readerSplitter')
        self.readerWidget = QtWidgets.QWidget(self.centralwidget)
        self.readerWidget.setLayout(self.progressLayout)
        self.horizontalSplitter.addWidget(self.readerSplitter)
        self.horizontalSplitter.setStretchFactor(1, 1)
        
        self.readerSplitter.addWidget(self.readerWidget)
        
        self.readerPaneWidget = QtWidgets.QWidget(self.centralwidget)
        self.readerPaneWidget.setObjectName('readerPaneWidget')

        self.readerPaneLayout = QtWidgets.QVBoxLayout()
        self.readerPaneLayout.setObjectName("readerPaneLayout")
        self.readerPaneLayout.addWidget(self.readerPane)

        self.readerPaneWidget.setLayout(self.readerPaneLayout)

        self.readerSplitter.addWidget(self.readerPaneWidget)
        self.readerSplitter.setStretchFactor(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.downloadProgress.hide()
        self.lblDownload.hide()

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionPlay = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "play.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay.setIcon(icon)
        self.actionPlay.setObjectName("actionPlay")
        self.actionPause = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "pause.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon1)
        self.actionPause.setObjectName("actionPause")
        self.actionPrevWord = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "prev.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevWord.setIcon(icon2)
        self.actionPrevWord.setObjectName("actionPrevWord")
        self.actionNextWord = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "next.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextWord.setIcon(icon3)
        self.actionNextWord.setObjectName("actionNextWord")
        self.actionStop = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "stop.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon4)
        self.actionStop.setObjectName("actionStop")
        self.actionPrevSent = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "first.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevSent.setIcon(icon5)
        self.actionPrevSent.setObjectName("actionPrevSent")
        self.actionNextSent = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "last.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextSent.setIcon(icon6)
        self.actionNextSent.setObjectName("actionNextSent")
        self.actionPrevChaper = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "skip_prev.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevChaper.setIcon(icon7)
        self.actionPrevChaper.setObjectName("actionPrevChaper")
        self.actionNextChaper = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "skip_next.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextChaper.setIcon(icon8)
        self.actionNextChaper.setObjectName("actionNextChaper")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "exit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon9)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAdd = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "add.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd.setIcon(icon10)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "remove.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemove.setIcon(icon11)
        self.actionRemove.setObjectName("actionRemove")
        self.actionDownload = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "download.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDownload.setIcon(icon12)
        self.actionDownload.setObjectName("actionDownload")
        # Settings toolbar item
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "settings.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon13)
        self.actionSettings.setObjectName("actionSettings")
        # ZoomIn
        self.actionZoomIn = QtWidgets.QAction(MainWindow)
        iconZoomIn = QtGui.QIcon()
        iconZoomIn.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "zoomin.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(iconZoomIn)
        # ZoomOut
        self.actionZoomOut = QtWidgets.QAction(MainWindow)
        iconZoomOut = QtGui.QIcon()
        iconZoomOut.addPixmap(QtGui.QPixmap(os.path.join(ICONS, "zoomout.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(iconZoomOut)
        

        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionRemove)
        self.toolBar.addAction(self.actionDownload)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPlay)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPrevChaper)
        self.toolBar.addAction(self.actionPrevSent)
        self.toolBar.addAction(self.actionPrevWord)
        self.toolBar.addAction(self.actionNextWord)
        self.toolBar.addAction(self.actionNextSent)
        self.toolBar.addAction(self.actionNextChaper)
        
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)        

        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionQuit)

        self.volumeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volumeSlider.setRange(0, 200)
        self.volumeSlider.setValue(70)
        self.toolBar.addWidget(self.volumeSlider)
        self.volumeSlider.sliderMoved.connect(self.player.setVolume) # connect to the player
        
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
        self.actionPrevSent.setShortcut(_translate("MainWindow", "Ctrl+Left"))
        self.actionNextSent.setText(_translate("MainWindow", "Next Sentence"))
        self.actionNextSent.setToolTip(_translate("MainWindow", "Play next sentence"))
        self.actionNextSent.setShortcut(_translate("MainWindow", "Ctrl+Right"))
        self.actionPrevChaper.setText(_translate("MainWindow", "Previous Chapter"))
        self.actionPrevChaper.setToolTip(_translate("MainWindow", "Play previous chaper"))
        self.actionPrevChaper.setShortcut(_translate("MainWindow", "Shift+Left"))
        self.actionNextChaper.setText(_translate("MainWindow", "Next Chapter"))
        self.actionNextChaper.setToolTip(_translate("MainWindow", "Play next chaper"))
        self.actionNextChaper.setShortcut(_translate("MainWindow", "Shift+Right"))
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


