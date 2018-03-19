
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

audio_file = 'library/20000LeaguesUnderTheSea/eng/audio/20000leaguesundertheseas_1-01_verne_64kb.mp3'
wavfile = "%s.wav" %  os.path.splitext(audio_file)[0]

infile = "library/20000LeaguesUnderTheSea/fra/audio/sentence.mp3"
audiofile = "library/20000LeaguesUnderTheSea/fra/audio/sentence.wav"
transcript = "library/20000LeaguesUnderTheSea/fra/audio/sentence.txt"

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

def segmentTranscript(lang, bookid, chapter, audiofile):
    # get spacy models for language processing
    sp = utils.getSpacy(lang)
    text = book_manager.bookChapter(lang, bookid, chapter)
    doc = sp(text)    
    # prepare sentences without punctuation
    token_count = 0
    sentences = []    
    for sent in doc.sents:        
        sent_tokens = [tkn for tkn in sent if not tkn.is_punct and tkn.text.strip()]
        sentences.append(sent_tokens)
        token_count += len(sent_tokens)
    audio_segment = AudioSegment.from_wav(audiofile) # read the audio
    audio_len = len(audio_segment)
    begin = 0
    for sent in sentences:
        begin = alignSentence(lang, audio_segment=audio_segment, audio_len=audio_len, begin=begin, trans_len=token_count, sent=sent)
        for tkn in sent:
            print("token: %s, begin: %d, end: %d, spoken: %s" % (tkn.text, tkn._.begin, tkn._.end, tkn._.spoken))
        
# align a single sentence
# takes the
#   audio, length of audio, begin
#   sent length of transcript
#   returns the end of the last token
def alignSentence(lang, audio_segment, audio_len, begin, trans_len, sent):
    temp_audio = os.path.join(TEMP_DIR, 'temp.wav')
    temp_transcript = os.path.join(TEMP_DIR, 'transcript.txt')
    rel_len = 2 * len(sent) / trans_len
    audio_span = 5000 + int(rel_len * audio_len)
    print("Audiospan: %d" % audio_span)
    audio = audio_segment[begin:begin+audio_span]
    audio.export(temp_audio, format="wav", parameters=["-ac", "1", "-ar", "16000"])
    trans = " ".join([word.lower_ for word in sent])
    with open(temp_transcript, 'w') as f:
        f.write(trans)
    alignment = alignSpeech(lang, temp_audio, temp_transcript) # try to align the audio with the text
    lastMappedEnd = -1
    for idx, tkn in enumerate(sent):
        # print("idx: %d, token: %s" % (idx, tkn.text))
        tkn._.spoken = alignment[idx].token
        end = alignment[idx].end
        end = end if end == -1 else end + begin
        if end > 0 and ((lastMappedEnd < 0) or (end < lastMappedEnd + 5000)):
            tkn._.end = end
            lastMappedEnd = end
            bgn = alignment[idx].begin
            if bgn > 0:
                bgn += begin
                tkn._.begin = bgn
        
    # for idx, aw in enumerate(alignment):
    #     print("idx: %d, token: %s" % (idx, aw.token))
    return lastMappedEnd

book_id = '20000LeaguesUnderTheSea'
alignChapter(utils.Lang.FRA, book_id, 1)

# alignSpeech(utils.Lang.FRA, audiofile, transcript)

