
import os
import json
import numpy as np
from settings import Config
from tr.libs.trans.utils import Lang
from tr.books.book_manager import AUDIO_URL, MAPPING_URL, BEAD_URL, ID, chapterFile
from tr.books.books import FIRST_LINE, LAST_LINE, IDX, TRANSLATIONS, URL, TITLE, CHAPTERS

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

class Token(object):
    def __init__(self, idx, texts, texte, audios, audioe):
        self.id = idx
        self.text_start = texts
        self.text_end = texte
        self.audio_start = audios
        self.audio_end = audioe    

    def __str__(self):
        return "Token[Id: %s, TextStart: %s, TextEnd: %s, AudioStart: %s, AudioEnd: %s]" % (self.id, self.text_start, self.text_end, self.audio_start, self.audio_end)

class Bead(object):
    def __init__(self, idx, texts, texte):
        self.id = idx
        self.text_start = texts
        self.text_end = texte

    def __str__(self):
        return "Bead[Id: %s, TextStart: %s, TextEnd: %s]" % (self.id, self.text_start, self.text_end)

class ChapterInfo(object):
    def __init__(self, translation, chapter):
        self.audioMap = None
        self.beads = None
        self.downloaded = False
        self.translation = translation
        self.idx = chapter[IDX]
        self.firstLine = chapter[FIRST_LINE]
        self.lastLine = chapter[LAST_LINE]
        self.audioURL = chapter[AUDIO_URL]
        self.audioFile = os.path.join(self.translation.book_path, self.audioURL.split('/')[-1])
        self.mappingURL = chapter[MAPPING_URL]
        self.mappingFile = os.path.join(self.translation.book_path, self.mappingURL.split('/')[-1])
        self.beadsURL = chapter[BEAD_URL]
        self.beadsFile = os.path.join(self.translation.book_path, self.beadsURL.split('/')[-1])
        self.contentFile = os.path.join(self.translation.book_path, chapterFile(self.idx))
        self.treeNode = None
        self.translation.addChapter(self)
        self.updateStatus()

    def loadMappings(self):
        self.audioMap = np.genfromtxt(self.mappingFile, delimiter=',', dtype=[('ts', int),('te', int),('as', int),('ae', int)])
        self.audioMap.sort(order=['as'], kind='mergesort', axis=0)
        self.beads = np.genfromtxt(self.beadsFile, delimiter=',', dtype=[('id', int),('start', int),('end', int)])
        self.beads.sort(order=['start'], kind='mergesort', axis=0)
        
    def currentToken(self, time_ms):
        if not self.audioMap is None:
            return np.searchsorted(self.audioMap['as'], time_ms) - 1

    def currentBead(self, char_pos):
        if not self.beads is None:
            return np.searchsorted(self.beads['start'], char_pos) - 1

    def updateStatus(self):
        self.downloaded = os.path.exists(self.audioFile) and os.path.exists(self.mappingFile)

    def saveContent(self):
        """Save the content file from the book"""
        if not os.path.exists(self.contentFile):
            with open(self.translation.book_file, 'r') as f:
                lines = [line.strip() for line in f.readlines()]
                ch_cont = ' '.join(lines[self.firstLine-1:self.lastLine+1])
                with open(self.contentFile, 'w') as chf:
                    chf.write(ch_cont)

    def __str__(self):
        return "%s - %s %d" % (self.translation.title, CHAPTER_CAPTION[self.translation.language], self.idx)
