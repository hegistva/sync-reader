from tr.libs.trans import utils
from tr.books.books import AUDIO_FILE, AUDIO_START, AUDIO_STOP, AUTHOR, TRANSLATIONS, CHAPTERS, FIRST_LINE, LAST_LINE, TITLE, URL, IDX

VOLUME = {
    'JourneyToTheCenterOfTheEarth': {
        AUTHOR: 'Jules Verne',
        TRANSLATIONS: {
            utils.Lang.FRA: {
                TITLE: 'Voyage au Centre de la Terre',
                URL: 'http://www.gutenberg.org/cache/epub/4791/pg4791.txt',
                CHAPTERS: [
                    { IDX: 1, FIRST_LINE: 72, LAST_LINE: 241, AUDIO_FILE: 'voyageaucentredelaterre_01_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 2, FIRST_LINE: 249, LAST_LINE: 444, AUDIO_FILE: 'voyageaucentredelaterre_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                    { IDX: 3, FIRST_LINE: 452, LAST_LINE: 735, AUDIO_FILE: 'voyageaucentredelaterre_03_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 4, FIRST_LINE: 743, LAST_LINE: 902, AUDIO_FILE: 'voyageaucentredelaterre_04_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },                    
                ]
            },
            utils.Lang.ENG: {
                TITLE: 'A Journey to the Centre of the Earth',
                URL: 'http://www.gutenberg.org/cache/epub/18857/pg18857.txt',
                CHAPTERS: [
                    { IDX: 1, FIRST_LINE: 111, LAST_LINE: 365, AUDIO_FILE: '20000lieues_1_01_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 2, FIRST_LINE: 369, LAST_LINE: 604, AUDIO_FILE: '20000lieues_1_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },                    
                ]
            },
        }
    }
}