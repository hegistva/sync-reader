
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from reader_rc import Ui_MainWindow
import settings
class ReaderWidget(QMainWindow):
    
    def __init__(self, parent=None):
        super(ReaderWidget, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionPlay.triggered.connect(self.play)
        self.ui.actionSettings.triggered.connect(self.showSettings)

    def stop(self):
        self.ui.chapterProgress.hide()

    def play(self):
        self.ui.chapterProgress.show()

    def download(self):
        self.ui.chapterProgress.show()
    
    def showSettings(self):
        settings.showSettings(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = ReaderWidget()
    reader.show()
    sys.exit(app.exec_())
