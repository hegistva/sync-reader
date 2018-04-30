import subprocess
import os
import re
import spacy
from tr.libs.trans import utils
from tr.books import book_manager
from pydub import AudioSegment
from tr.libs.utils import general as gu
from tr.libs.utils import config
from progress.bar import IncrementalBar

spacy.tokens.Token.set_extension('begin', default=-1)
spacy.tokens.Token.set_extension('end', default=-1)
spacy.tokens.Token.set_extension('spoken', default='')

def msec2time(msec):
    """Convert milliseconds to human readable time strings"""
    if msec >= 0:
        minutes = int(msec / 60000)
        secs = (msec % 60000) / 1000
        return "%02d:%05.2f" % (minutes,secs)
    else:
        return "NONE"

def time2msec(timestr):
    """Convert human readable time strings to milliseconds"""
    lst = timestr.split(":")
    mult = 1000
    msecs = 0.0
    while lst:
        msecs += mult * float(lst.pop())
        mult = mult * 60
    return int(msecs)
    
class AudioWord:
    """Class to represent the audio mapping of a token"""
    def __init__(self, token, status, begin=-1, end=-1):
        self.token = token
        self.status = status
        self.begin = int(begin)
        self.end = int(end)

    def __str__(self):
        return "%s: %d-%d" % (self.token, self.begin, self.end)

