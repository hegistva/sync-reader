from tr.books import book_manager
from tr.libs import book_mapper


book_id = '20000LeaguesUnderTheSea'
book_manager.downloadBook(book_id)

# book_mapper.mapChapter('fra', 'eng', book_id, 13, debug=True)
book_mapper.mapBook('fra', 'eng', book_id, chapters=None, debug=False)
