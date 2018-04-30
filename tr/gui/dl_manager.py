
import os
from pySmartDL import SmartDL
import model
from PyQt5 import QtCore
import time

class DownloadManager(QtCore.QObject):
    
    progress_changed = QtCore.pyqtSignal(int, int, name="dlProgressChanged") # download progress changed (speed, percent progress)
    completed = QtCore.pyqtSignal(name="dlCompleted") # all downloads completed
    chapter_completed = QtCore.pyqtSignal(model.ChapterInfo, name="dlCompleted") # a chapter completed

    def __init__(self, parent=None):
        super(DownloadManager, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timeout = 1000       
        self.downloads = []
        self.chapters = {}
        
    def download(self, url, targetFolder, blocking=False, chapter=None):
        os.makedirs(targetFolder, exist_ok=True)
        dl = SmartDL(urls=url, dest=targetFolder, progress_bar=False)
        if blocking:
            dl.start(blocking=True)
        else:
            dl.start(blocking=False)
            self.downloads.append(dl)
            self.chapters[url] = chapter # save url chapter so we can find it on dl complete

    def downloadChapter(self, chapter):
        
        dest = chapter.translation.book_path

        # blocking download of the book first
        if not chapter.translation.book_dl:
            self.download(chapter.translation.content_url, dest, blocking=True) # download the book first
            chapter.translation.updateStatus() # update the book status
    
        # download the chapter files next
        if not chapter.downloaded:            
            if not os.path.exists(chapter.audioFile):
                self.download(chapter.audioURL, dest, blocking=False, chapter=chapter)
            if not os.path.exists(chapter.mappingFile):
                self.download(chapter.mappingURL, dest, blocking=False, chapter=chapter)
            if not os.path.exists(chapter.beadsFile):
                self.download(chapter.beadsURL, dest, blocking=False, chapter=chapter)

    def downloadTranslation(self, translation):
        # download each chapter
        for chapter in translation.chapters:
            self.downloadChapter(chapter)

    def downloadBook(self, book):
        # download each translation
        for tr in book.translations:
            self.downloadTranslation(tr)

    def downloadContent(self, content):
        # download content
        if isinstance(content, model.ChapterInfo):
            self.downloadChapter(content)
        elif isinstance(content, model.TranslationInfo):
            self.downloadTranslation(content)
        elif isinstance(content, model.BookInfo):
            self.downloadBook(content)
        else:
            raise RuntimeError('Unknown content, cannot download it')
        if not self.timer.isActive():
            self.timer.start(self.timeout) # start the timer

    def update(self):        
        sum_dl_size = 0
        sum_file_size = 0
        sum_speed = 0
        for dl in self.downloads:
            if dl.isFinished():
                self.downloads.remove(dl) # remove finished downloads
                ch = self.chapters.get(dl.url, None)
                if ch:
                    ch.updateStatus()
                    self.chapters.pop(dl.url)
                    if ch.downloaded:
                        self.chapter_completed.emit(ch) # TODO, improve, this may complete early
            else:
                # check progress
                sum_dl_size += dl.get_dl_size()
                sum_file_size += dl.control_thread.get_final_filesize()
                sum_speed += dl.get_speed()
        if self.downloads:
            if sum_file_size > 0:
                self.progress_changed.emit(sum_speed, int(100.0 * sum_dl_size / sum_file_size))
        else:
            self.completed.emit() # indicate that downlaod is complete
            self.timer.stop() # stop the timer
