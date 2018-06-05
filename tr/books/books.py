import os
import csv

AUDIO_FILE = 'audioFile'
AUDIO_START = 'audioStart'
AUDIO_STOP = 'audioStop'
AUTHOR = 'author'
TRANSLATIONS = 'translations'
CHAPTERS = 'chapters'
FIRST_LINE = 'firstLine'
LAST_LINE = 'lastLine'
TITLE = 'title'
URL = 'url'
IDX = 'idx'

def loadChapters(lib):
    for bookid, trs in lib.items():
        for lang, book in trs[TRANSLATIONS].items():
            ch_node = book[CHAPTERS]
            if not ch_node:
                # no chapters, load them            
                cur = os.path.dirname(os.path.realpath(__file__))
                ch_csv = os.path.join(cur, 'volumes', bookid, lang, 'chapters.csv')
                if os.path.exists(ch_csv):
                    with open(ch_csv, newline='') as csvfile:
                        r = csv.reader(csvfile, delimiter=',')
                        for row in r:
                            ch = {}
                            ch[IDX] = int(row[0])
                            ch[FIRST_LINE] = int(row[1])
                            ch[LAST_LINE] = int(row[2])
                            ch[AUDIO_FILE] = row[3]
                            ch[AUDIO_START] = row[4]
                            ch[AUDIO_STOP] = row[5]
                            ch_node.append(ch)