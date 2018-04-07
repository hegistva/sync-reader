
import os
import requests

from tr.books import books
from tr.libs.utils import config

# constants
BOOKS = os.path.join(config.ROOT, 'library')
AUDIO = 'audio'

def chapterFile(chnum):
    return 'chapter_%04d.txt' % chnum

def chaptersPath(lang, bookid):
    return os.path.join(BOOKS, bookid, lang, books.CHAPTERS)

def chapterPath(lang, bookid, chapter):
    return os.path.join(BOOKS, bookid, lang, books.CHAPTERS, chapterFile(chapter))

class SearchResult(object):
    def __init__(self, book, author, title, langs, chapters):
        self.book = book
        self.author = author
        self.title = title
        self.languages = langs
        self.chapters = chapters

    def asList(self):
        return [self.book, self.author, self.title, self.languages, str(self.chapters)]
    
    def __str__(self):
        return "Book: %s, Author: %s, Title: %s, Languages: %s, Chapters: %s" % (self.book, self.author, self.title, self.languages, self.chapters)
    
    @staticmethod
    def fromBook(bookid, book):
        author = book[books.AUTHOR]
        titles = []
        langs = []
        chapters = 0
        for lang, tr in book[books.TRANSLATIONS].items():
            titles.append(tr[books.TITLE])
            langs.append(lang)
            chapters = len(tr[books.CHAPTERS])
        return SearchResult(bookid, author, " / ".join(titles), " / ".join(langs), chapters)
                        
def searchLibary(keyword):
    """
    Keyword based search for books, case insensitive in author and title
    
    Args: 
        keyword (string): Keyword to search for

    Return:
        List of search results
    """
    results = []
    lk = keyword.lower()
    for bookid, book in books.LIBRARY.items():
        author = book[books.AUTHOR]
        if author.lower().find(lk) >= 0:
            results.append(SearchResult.fromBook(bookid, book))
            continue
        for _, tr in book[books.TRANSLATIONS].items():
            if tr[books.TITLE].lower().find(lk) >= 0:
                results.append(SearchResult.fromBook(bookid, book))
                continue
    return results

def chapterAudio(lang, bookid, chapter):
    ch = books.LIBRARY[bookid][books.TRANSLATIONS][lang][books.CHAPTERS][chapter-1]
    fname = ch[books.AUDIO_FILE]
    fpath = os.path.join(BOOKS, bookid, lang, AUDIO, fname)
    audio_start = ch[books.AUDIO_START]
    audio_stop = ch[books.AUDIO_STOP]
    return (fpath, audio_start, audio_stop)

def bookChapter(lang, bookid, chapter):
    cp = chapterPath(lang, bookid, chapter)
    with open(cp, 'r') as cf:
        return cf.read()

def allChapters(bookid, lang):
    return list(range(1, 1+len(books.LIBRARY[bookid][books.TRANSLATIONS][lang][books.CHAPTERS])))

def downloadBook(bookid):
    # find book in library
    bookdef = books.LIBRARY[bookid]
    # create folder for the library
    os.makedirs(BOOKS, exist_ok=True)
    for lang, content in bookdef[books.TRANSLATIONS].items():
        langpath = os.path.join(BOOKS, bookid, lang)
        os.makedirs(langpath, exist_ok=True)
        bookfile = os.path.join(langpath, 'book.txt')
        if not os.path.exists(bookfile):
            r = requests.get(content['url'])
            with open(bookfile, 'w')  as bf:
                bf.write(r.text)
        ch_path = os.path.join(langpath, books.CHAPTERS)
        os.makedirs(ch_path, exist_ok=True)
        with open(bookfile, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            for ch_idx, chdef in enumerate(content[books.CHAPTERS]):
                ch_file = chapterFile(ch_idx + 1)
                curr_ch = os.path.join(ch_path, ch_file)
                if not os.path.exists(curr_ch):
                    # extract and save chapter
                    ch_cont = ' '.join(lines[chdef[books.FIRST_LINE]-1:chdef[books.LAST_LINE]+1])
                    with open(curr_ch, 'w') as chf:
                        chf.write(ch_cont)
                        print("Saved chapter %s" % curr_ch)
