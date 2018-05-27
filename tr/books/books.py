
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
                    { IDX: 22, FIRST_LINE: 7129, LAST_LINE: 7660, AUDIO_FILE: '20000lieues_1_22_verne_64kb.mp3', AUDIO_START: '00:00:24.0', AUDIO_STOP:'00:23:42' },
                    { IDX: 23, FIRST_LINE: 7664, LAST_LINE: 8033, AUDIO_FILE: '20000lieues_1_23_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:20:32' },
                    { IDX: 24, FIRST_LINE: 8037, LAST_LINE: 8359, AUDIO_FILE: '20000lieues_1_24_verne_64kb.mp3', AUDIO_START: '00:00:27.0', AUDIO_STOP:'00:18:17' },
                    { IDX: 25, FIRST_LINE: 8471, LAST_LINE: 8876, AUDIO_FILE: '20000lieues_2_01_verne_64kb.mp3', AUDIO_START: '00:00:21.0', AUDIO_STOP:'00:22:04' },
                    { IDX: 26, FIRST_LINE: 8880, LAST_LINE: 9330, AUDIO_FILE: '20000lieues_2_02_verne_64kb.mp3', AUDIO_START: '00:00:22.5', AUDIO_STOP:'00:19:22' },
                    { IDX: 27, FIRST_LINE: 9334, LAST_LINE: 9816, AUDIO_FILE: '20000lieues_2_03_verne_64kb.mp3', AUDIO_START: '00:00:22.5', AUDIO_STOP:'00:27:01' },
                    { IDX: 28, FIRST_LINE: 9820, LAST_LINE: 10357, AUDIO_FILE: '20000lieues_2_04_verne_64kb.mp3', AUDIO_START: '00:00:22.5', AUDIO_STOP:'00:29:10' },
                    { IDX: 29, FIRST_LINE: 10361, LAST_LINE: 10764, AUDIO_FILE: '20000lieues_2_05_verne_64kb.mp3', AUDIO_START: '00:00:23.5', AUDIO_STOP:'00:19:16' },
                    { IDX: 30, FIRST_LINE: 10768, LAST_LINE: 11266, AUDIO_FILE: '20000lieues_2_06_verne_64kb.mp3', AUDIO_START: '00:00:23.0', AUDIO_STOP:'00:22:25' },
                    { IDX: 31, FIRST_LINE: 11270, LAST_LINE: 11655, AUDIO_FILE: '20000lieues_2_07_verne_64kb.mp3', AUDIO_START: '00:00:24.0', AUDIO_STOP:'00:24:00' },
                    { IDX: 32, FIRST_LINE: 11659, LAST_LINE: 12093, AUDIO_FILE: '20000lieues_2_08_verne_64kb.mp3', AUDIO_START: '00:00:24.0', AUDIO_STOP:'00:21:25' },
                    { IDX: 33, FIRST_LINE: 12097, LAST_LINE: 12512, AUDIO_FILE: '20000lieues_2_09_verne_64kb.mp3', AUDIO_START: '00:00:21.0', AUDIO_STOP:'00:22:32' },
                    { IDX: 34, FIRST_LINE: 12516, LAST_LINE: 12965, AUDIO_FILE: '20000lieues_2_10_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:21:20' },
                    { IDX: 35, FIRST_LINE: 12969, LAST_LINE: 13336, AUDIO_FILE: '20000lieues_2_11_verne_64kb.mp3', AUDIO_START: '00:00:28.5', AUDIO_STOP:'00:21:05' },
                    { IDX: 36, FIRST_LINE: 13340, LAST_LINE: 13861, AUDIO_FILE: '20000lieues_2_12_verne_64kb.mp3', AUDIO_START: '00:00:25.0', AUDIO_STOP:'00:23:53' },
                    { IDX: 37, FIRST_LINE: 13865, LAST_LINE: 14362, AUDIO_FILE: '20000lieues_2_13_verne_64kb.mp3', AUDIO_START: '00:00:25.0', AUDIO_STOP:'00:27:55' },
                    { IDX: 38, FIRST_LINE: 14366, LAST_LINE: 14901, AUDIO_FILE: '20000lieues_2_14_verne_64kb.mp3', AUDIO_START: '00:00:20.0', AUDIO_STOP:'00:30:09' },
                    { IDX: 39, FIRST_LINE: 14905, LAST_LINE: 15263, AUDIO_FILE: '20000lieues_2_15_verne_64kb.mp3', AUDIO_START: '00:00:22.0', AUDIO_STOP:'00:15:19' },
                    { IDX: 40, FIRST_LINE: 15267, LAST_LINE: 15700, AUDIO_FILE: '20000lieues_2_16_verne_64kb.mp3', AUDIO_START: '00:00:21.5', AUDIO_STOP:'00:19:26' },
                    { IDX: 41, FIRST_LINE: 15704, LAST_LINE: 16114, AUDIO_FILE: '20000lieues_2_17_verne_64kb.mp3', AUDIO_START: '00:00:24.0', AUDIO_STOP:'00:23:57' },
                    { IDX: 42, FIRST_LINE: 16118, LAST_LINE: 16602, AUDIO_FILE: '20000lieues_2_18_verne_64kb.mp3', AUDIO_START: '00:00:22.0', AUDIO_STOP:'00:22:14' },
                    { IDX: 43, FIRST_LINE: 16606, LAST_LINE: 17059, AUDIO_FILE: '20000lieues_2_19_verne_64kb.mp3', AUDIO_START: '00:00:24.0', AUDIO_STOP:'00:26:55' },
                    { IDX: 44, FIRST_LINE: 17063, LAST_LINE: 17388, AUDIO_FILE: '20000lieues_2_20_verne_64kb.mp3', AUDIO_START: '00:00:19.5', AUDIO_STOP:'00:16:36' },
                    { IDX: 45, FIRST_LINE: 17392, LAST_LINE: 17787, AUDIO_FILE: '20000lieues_2_21_verne_64kb.mp3', AUDIO_START: '00:00:23.0', AUDIO_STOP:'00:19:06' },                    
                    { IDX: 46, FIRST_LINE: 17791, LAST_LINE: 18094, AUDIO_FILE: '20000lieues_2_22_verne_64kb.mp3', AUDIO_START: '00:00:23.0', AUDIO_STOP:'00:15:58' },
                    { IDX: 47, FIRST_LINE: 18098, LAST_LINE: 18146, AUDIO_FILE: '20000lieues_2_23_verne_64kb.mp3', AUDIO_START: '00:00:29.0', AUDIO_STOP:'00:03:36' }
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
                    { IDX: 21, FIRST_LINE: 7466, LAST_LINE: 7982, AUDIO_FILE: '20000leaguesundertheseas_1-21_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:26:04' },
                    { IDX: 22, FIRST_LINE: 7996, LAST_LINE: 8523, AUDIO_FILE: '20000leaguesundertheseas_1-22_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:23:02' },
                    { IDX: 23, FIRST_LINE: 8528, LAST_LINE: 8894, AUDIO_FILE: '20000leaguesundertheseas_1-23_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:18:06' },
                    { IDX: 24, FIRST_LINE: 8911, LAST_LINE: 9271, AUDIO_FILE: '20000leaguesundertheseas_1-24_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:18:50' },
                    { IDX: 25, FIRST_LINE: 9750, LAST_LINE: 10137, AUDIO_FILE: '20000leaguesundertheseas_2-01_verne_64kb.mp3', AUDIO_START: '00:00:31.5', AUDIO_STOP:'00:23:53' },
                    { IDX: 26, FIRST_LINE: 10149, LAST_LINE: 10593, AUDIO_FILE: '20000leaguesundertheseas_2-02_verne_64kb.mp3', AUDIO_START: '00:00:44', AUDIO_STOP:'00:23:13' },
                    { IDX: 27, FIRST_LINE: 10603, LAST_LINE: 11082, AUDIO_FILE: '20000leaguesundertheseas_2-03_verne_64kb.mp3', AUDIO_START: '00:00:32', AUDIO_STOP:'00:24:23' },
                    { IDX: 28, FIRST_LINE: 11094, LAST_LINE: 11623, AUDIO_FILE: '20000leaguesundertheseas_2-04_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:29:47' },
                    { IDX: 29, FIRST_LINE: 11633, LAST_LINE: 12026, AUDIO_FILE: '20000leaguesundertheseas_2-05_verne_64kb.mp3', AUDIO_START: '00:00:21', AUDIO_STOP:'00:16:41' },
                    { IDX: 30, FIRST_LINE: 12034, LAST_LINE: 12538, AUDIO_FILE: '20000leaguesundertheseas_2-06_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:21:47' },
                    { IDX: 31, FIRST_LINE: 12546, LAST_LINE: 12927, AUDIO_FILE: '20000leaguesundertheseas_2-07_verne_64kb.mp3', AUDIO_START: '00:00:17.5', AUDIO_STOP:'00:21:22' },
                    { IDX: 32, FIRST_LINE: 12937, LAST_LINE: 13367, AUDIO_FILE: '20000leaguesundertheseas_2-08_verne_64kb.mp3', AUDIO_START: '00:00:29', AUDIO_STOP:'00:23:55' },
                    { IDX: 33, FIRST_LINE: 13379, LAST_LINE: 13797, AUDIO_FILE: '20000leaguesundertheseas_2-09_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:22:19' },
                    { IDX: 34, FIRST_LINE: 13807, LAST_LINE: 14251, AUDIO_FILE: '20000leaguesundertheseas_2-10_verne_64kb.mp3', AUDIO_START: '00:00:20', AUDIO_STOP:'00:27:21' },
                    { IDX: 35, FIRST_LINE: 14261, LAST_LINE: 14618, AUDIO_FILE: '20000leaguesundertheseas_2-11_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:23:02' },
                    { IDX: 36, FIRST_LINE: 14628, LAST_LINE: 15137, AUDIO_FILE: '20000leaguesundertheseas_2-12_verne_64kb.mp3', AUDIO_START: '00:00:21', AUDIO_STOP:'00:24:51' },
                    { IDX: 37, FIRST_LINE: 15145, LAST_LINE: 15639, AUDIO_FILE: '20000leaguesundertheseas_2-13_verne_64kb.mp3', AUDIO_START: '00:00:29', AUDIO_STOP:'00:28:19' },
                    { IDX: 38, FIRST_LINE: 15649, LAST_LINE: 16185, AUDIO_FILE: '20000leaguesundertheseas_2-14_verne_64kb.mp3', AUDIO_START: '00:00:27.5', AUDIO_STOP:'00:29:31' },
                    { IDX: 39, FIRST_LINE: 16195, LAST_LINE: 16550, AUDIO_FILE: '20000leaguesundertheseas_2-15_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:17:20' },
                    { IDX: 40, FIRST_LINE: 16569, LAST_LINE: 16996, AUDIO_FILE: '20000leaguesundertheseas_2-16_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:22:53' },
                    { IDX: 41, FIRST_LINE: 17008, LAST_LINE: 17416, AUDIO_FILE: '20000leaguesundertheseas_2-17_verne_64kb.mp3', AUDIO_START: '00:00:20', AUDIO_STOP:'00:25:12' },
                    { IDX: 42, FIRST_LINE: 17426, LAST_LINE: 17897, AUDIO_FILE: '20000leaguesundertheseas_2-18_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:26:29' },
                    { IDX: 43, FIRST_LINE: 17905, LAST_LINE: 18357, AUDIO_FILE: '20000leaguesundertheseas_2-19_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:26:02' },
                    { IDX: 44, FIRST_LINE: 18379, LAST_LINE: 18703, AUDIO_FILE: '20000leaguesundertheseas_2-20_verne_64kb.mp3', AUDIO_START: '00:00:22', AUDIO_STOP:'00:23:23' },
                    { IDX: 45, FIRST_LINE: 18713, LAST_LINE: 19110, AUDIO_FILE: '20000leaguesundertheseas_2-21_verne_64kb.mp3', AUDIO_START: '00:00:27', AUDIO_STOP:'00:21:28' },
                    { IDX: 46, FIRST_LINE: 19122, LAST_LINE: 19427, AUDIO_FILE: '20000leaguesundertheseas_2-22_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:17:56' },
                    { IDX: 47, FIRST_LINE: 19437, LAST_LINE: 19489, AUDIO_FILE: '20000leaguesundertheseas_2-23_verne_64kb.mp3', AUDIO_START: '00:00:29.5', AUDIO_STOP:'00:03:59' },
                ]
            },
        }
    }
}