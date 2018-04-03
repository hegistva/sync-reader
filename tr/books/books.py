
from tr.libs.trans import utils

AUDIO_FILE = 'audioFile'
AUDIO_START = 'audioStart'
AUDIO_STOP = 'audioStop'

LIBRARY = {
    '20000LeaguesUnderTheSea': {
        'author': 'Jules Verne',
        'translations': {
            utils.Lang.FRA: {
                'title': '20000 Lieues sous les mers',
                'url': 'http://www.gutenberg.org/cache/epub/5097/pg5097.txt',
                'chapters': [
                    { 'firstLine': 111, 'lastLine': 365, AUDIO_FILE: '20000lieues_1_01_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:16:42' },
                    { 'firstLine': 369, 'lastLine': 604, AUDIO_FILE: '20000lieues_1_02_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:13:11' },
                    { 'firstLine': 608, 'lastLine': 844, AUDIO_FILE: '20000lieues_1_03_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:11:56' }, 
                    { 'firstLine': 848, 'lastLine': 1138, AUDIO_FILE: '20000lieues_1_04_verne_64kb.mp3', AUDIO_START: '00:00:29', AUDIO_STOP:'00:15:31' },
                    { 'firstLine': 1142, 'lastLine': 1392, AUDIO_FILE: '20000lieues_1_05_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:14:11' },
                    { 'firstLine': 1396, 'lastLine': 1798, AUDIO_FILE: '20000lieues_1_06_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:20:21' },
                    { 'firstLine': 1802, 'lastLine': 2154, AUDIO_FILE: '20000lieues_1_07_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:17:22' },
                    { 'firstLine': 2158, 'lastLine': 2488, AUDIO_FILE: '20000lieues_1_08_verne_64kb.mp3', AUDIO_START: '00:00:24.5', AUDIO_STOP:'00:19:06' },
                    { 'firstLine': 2492, 'lastLine': 2797, AUDIO_FILE: '20000lieues_1_09_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:14:41' },
                    { 'firstLine': 2801, 'lastLine': 3191, AUDIO_FILE: '20000lieues_1_10_verne_64kb.mp3', AUDIO_START: '00:00:18.5', AUDIO_STOP:'00:19:15' },
                    { 'firstLine': 3195, 'lastLine': 3512, AUDIO_FILE: '20000lieues_1_11_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:20:00' },
                    { 'firstLine': 3516, 'lastLine': 3809, AUDIO_FILE: '20000lieues_1_12_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:16:41' },
                    { 'firstLine': 3813, 'lastLine': 4107, AUDIO_FILE: '20000lieues_1_13_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:15:23' },
                    { 'firstLine': 4111, 'lastLine': 4606, AUDIO_FILE: '20000lieues_1_14_verne_64kb.mp3', AUDIO_START: '00:00:26', AUDIO_STOP:'00:25:53' },
                    { 'firstLine': 4610, 'lastLine': 4981, AUDIO_FILE: '20000lieues_1_15_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:16:07' },
                    { 'firstLine': 4985, 'lastLine': 5242, AUDIO_FILE: '20000lieues_1_16_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:15:57' },
                    { 'firstLine': 5246, 'lastLine': 5512, AUDIO_FILE: '20000lieues_1_17_verne_64kb.mp3', AUDIO_START: '00:00:19', AUDIO_STOP:'00:13:56' },
                    { 'firstLine': 5516, 'lastLine': 5844, AUDIO_FILE: '20000lieues_1_18_verne_64kb.mp3', AUDIO_START: '00:00:23', AUDIO_STOP:'00:18:08' },
                    { 'firstLine': 5848, 'lastLine': 6256, AUDIO_FILE: '20000lieues_1_19_verne_64kb.mp3', AUDIO_START: '00:00:21.5', AUDIO_STOP:'00:21:42' },
                    { 'firstLine': 6260, 'lastLine': 6616, AUDIO_FILE: '20000lieues_1_20_verne_64kb.mp3', AUDIO_START: '00:00:23.5', AUDIO_STOP:'00:18:05' },
                    { 'firstLine': 6620, 'lastLine': 7125, AUDIO_FILE: '20000lieues_1_21_verne_64kb.mp3', AUDIO_START: '00:00:25.5', AUDIO_STOP:'00:24:16' },
                ]
            },
            utils.Lang.ENG: {
                'title': '20000 Leagues Under the Seas',
                'url': 'http://www.gutenberg.org/cache/epub/2488/pg2488.txt',
                'chapters': [
                    { 'firstLine': 696, 'lastLine': 958, AUDIO_FILE: '20000leaguesundertheseas_1-01_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:19:23' },
                    { 'firstLine': 969, 'lastLine': 1215, AUDIO_FILE: '20000leaguesundertheseas_1-02_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:13:50' },
                    { 'firstLine': 1227, 'lastLine': 1472, AUDIO_FILE: '20000leaguesundertheseas_1-03_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:11:49' },
                    { 'firstLine': 1482, 'lastLine': 1770, AUDIO_FILE: '20000leaguesundertheseas_1-04_verne_64kb.mp3', AUDIO_START: '00:00:28.5', AUDIO_STOP:'00:16:48' },
                    { 'firstLine': 1782, 'lastLine': 2036, AUDIO_FILE: '20000leaguesundertheseas_1-05_verne_64kb.mp3', AUDIO_START: '00:00:26.5', AUDIO_STOP:'00:15:31' },
                    { 'firstLine': 2046, 'lastLine': 2450, AUDIO_FILE: '20000leaguesundertheseas_1-06_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:20:14' },
                    { 'firstLine': 2462, 'lastLine': 2805, AUDIO_FILE: '20000leaguesundertheseas_1-07_verne_64kb.mp3', AUDIO_START: '00:00:36', AUDIO_STOP:'00:19:02' },
                    { 'firstLine': 2817, 'lastLine': 3170, AUDIO_FILE: '20000leaguesundertheseas_1-08_verne_64kb.mp3', AUDIO_START: '00:00:27', AUDIO_STOP:'00:20:26.5' },
                    { 'firstLine': 3182, 'lastLine': 3495, AUDIO_FILE: '20000leaguesundertheseas_1-09_verne_64kb.mp3', AUDIO_START: '00:00:26', AUDIO_STOP:'00:16:09' },
                    { 'firstLine': 3507, 'lastLine': 3899, AUDIO_FILE: '20000leaguesundertheseas_1-10_verne_64kb.mp3', AUDIO_START: '00:00:28', AUDIO_STOP:'00:20:44.5' },
                    { 'firstLine': 3920, 'lastLine': 4240, AUDIO_FILE: '20000leaguesundertheseas_1-11_verne_64kb.mp3', AUDIO_START: '00:00:36', AUDIO_STOP:'00:20:20' },
                    { 'firstLine': 4250, 'lastLine': 4546, AUDIO_FILE: '20000leaguesundertheseas_1-12_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:15:44' },
                    { 'firstLine': 4560, 'lastLine': 4846, AUDIO_FILE: '20000leaguesundertheseas_1-13_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:15:01' },
                    { 'firstLine': 4859, 'lastLine': 5349, AUDIO_FILE: '20000leaguesundertheseas_1-14_verne_64kb.mp3', AUDIO_START: '00:00:19.5', AUDIO_STOP:'00:13:57' },
                    { 'firstLine': 5378, 'lastLine': 5761, AUDIO_FILE: '20000leaguesundertheseas_1-15_verne_64kb.mp3', AUDIO_START: '00:00:32', AUDIO_STOP:'00:17:07' },
                    { 'firstLine': 5772, 'lastLine': 6029, AUDIO_FILE: '20000leaguesundertheseas_1-16_verne_64kb.mp3', AUDIO_START: '00:00:24', AUDIO_STOP:'00:17:20' },
                    { 'firstLine': 6039, 'lastLine': 6307, AUDIO_FILE: '20000leaguesundertheseas_1-17_verne_64kb.mp3', AUDIO_START: '00:00:25', AUDIO_STOP:'00:18:06' },
                    { 'firstLine': 6326, 'lastLine': 6655, AUDIO_FILE: '20000leaguesundertheseas_1-18_verne_64kb.mp3', AUDIO_START: '00:00:21', AUDIO_STOP:'00:16:46' },
                    { 'firstLine': 6669, 'lastLine': 7087, AUDIO_FILE: '20000leaguesundertheseas_1-19_verne_64kb.mp3', AUDIO_START: '00:00:20', AUDIO_STOP:'00:26:50' },
                    { 'firstLine': 7101, 'lastLine': 7456, AUDIO_FILE: '20000leaguesundertheseas_1-20_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:22:42' },
                    { 'firstLine': 7466, 'lastLine': 7982, AUDIO_FILE: '20000leaguesundertheseas_1-11_verne_64kb.mp3', AUDIO_START: '00:00:35', AUDIO_STOP:'00:26:04' },
                ]
            },
        }
    }
}