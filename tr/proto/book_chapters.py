
# extract the chapter structure of a book

from tr.books import chapters
from tr.libs.trans import utils

book_id = 'AroundTheWorldIn80Days'

# chapters.extract(bookid=book_id, lang=utils.Lang.ENG, ch_re="^Chapter\s+[IVXL]+\s*$", audio_pattern="around80days_%02d_verne_64kb.mp3", first_line=144, last_line=8036)
# chapters.extract(bookid=book_id, lang=utils.Lang.FRA, ch_re="^[IVXL]{1,8}$", audio_pattern="tour_monde_%02d_verne_64kb.mp3", first_line=119, last_line=9447)

book_id = '20000LeaguesUnderTheSea'
# chapters.extract(bookid=book_id, lang=utils.Lang.ENG, ch_re="^CHAPTER\s+\d+\s*$", audio_pattern="20000leaguesundertheseas_1-%02d_verne_64kb.mp3", first_line=692, last_line=19489)
# chapters.extract(bookid=book_id, lang=utils.Lang.FRA, ch_re="\s*^[IVXL]{1,8}\s*$", audio_pattern="20000lieues_1_%02d_verne_64kb.mp3", first_line=109, last_line=18146)
