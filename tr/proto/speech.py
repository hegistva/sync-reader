import os
from tr.libs.speech import aligner
from tr.libs.trans import utils
from tr.libs.utils import config

book_id = '20000LeaguesUnderTheSea'

# start at min, stop at max-1
for chapter in range(11, 22):
    aligner.alignChapter(utils.Lang.ENG, book_id, chapter)
# alignChapter(utils.Lang.ENG, book_id, 1)
