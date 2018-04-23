
import os
from pySmartDL import SmartDL

class DownloadManager(object):
    def __init__(self, mainWindow, progressBar, progressMessage):
        self.mainWindow = mainWindow
        self.progressBar = progressBar
        self.progressMessage = progressMessage
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
                self.download(chapter.audioURL, dest, chapter=chapter)
            if not os.path.exists(chapter.mappingFile):
                self.download(chapter.mappingURL, dest, chapter=chapter)
    
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
            else:
                # check progress
                sum_dl_size += dl.get_dl_size()
                sum_file_size += dl.control_thread.get_final_filesize()
                sum_speed += dl.get_speed()
        if self.downloads:
            # download is in progress
            if not self.progressBar.isVisible():
                #  show progress bar
                self.progressBar.show()
                self.progressMessage.show()
            # set progress message and progress
            self.progressMessage.setText('Downloading at %s ...' % sum_speed)
            if sum_file_size > 0:
                self.progressBar.setValue(int(100.0 * sum_dl_size / sum_file_size))
        else:
            # if there are not downloads reset and hide the GUI elements
            self.progressBar.setValue(0)
            self.progressBar.hide()
            self.progressMessage.setText('Downloads')
            self.progressMessage.hide()
