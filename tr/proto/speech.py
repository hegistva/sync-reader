import os
from tr.libs.speech import aligner
from tr.libs.trans import utils
from tr.libs.utils import config

print(os.getcwd())

book_id = '20000LeaguesUnderTheSea'
chapter = 1
outfile = os.path.join(config.TEMP_DIR, 'chapter_%04d.audio.map' % chapter)
aligner.alignChapter(utils.Lang.FRA, book_id, chapter, outfile)
# alignChapter(utils.Lang.ENG, book_id, 1)
