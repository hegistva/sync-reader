

import vlc
import model
import time
import model

class Player(object):

    def __init__(self, chapterSlider, volumeSlider):        
        self.instance = vlc.Instance() 
        self.player = self.instance.media_player_new()
        self.chapterSlider = chapterSlider
        self.volumeSlider = volumeSlider
        self.volumeSlider.sliderMoved.connect(lambda v: self.player.audio_set_volume(v))
        self.chapterSlider.sliderMoved.connect(lambda v: self.setPosition(v))
        self.player.audio_set_volume(70)
        self.length = 0
        self.audio_file = None
        
    def play(self, content):
        if content:
            if isinstance(content, model.ChapterInfo):
                # need to play a chapter
                if not content.audioFile == self.audio_file:
                    # need to load the chapter
                    self.audio_file = content.audioFile
                    media = self.instance.media_new(self.audio_file)
                    self.player.set_media(media)
                    self.player.play()
                    time.sleep(0.1)
                    self.length = self.player.get_length()
                    self.chapterSlider.setMaximum(self.length)
                else:
                    # chapter is already loaded resume/start
                    if self.player.is_playing():
                        pass
                    else:
                        self.player.play()

    def getPosition(self):
        position = self.length * self.player.get_position()
        return position

    def setPosition(self, position):      
        if self.length > 0:
            self.player.set_position(position / self.length)
        
    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
    
    def update(self):
        self.chapterSlider.setValue(self.getPosition())