def encodeForSphinx(infile, begin, end, outfile):
    """
    Use ffmpeg to extract the relevant part of an audio file and
    save it under the outfile with the encoding/sampling rate use by sphinx
    """
    if os.path.exists(infile):
        subprocess.call(['ffmpeg', '-i', infile, '-ss', begin, '-to', end, '-ar', '16000', '-ac', '1', outfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def alignAudio(lang, audio_file, transcript_file):
    """
    Call the Sphinx Java module to align an audiofile with a transcript file
    Read the results and convert

    Args:
        lang (string): language
        audio_file (string): path to the audio file 
        transcript_file (string): path to the transcript file
    
    Returns:
        list(AudioWord): Alignment status if applicable the start/end of each token
    """
    rmapped = re.compile(r'^(?P<type>MAPPED):\s(?P<token>\S+)\s+\[(?P<from>\d+):(?P<to>\d+)]$')
    rmissing = re.compile(r'^(?P<type>MISSING):\s(?P<token>\S+)\s+$')
    outfile = os.path.join(config.TEMP_DIR, 'mapping.txt')
    mapping = None
    if os.path.exists(audio_file) and os.path.exists(transcript_file):
        gu.removeFile(outfile)
        ret = subprocess.call(['java', '-jar', config.AUDIO_ALIGNER, lang, audio_file, transcript_file, outfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
    gu.removeFile(outfile)
    return mapping

def alignChunk(lang, audio_segment, audio_begin, audio_end, chunk):
    """
    Align a chunk of a longer text/audio

    Args:
        lang (str): language 
        audio_segment (AudioSegment): The entire audio content
        audio_begin (int): The start of the audio range (ms)
        audio_end (int): The end of the audio range (ms)
        chunk (list of spacy Tokens): List of spacy tokens with the transcript
    
    Returns:
        (int, int): Index of the last mapped token 
        and the position of the last mapping in the audio

    """
    temp_audio = os.path.join(config.TEMP_DIR, 'temp.wav')
    temp_transcript = os.path.join(config.TEMP_DIR, 'transcript.txt')
    # print("Audio: %s - %s" % (msec2time(audio_begin), msec2time(audio_end)))
    audio = audio_segment[audio_begin:audio_end]
    audio.export(temp_audio, format="wav", parameters=["-ac", "1", "-ar", "16000"])
    trans = " ".join([word.lower_ for word in chunk])
    with open(temp_transcript, 'w') as f:
        f.write(trans)
    alignment = alignAudio(lang, temp_audio, temp_transcript) # try to align the audio with the text
    lastMappedEnd = -1
    lastIdx = -1
    if alignment is None:
        gu.removeFile(temp_audio)
        gu.removeFile(temp_transcript)
        return (lastIdx, lastMappedEnd)
    # add mapping information to the tokens
    for idx, tkn in enumerate(chunk):
        tkn._.spoken = alignment[idx].token
        end = alignment[idx].end
        end = end if end == -1 else end + audio_begin
        if end > 0 and ((lastMappedEnd < 0) or (end < lastMappedEnd + 10000)):
            tkn._.end = end
            lastMappedEnd = end
            lastIdx = idx
            bgn = alignment[idx].begin
            if bgn > 0:
                bgn += audio_begin
                tkn._.begin = bgn        
    gu.removeFile(temp_audio)
    gu.removeFile(temp_transcript)
    return (lastIdx, lastMappedEnd)


def saveAudioMapping(mtks, start_time, stop_time, outfile):
    """
    Write audio mapping information to a file

    Args:
        mtks (list): List of mapped tokens
        start_time (int): offset to be added to the audio coordintes
        stop_time (int): end of the whole audio
        outfile (string): file to save the mapping into
    """
    last_recognized_audio_end = start_time
    unrecognized_text_start = 0
    has_unrecognized = False
    
    with open(outfile, 'w') as f:
        for mtk in mtks:            
            if mtk._.begin >= 0 and mtk._.end >= 0: # recognized token, map it
                if has_unrecognized: # close the unrecognized section
                    f.write("%d,%d,%d,%d\n" % (unrecognized_text_start, mtk.idx - 1, last_recognized_audio_end + 100, mtk._.begin + start_time - 100))
                f.write("%d,%d,%d,%d\n" % (mtk.idx, mtk.idx + len(mtk.text),  mtk._.begin + start_time, mtk._.end + start_time))
                last_recognized_audio_end = mtk._.end + start_time
                has_unrecognized = False
            else: # unrecognized token
                if not has_unrecognized:
                    has_unrecognized = True
                    unrecognized_text_start = mtk.idx
        if has_unrecognized: # close the unrecognized section
            f.write("%d,%d,%d,%d\n" % (unrecognized_text_start, mtks[-1].idx + len(mtks[-1]), last_recognized_audio_end + 100, stop_time))
                
def alignChapter(lang, bookid, chapter):
    """
    Align a chapter of a book

    Args:
        lang (str): language
        bookid (str): identifier of a book
        chapter (int): the chapter to be aligned
    
    Returns:
        list of spacy tokens: the tokens with the added audio alignment information
    """
    bar = IncrementalBar('Processing %s [%s] (%s)' % (bookid, lang, chapter) , max=100)
    bar.start()
    outfile = os.path.join(book_manager.chaptersPath(lang, bookid),book_manager.mappingFile(chapter))
    audio_file, start_time, stop_time = book_manager.chapterAudio(lang, bookid, chapter)
    wavfile = os.path.join(config.TEMP_DIR, 'chapter%s.wav' % chapter)
    gu.removeFile(wavfile)
    encodeForSphinx(audio_file, start_time, stop_time, wavfile) # encode audio for speech recognition
    # get spacy models for language processing
    sp = utils.getSpacy(lang)
    text = book_manager.bookChapter(lang, bookid, chapter)
    doc = sp(text)    
    # prepare sentences without punctuation
    token_count = 0    
    doc_tokens = [tkn for tkn in doc if tkn.is_alpha and (not tkn.is_punct) and tkn.text.strip()]
    token_count = len(doc_tokens)
    audio_segment = AudioSegment.from_wav(wavfile) # read the audio
    audio_len = len(audio_segment)
    begin_tkn = 0
    begin_audio = 0
    startm = time2msec(start_time)
    stopm = time2msec(stop_time)
    l = stopm - startm
    
    while begin_tkn < token_count:
        chunk = doc_tokens[begin_tkn:begin_tkn+50]
        rel_len = 1.25 * len(chunk) / token_count
        end_audio = begin_audio + int(rel_len * audio_len)
        last_idx, begin_audio = alignChunk(lang, audio_segment=audio_segment, audio_begin=begin_audio, audio_end=end_audio, chunk=chunk)        
        bar.goto(int(100.0 * begin_audio / l))
        # print("Mapped up to token %d, time: %s" % (last_idx, msec2time(begin_audio)))
        # for tkn in chunk:            
        #     print("token: %s, begin: %s, end: %s, spoken: %s" % (tkn.text, msec2time(tkn._.begin), msec2time(tkn._.end), tkn._.spoken))
        if last_idx == -1: # could not map anything
            break
        else:
            begin_tkn += last_idx + 1
    gu.removeFile(wavfile)
    saveAudioMapping(doc_tokens, startm, stopm, outfile)
