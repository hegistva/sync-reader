from tr.books import book_manager
from tr.libs.trans import book_mapper
from tr.libs.trans import utils


book_id = '20000LeaguesUnderTheSea'
book_manager.downloadBook(book_id)

# book_mapper.mapChapter(utils.Lang.FRA, utils.Lang.ENG, book_id, 13, debug=True)
book_mapper.mapBook(utils.Lang.FRA, utils.Lang.ENG, book_id, chapters=[13], chapterToPrint=13)
