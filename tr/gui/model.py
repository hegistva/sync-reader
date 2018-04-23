
import os
import json
from settings import Config
from tr.libs.trans.utils import Lang
from tr.books.book_manager import AUDIO_URL, MAPPING_URL, ID
from tr.books.books import FIRST_LINE, LAST_LINE, IDX, TRANSLATIONS, URL, TITLE, CHAPTERS

import res

CHAPTER_CAPTION = {
    Lang.ENG: 'Chapter',
    Lang.FRA: 'Chapitre'
}

BOOK_FILE = "book.txt"

class BookInfo(object):
    def __init__(self, bookid):
        self.bookid = bookid
        self.translations = []

    def addTranslation(self, ti):
        self.translations.append(ti)

    def __str__(self):
        translations = ",".join([tr.language for tr in self.translations])
        return ("Book: %s Translations: %s" % (self.bookid, translations))

    @classmethod
    def fromJson(cls, jsonStr):
        book = json.loads(jsonStr)
        book_id = book[ID]
        ret = cls(book_id)
        for lang, tr in book[TRANSLATIONS].items():
            tr_url = tr[URL]
            tr_title = tr[TITLE]
            tr_model = TranslationInfo(ret, lang, tr_title, tr_url)
            for chapter in tr[CHAPTERS]:
                chapter_model = ChapterInfo(tr_model, chapter)
        return ret
    
    @classmethod
    def fromJsonFile(cls, pathToJson):
        with open(pathToJson, 'r') as f:
            return cls.fromJson(f.read())        
        
class TranslationInfo(object):
    def __init__(self, book_info, lang, title, content_url):
        """Initialize information on a book"""
        cpath = Config.value(Config.CONTENT) # book contents
        self.book = book_info # identifier of the book
        self.book_path = os.path.join(cpath, book_info.bookid, lang) # root path of the book                
        self.book_file = os.path.join(self.book_path, BOOK_FILE) # path to the local file        
        self.language = lang # Language
        self.title = title # Title
        self.content_url = content_url # URL of the content
        self.chapters = [] # List of chapters
        self.book.addTranslation(self)
        self.updateStatus() # update download status

    def updateStatus(self):
        self.book_dl = os.path.exists(self.book_file) # downloaded?
    
    def addChapter(self, chapter):
        """Add a chapter to the book"""
        self.chapters.append(chapter)

    def __str__(self):
        return "Title: %s [%s, %d chapters]" % (self.title, self.language, len(self.chapters))

class ChapterInfo(object):
    def __init__(self, translation, chapter):
        self.translation = translation
        self.idx = chapter[IDX]
        self.firstLine = chapter[FIRST_LINE]
        self.lastLine = chapter[LAST_LINE]
        self.audioURL = chapter[AUDIO_URL]
        self.audioFile = os.path.join(self.translation.book_path, self.audioURL.split('/')[-1])
        self.mappingURL = chapter[MAPPING_URL]
        self.mappingFile = os.path.join(self.translation.book_path, self.mappingURL.split('/')[-1])
        self.treeNode = None
        self.translation.addChapter(self)
        self.updateStatus()

    def updateStatus(self):
        self.downloaded = os.path.exists(self.audioFile) and os.path.exists(self.mappingFile)
        # update display
        if self.treeNode:
            if self.downloaded:
                self.treeNode.setIcon(res.play_icon)
            else:
                self.treeNode.setIcon(res.dl_icon)

    def __str__(self):
        return "%s - %s %d" % (self.translation.title, CHAPTER_CAPTION[self.translation.language], self.idx)
