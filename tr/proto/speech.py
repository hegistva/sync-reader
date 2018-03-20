
import pocketsphinx
import subprocess
import os
import re
import spacy

from tr.libs.trans import utils
from tr.books import book_manager

from pydub import AudioSegment
from pydub import silence

spacy.tokens.Token.set_extension('begin', default=-1)
spacy.tokens.Token.set_extension('end', default=-1)
spacy.tokens.Token.set_extension('spoken', default='')

TEMP_DIR = 'temp'
ALIGNER = 'tools/speechaligner.jar'

class AudioWord:
    def __init__(self, token, status, begin=-1, end=-1):
        self.token = token
        self.status = status
        self.begin = int(begin)
        self.end = int(end)

    def __str__(self):
        return "%s: %d-%d" % (self.token, self.begin, self.end)

def encodeForSphinx(infile, begin, end, outfile):
    if os.path.exists(infile):
        subprocess.call(['ffmpeg', '-i', infile, '-ss', begin, '-to', end, '-ar', '16000', '-ac', '1', outfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def alignSpeech(lang, audio_file, transcript):
    rmapped = re.compile(r'^(?P<type>MAPPED):\s(?P<token>\S+)\s+\[(?P<from>\d+):(?P<to>\d+)]$')
    rmissing = re.compile(r'^(?P<type>MISSING):\s(?P<token>\S+)\s+$')
    outfile = os.path.join(TEMP_DIR, 'mapping.txt')
    if os.path.exists(audio_file) and os.path.exists(transcript):
        if os.path.exists(outfile):
            os.remove(outfile)
        ret = subprocess.call(['java', '-jar', ALIGNER, lang, audio_file, transcript, outfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret == 0: # success
            with open(outfile, 'r') as f:
                lines = f.readlines()
                mapping = []
                for line in lines:
                    m = rmapped.search(line)
                    if m:
                        mapping.append(AudioWord(m.group('token'), m.group('type'), m.group('from'), m.group('to')))                        
                    else:
                        m = rmissing.search(line)
                        if m:
                            mapping.append(AudioWord(m.group('token'), m.group('type')))
                return mapping

def alignChapter(lang, bookid, chapter):
    audio_file, start_time, stop_time = book_manager.chapterAudio(lang, bookid, chapter)
    wavfile = os.path.join(TEMP_DIR, 'chapter%s.wav' % chapter)
    if os.path.exists(wavfile):
        os.remove(wavfile)
    encodeForSphinx(audio_file, start_time, stop_time, wavfile) # encode audio for speech recognition
    # transcript = book_manager.chapterPath(lang, book_id, chapter) # find the chapter text file
    segmentTranscript(lang, bookid, chapter, wavfile)
    # alignSpeech(lang, audio_file, transcript) # try to align the audio with the text

def msec2min(msec):
    if msec >= 0:
        minutes = int(msec / 60000)
        secs = (msec % 60000) / 1000
        return "%02d:%05.2f" % (minutes,secs)
    else:
        return "NONE"

def segmentTranscript(lang, bookid, chapter, audiofile):
    # get spacy models for language processing
    sp = utils.getSpacy(lang)
    text = book_manager.bookChapter(lang, bookid, chapter)
    doc = sp(text)    
    # prepare sentences without punctuation
    token_count = 0    
    doc_tokens = [tkn for tkn in doc if tkn.is_alpha and (not tkn.is_punct) and tkn.text.strip()]
    token_count = len(doc_tokens)
    audio_segment = AudioSegment.from_wav(audiofile) # read the audio
    audio_len = len(audio_segment)
    begin_tkn = 0
    begin_audio = 0
    while begin_tkn < token_count:
        chunk = doc_tokens[begin_tkn:begin_tkn+50]
        last_idx, begin_audio = alignSentence(lang, audio_segment=audio_segment, audio_len=audio_len, begin=begin_audio, trans_len=token_count, sent=chunk)
        print("Mapped up to token %d, time: %s" % (last_idx, msec2min(begin_audio)))
        for tkn in chunk:            
            print("token: %s, begin: %s, end: %s, spoken: %s" % (tkn.text, msec2min(tkn._.begin), msec2min(tkn._.end), tkn._.spoken))
        if last_idx == -1: # could not map anything
            break
        else:
            begin_tkn += last_idx + 1
        
# align a single sentence
# takes the
#   audio, length of audio, begin
#   sent length of transcript
#   returns the end of the last index of the last mapped token and the end time for it
def alignSentence(lang, audio_segment, audio_len, begin, trans_len, sent):
    temp_audio = os.path.join(TEMP_DIR, 'temp.wav')
    temp_transcript = os.path.join(TEMP_DIR, 'transcript.txt')
    rel_len = 1.25 * len(sent) / trans_len
    audio_span = int(rel_len * audio_len)
    print("Audiospan: %s" % msec2min(audio_span))
    audio = audio_segment[begin:begin+audio_span]
    audio.export(temp_audio, format="wav", parameters=["-ac", "1", "-ar", "16000"])
    trans = " ".join([word.lower_ for word in sent])
    with open(temp_transcript, 'w') as f:
        f.write(trans)
    alignment = alignSpeech(lang, temp_audio, temp_transcript) # try to align the audio with the text
    lastMappedEnd = -1
    lastIdx = -1
    if alignment is None:
        return (lastIdx, lastMappedEnd)
    
    for idx, tkn in enumerate(sent):
        # print("idx: %d, token: %s" % (idx, tkn.text))
        tkn._.spoken = alignment[idx].token
        end = alignment[idx].end
        end = end if end == -1 else end + begin
        if end > 0 and ((lastMappedEnd < 0) or (end < lastMappedEnd + 10000)):
            tkn._.end = end
            lastMappedEnd = end
            lastIdx = idx
            bgn = alignment[idx].begin
            if bgn > 0:
                bgn += begin
                tkn._.begin = bgn
        
    # for idx, aw in enumerate(alignment):
    #     print("idx: %d, token: %s" % (idx, aw.token))
    return (lastIdx, lastMappedEnd)

book_id = '20000LeaguesUnderTheSea'
alignChapter(utils.Lang.FRA, book_id, 1)
# alignChapter(utils.Lang.ENG, book_id, 1)

