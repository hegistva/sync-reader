
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from reader_rc import Ui_MainWindow
import settings
import search
import book_nav
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
        book_nav.initNavigator(self.ui.bookList, self)

    def stop(self):
        self.ui.chapterProgress.hide()

    def play(self):
        sender = self.sender()
        print("Playing chaper: %s" % sender.property('model'))
        self.ui.chapterProgress.show()

    def download(self):
        sender = self.sender()
        print("Downloading chaper: %s" % sender.property('model'))
        self.ui.lblDownload.show()
        self.ui.downloadProgress.show()        
    
    def showSettings(self):
        settings.showSettings(self)

    def showSearch(self):
        search.showSearch(self)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = ReaderWidget()
    reader.show()
    sys.exit(app.exec_())
