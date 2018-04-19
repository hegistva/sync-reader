
from tr.libs.trans import utils

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

LIBRARY = {
    '20000LeaguesUnderTheSea': {
        AUTHOR: 'Jules Verne',
        TRANSLATIONS: {
            utils.Lang.FRA: {
                TITLE: '20000 Lieues sous les mers',
                URL: 'http://www.gutenberg.org/cache/epub/5097/pg5097.txt',
                CHAPTERS: [
                    { IDX: 1, FIRST_LINE: 111, LAST_LINE: 365, AUDIO_FILE: '20000lieues_1_01_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { IDX: 2, FIRST_LINE: 369, LAST_LINE: 604, AUDIO_FILE: '20000lieues_1_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                    { IDX: 3, FIRST_LINE: 608, LAST_LINE: 844, AUDIO_FILE: '20000lieues_1_03_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:11:56' }, 
                    { IDX: 4, FIRST_LINE: 848, LAST_LINE: 1138, AUDIO_FILE: '20000lieues_1_04_verne_64kb.mp3', AUDIO_START: '00:00:29', AUDIO_STOP:'00:15:31' },
                    { IDX: 5, FIRST_LINE: 1142, LAST_LINE: 1392, AUDIO_FILE: '20000lieues_1_05_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:14:11' },
                    { IDX: 6, FIRST_LINE: 1396, LAST_LINE: 1798, AUDIO_FILE: '20000lieues_1_06_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:20:21' },
                    { IDX: 7, FIRST_LINE: 1802, LAST_LINE: 2154, AUDIO_FILE: '20000lieues_1_07_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:17:22' },
                    { IDX: 8, FIRST_LINE: 2158, LAST_LINE: 2488, AUDIO_FILE: '20000lieues_1_08_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:19:06' },
                    { IDX: 9, FIRST_LINE: 2492, LAST_LINE: 2797, AUDIO_FILE: '20000lieues_1_09_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:14:41' },
                    { IDX: 10, FIRST_LINE: 2801, LAST_LINE: 3191, AUDIO_FILE: '20000lieues_1_10_verne_64kb.mp3', AUDIO_START: '00:00:18.5', AUDIO_STOP:'00:19:15' },
                    { IDX: 11, FIRST_LINE: 3195, LAST_LINE: 3512, AUDIO_FILE: '20000lieues_1_11_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:20:00' },
                    { IDX: 12, FIRST_LINE: 3516, LAST_LINE: 3809, AUDIO_FILE: '20000lieues_1_12_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:16:41' },
                    { IDX: 13, FIRST_LINE: 3813, LAST_LINE: 4107, AUDIO_FILE: '20000lieues_1_13_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:15:23' },
                    { IDX: 14, FIRST_LINE: 4111, LAST_LINE: 4606, AUDIO_FILE: '20000lieues_1_14_verne_64kb.mp3', AUDIO_START: '00:00:26', AUDIO_STOP:'00:25:53' },
                    { IDX: 15, FIRST_LINE: 4610, LAST_LINE: 4981, AUDIO_FILE: '20000lieues_1_15_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:16:07' },
                    { IDX: 16, FIRST_LINE: 4985, LAST_LINE: 5242, AUDIO_FILE: '20000lieues_1_16_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:15:57' },
                    { IDX: 17, FIRST_LINE: 5246, LAST_LINE: 5512, AUDIO_FILE: '20000lieues_1_17_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:13:56' },
                    { IDX: 18, FIRST_LINE: 5516, LAST_LINE: 5844, AUDIO_FILE: '20000lieues_1_18_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:18:08' },
                    { IDX: 19, FIRST_LINE: 5848, LAST_LINE: 6256, AUDIO_FILE: '20000lieues_1_19_verne_64kb.mp3', AUDIO_START: '00:00:21.5', AUDIO_STOP:'00:21:42' },
                    { IDX: 20, FIRST_LINE: 6260, LAST_LINE: 6616, AUDIO_FILE: '20000lieues_1_20_verne_64kb.mp3', AUDIO_START: '00:00:23.5', AUDIO_STOP:'00:18:05' },
                    { IDX: 21, FIRST_LINE: 6620, LAST_LINE: 7125, AUDIO_FILE: '20000lieues_1_21_verne_64kb.mp3', AUDIO_START: '00:00:25.5', AUDIO_STOP:'00:24:16' },
                ]
            },
            utils.Lang.ENG: {
                TITLE: '20000 Leagues Under the Seas',
                URL: 'http://www.gutenberg.org/cache/epub/2488/pg2488.txt',
                CHAPTERS: [
                    { IDX: 1, FIRST_LINE: 696, LAST_LINE: 958, AUDIO_FILE: '20000leaguesundertheseas_1-01_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:19:23' },
                    { IDX: 2, FIRST_LINE: 969, LAST_LINE: 1215, AUDIO_FILE: '20000leaguesundertheseas_1-02_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:13:50' },
                    { IDX: 3, FIRST_LINE: 1227, LAST_LINE: 1472, AUDIO_FILE: '20000leaguesundertheseas_1-03_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:11:49' },
                    { IDX: 4, FIRST_LINE: 1482, LAST_LINE: 1770, AUDIO_FILE: '20000leaguesundertheseas_1-04_verne_64kb.mp3', AUDIO_START: '00:00:28.5', AUDIO_STOP:'00:16:48' },
                    { IDX: 5, FIRST_LINE: 1782, LAST_LINE: 2036, AUDIO_FILE: '20000leaguesundertheseas_1-05_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:15:31' },
                    { IDX: 6, FIRST_LINE: 2046, LAST_LINE: 2450, AUDIO_FILE: '20000leaguesundertheseas_1-06_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:20:14' },
                    { IDX: 7, FIRST_LINE: 2462, LAST_LINE: 2805, AUDIO_FILE: '20000leaguesundertheseas_1-07_verne_64kb.mp3', AUDIO_START: '00:00:36', AUDIO_STOP:'00:19:02' },
                    { IDX: 8, FIRST_LINE: 2817, LAST_LINE: 3170, AUDIO_FILE: '20000leaguesundertheseas_1-08_verne_64kb.mp3', AUDIO_START: '00:00:27', AUDIO_STOP:'00:20:26.5' },
                    { IDX: 9, FIRST_LINE: 3182, LAST_LINE: 3495, AUDIO_FILE: '20000leaguesundertheseas_1-09_verne_64kb.mp3', AUDIO_START: '00:00:26', AUDIO_STOP:'00:16:09' },
                    { IDX: 10, FIRST_LINE: 3507, LAST_LINE: 3899, AUDIO_FILE: '20000leaguesundertheseas_1-10_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:20:44.5' },
                    { IDX: 11, FIRST_LINE: 3920, LAST_LINE: 4240, AUDIO_FILE: '20000leaguesundertheseas_1-11_verne_64kb.mp3', AUDIO_START: '00:00:36', AUDIO_STOP:'00:20:20' },
                    { IDX: 12, FIRST_LINE: 4250, LAST_LINE: 4546, AUDIO_FILE: '20000leaguesundertheseas_1-12_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:15:44' },
                    { IDX: 13, FIRST_LINE: 4560, LAST_LINE: 4846, AUDIO_FILE: '20000leaguesundertheseas_1-13_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:15:01' },
                    { IDX: 14, FIRST_LINE: 4859, LAST_LINE: 5349, AUDIO_FILE: '20000leaguesundertheseas_1-14_verne_64kb.mp3', AUDIO_START: '00:00:19.5', AUDIO_STOP:'00:13:57' },
                    { IDX: 15, FIRST_LINE: 5378, LAST_LINE: 5761, AUDIO_FILE: '20000leaguesundertheseas_1-15_verne_64kb.mp3', AUDIO_START: '00:00:32', AUDIO_STOP:'00:17:07' },
                    { IDX: 16, FIRST_LINE: 5772, LAST_LINE: 6029, AUDIO_FILE: '20000leaguesundertheseas_1-16_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:17:20' },
                    { IDX: 17, FIRST_LINE: 6039, LAST_LINE: 6307, AUDIO_FILE: '20000leaguesundertheseas_1-17_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:18:06' },
                    { IDX: 18, FIRST_LINE: 6326, LAST_LINE: 6655, AUDIO_FILE: '20000leaguesundertheseas_1-18_verne_64kb.mp3', AUDIO_START: '00:00:21', AUDIO_STOP:'00:16:46' },
                    { IDX: 19, FIRST_LINE: 6669, LAST_LINE: 7087, AUDIO_FILE: '20000leaguesundertheseas_1-19_verne_64kb.mp3', AUDIO_START: '00:00:20', AUDIO_STOP:'00:26:50' },
                    { IDX: 20, FIRST_LINE: 7101, LAST_LINE: 7456, AUDIO_FILE: '20000leaguesundertheseas_1-20_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:22:42' },
                    { IDX: 21, FIRST_LINE: 7466, LAST_LINE: 7982, AUDIO_FILE: '20000leaguesundertheseas_1-11_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:26:04' },
                ]
            },
        }
    }
}