
import os

from settings import Config
from tr.books.book_manager import AUDIO_URL, MAPPING_URL
from tr.books.books import FIRST_LINE, LAST_LINE, IDX


BOOK_FILE = "book.txt"

class BookInfo(object):
    def __init__(self, bookid):
        self.bookid = bookid
        self.translations = []

    def addTranslation(self, ti):
        self.translations.append(ti)
        ti.book = self

class TranslationInfo(object):
    def __init__(self, bookid, lang, title, content_url):
        """Initialize information on a book"""
        cpath = Config.value(Config.CONTENT) # book contents
        self.book_path = os.path.join(cpath, bookid, lang) # root path of the book        
        self.book = None # identifier of the book
        self.book_file = os.path.join(self.book_path, BOOK_FILE) # path to the local file
        self.book_dl = os.path.exists(self.book_file) # downloaded?
        self.language = lang # Language
        self.title = title # Title
        self.content_url = content_url # URL of the content
        self.chapters = [] # List of chapters
    
    def addChapter(self, chapter):
        """Add a chapter to the book"""
        self.chapters.append(chapter)
        chapter.translation = self

class ChapterInfo(object):
    def __init__(self, chapter):        
        self.translation = None
        self.idx = chapter[IDX]
        self.firstLine = chapter[FIRST_LINE]
        self.lastLine = chapter[LAST_LINE]
        self.audioURL = chapter[AUDIO_URL]
        self.mappingURL = chapter[MAPPING_URL]

    def __str__(self):
        return "%s %s %s" % (self.translation.title, self.translation.language, self.idx)
