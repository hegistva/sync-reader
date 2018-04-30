

import vlc
import model
import time
import model

from PyQt5 import QtCore

class Player(QtCore.QObject):

    token_changed = QtCore.pyqtSignal(model.Token, name="tokenChanged")
    position_changed = QtCore.pyqtSignal(int, name='positionChanged')
    length_changed = QtCore.pyqtSignal(int, name='lengthChanged')

    def __init__(self, parent=None):            
        super(Player, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timeout = 100
        self.prevPosition = 0
        self.instance = vlc.Instance() 
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(70)
        self.length = 0
        self.audio_file = None
        self.content = None
        self.token = None

    def play(self, content):
        self.content = content        
        # need to play a chapter
        if not content.audioFile == self.audio_file:
            # need to load the chapter
            self.audio_file = content.audioFile
            media = self.instance.media_new(self.audio_file)
            self.player.set_media(media)
            self.player.play()
            self.measureLength() # measure length and emit change            
        else:
            # chapter is already loaded resume/start
            if self.player.is_playing():
                pass
            else:
                self.player.play()
        if not self.timer.isActive():
            self.timer.start(self.timeout)

    def getPosition(self):
        position = self.length * self.player.get_position()
        return position

    def setPosition(self, position):      
        if self.length > 0:
            self.player.set_position(position / self.length)

    def setVolume(self, volume):
        self.player.audio_set_volume(volume)
        
    def pause(self):
        if self.player.get_state() == vlc.State.Playing:
            self.timer.stop()
        else:
            self.timer.start(self.timeout)
        self.player.pause()

    def stop(self):        
        self.player.stop()
        self.timer.stop()
        self.position_changed.emit(0)
    
    def measureLength(self):
        time.sleep(0.1)
        self.length = self.player.get_length()
        self.length_changed.emit(self.length)

    def update(self):
        newPosition = self.getPosition()
        if not self.prevPosition == newPosition:
            self.prevPosition = newPosition            
            self.position_changed.emit(newPosition)
            if self.content:
                tkn = self.content.currentToken(newPosition)
                if tkn != self.token:
                    self.token = tkn
                    if tkn >= 0:
                        tkn_obj = model.Token(tkn, *self.content.audioMap[tkn])
                        self.token_changed.emit(tkn_obj)



            