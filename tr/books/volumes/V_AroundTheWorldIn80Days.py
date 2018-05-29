
from tr.libs.trans import utils
from tr.books.books import AUDIO_FILE, AUDIO_START, AUDIO_STOP, AUTHOR, TRANSLATIONS, CHAPTERS, FIRST_LINE, LAST_LINE, TITLE, URL, IDX

VOLUME = {
    'AroundTheWorldIn80Days': {
        AUTHOR: 'Jules Verne',
        TRANSLATIONS: {
            utils.Lang.FRA: {
                TITLE: 'Le Tour du monde en quatre-vingts jours',
                URL: 'http://www.gutenberg.org/files/46541/46541-0.txt',
                CHAPTERS: [
                    { IDX: 1, FIRST_LINE: 121, LAST_LINE: 308, AUDIO_FILE: 'voyageaucentredelaterre_01_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 2, FIRST_LINE: 315, LAST_LINE: 454, AUDIO_FILE: 'voyageaucentredelaterre_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                    { IDX: 3, FIRST_LINE: 461, LAST_LINE: 773, AUDIO_FILE: 'voyageaucentredelaterre_03_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 4, FIRST_LINE: 782, LAST_LINE: 955, AUDIO_FILE: 'voyageaucentredelaterre_04_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },                    
                ]
            },
            utils.Lang.ENG: {
                TITLE: 'Around the World in 80 Days',
                URL: 'http://www.gutenberg.org/cache/epub/103/pg103.txt',
                CHAPTERS: [
                    { IDX: 1, FIRST_LINE: 146, LAST_LINE: 310, AUDIO_FILE: '20000lieues_1_01_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 2, FIRST_LINE: 317, LAST_LINE: 427, AUDIO_FILE: '20000lieues_1_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                    { IDX: 3, FIRST_LINE: 434, LAST_LINE: 704, AUDIO_FILE: '20000lieues_1_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                    { IDX: 4, FIRST_LINE: 709, LAST_LINE: 855, AUDIO_FILE: '20000lieues_1_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                ]
            },
        }
    }
}