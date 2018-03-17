
from tr.books import book_manager
from tr.libs.trans import sentence_matcher
from tr.libs.trans import utils
from tr.libs.trans import lemma_mapper

book_id = '20000LeaguesUnderTheSea'

lemma_mapper.setDefault(utils.Lang.FRA, utils.Lang.ENG)

text_fr = book_manager.bookChapter(utils.Lang.FRA, book_id, 13)
text_en = book_manager.bookChapter(utils.Lang.ENG, book_id, 13)

blocks = sentence_matcher.alignSimilar(utils.Lang.FRA, utils.Lang.ENG, text_fr, text_en)

