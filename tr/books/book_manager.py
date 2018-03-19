
import os
import requests

from tr.books import books

# constants
BOOKS = './library'
CHAPTERS = 'chapters'
AUDIO = 'audio'
TRANSLATIONS = 'translations'
FIRST_LINE = 'firstLine'
LAST_LINE = 'lastLine'
AUDIO_FILE = 'audioFile'
AUDIO_START = 'audioStart'
AUDIO_STOP = 'audioStop'

def chapterFile(chnum):
    return 'chapter_%04d.txt' % chnum

def chapterPath(lang, bookid, chapter):
    return os.path.join(BOOKS, bookid, lang, CHAPTERS, chapterFile(chapter))

def chapterAudio(lang, bookid, chapter):
    ch = books.LIBRARY[bookid][TRANSLATIONS][lang][CHAPTERS][chapter-1]
    fname = ch[AUDIO_FILE]
    fpath = os.path.join(BOOKS, bookid, lang, AUDIO, fname)
    audio_start = ch[AUDIO_START]
    audio_stop = ch[AUDIO_STOP]
    return (fpath, audio_start, audio_stop)

def bookChapter(lang, bookid, chapter):
    cp = chapterPath(lang, bookid, chapter)
    with open(cp, 'r') as cf:
        return cf.read()

def allChapters(bookid, lang):
    return list(range(1, 1+len(books.LIBRARY[bookid][TRANSLATIONS][lang][CHAPTERS])))

def downloadBook(bookid):
    # find book in library
    bookdef = books.LIBRARY[bookid]
    # create folder for the library
    os.makedirs(BOOKS, exist_ok=True)
    for lang, content in bookdef[TRANSLATIONS].items():
        langpath = os.path.join(BOOKS, bookid, lang)
        os.makedirs(langpath, exist_ok=True)
        bookfile = os.path.join(langpath, 'book.txt')
        if not os.path.exists(bookfile):
            r = requests.get(content['url'])
            with open(bookfile, 'w')  as bf:
                bf.write(r.text)
        ch_path = os.path.join(langpath, CHAPTERS)
        os.makedirs(ch_path, exist_ok=True)
        with open(bookfile, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            for ch_idx, chdef in enumerate(content[CHAPTERS]):
                ch_file = chapterFile(ch_idx + 1)
                curr_ch = os.path.join(ch_path, ch_file)
                if not os.path.exists(curr_ch):
                    # extract and save chapter
                    ch_cont = ' '.join(lines[chdef[FIRST_LINE]-1:chdef[LAST_LINE]+1])
                    with open(curr_ch, 'w') as chf:
                        chf.write(ch_cont)
                        print("Saved chapter %s" % curr_ch)
