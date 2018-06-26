
import os

ROOT = '/home/hegistva/programming/python/sync-reader'
TEMP_DIR = os.path.join(ROOT, 'temp/audio')
os.makedirs(TEMP_DIR, exist_ok=True)
AUDIO_ALIGNER = os.path.join(ROOT, 'tools/speechaligner.jar')
AUDIO_TRANSCRIBER = os.path.join(ROOT, 'tools/transcriber.jar')
LIBRARY = os.path.join(ROOT, 'library')