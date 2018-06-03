from tr.books import book_manager
from tr.libs.trans import book_mapper
from tr.libs.trans import utils
from tr.libs.speech import aligner


book_id = '20000LeaguesUnderTheSea'
book_id = 'AroundTheWorldIn80Days'
book_manager.downloadBook(book_id)
# book_mapper.mapChapter(utils.Lang.FRA, utils.Lang.ENG, book_id, 1, doMapping=False, debug=True)

# book_mapper.mapBook(utils.Lang.FRA, utils.Lang.ENG, book_id, chapters=1, chapterToPrint=1)

# map sentence for all chapters, save results in beads files
# book_mapper.beadMapBook(utils.Lang.FRA, utils.Lang.ENG, book_id)

# speech
# start at min, stop at max-1
# for chapter in range(21, 48):
#     aligner.alignChapter(utils.Lang.ENG, book_id, chapter)

# for chapter in range(21, 48):
#     aligner.alignChapter(utils.Lang.FRA, book_id, chapter)

