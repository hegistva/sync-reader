

import vlc
import model
import time
import model

from PyQt5 import QtCore


class Player(QtCore.QObject):

    token_changed = QtCore.pyqtSignal(model.Token, name='tokenChanged')
    bead_changed = QtCore.pyqtSignal(model.Bead, name='beadChanged')
    position_changed = QtCore.pyqtSignal(int, name='positionChanged')
    length_changed = QtCore.pyqtSignal(int, name='lengthChanged')
    chapter_ended = QtCore.pyqtSignal(name='chapterEnded')

    def __init__(self, parent=None, skipIntro=True):            
        super(Player, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timeout = 40
        self.prevPosition = 0
        self.instance = vlc.Instance() 
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(70)
        self.length = 0
        self.audio_file = None
        self.content = None
        self.token = None
        self.bead = None
        self.skipIntro = skipIntro
        self.currentBead = None
        self.currentToken = None
        self.nextPauseTime = None

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
            self.gotoStart() # skip to the start if needed         
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

    def gotoStart(self):
        """Skip to the start of the chapter"""
        if self.skipIntro:            
            if self.content:
                self.setPosition(self.content.audioStart)

    def playRelativeBead(self, offset):
        if self.currentBead:            
            next_bead = self.content.getBead(self.currentBead.id + offset)
            if not next_bead is None:
                start_token = self.content.tokenAtPosition(next_bead.text_start)
                end_token = self.content.tokenAtPosition(next_bead.text_end)
                if not end_token is None:
                    if start_token is None:
                        start_pos = self.content.audioStart
                    else:
                        start_pos = start_token.audio_end - 100
                    end_pos = end_token.audio_end - 100
                    self.nextPauseTime = end_pos
                    self.setPosition(start_pos)
                    if self.player.get_state() != vlc.State.Playing:
                        self.pause()

    def playRelativeToken(self, offset):
        if self.currentToken:
            print(self.currentToken)
            print(self.getPosition())
            next_token = self.content.getToken(self.currentToken.id + offset + 1)
            print(next_token)
            if not next_token is None:
                start_pos = next_token.audio_start
                end_pos = next_token.audio_end
                self.nextPauseTime = end_pos
                self.setPosition(start_pos)
                if self.player.get_state() != vlc.State.Playing:
                    self.pause()

    def playNextToken(self):
        if self.currentToken:
            print("current token is: %s" % self.currentToken.id)

    def playPreviousToken(self):
        if self.currentToken:
            print("current token is: %s" % self.currentToken.id)

    def update(self):
        if self.player.get_state() == vlc.State.Ended:
            self.timer.stop() # stop the timer
            self.chapter_ended.emit() # emit event
            return                
        newPosition = self.getPosition()
        if not self.nextPauseTime is None and newPosition >= self.nextPauseTime:
            self.pause() # auto-pause
            return 
        if self.skipIntro and newPosition > self.content.audioEnd:
            self.stop()
            self.chapter_ended.emit()
            return            
        if not self.prevPosition == newPosition:
            self.prevPosition = newPosition            
            self.position_changed.emit(newPosition)
            if self.content:
                tkn = self.content.currentToken(newPosition)
                if tkn != self.token:
                    self.token = tkn
                    if tkn >= 0:
                        tkn_obj = model.Token(tkn, *self.content.audioMap[tkn])
                        bead = self.content.currentBead(tkn_obj.text_end)
                        if bead != self.bead:
                            self.bead = bead
                            bead_obj = model.Bead(*self.content.beads[bead])
                            self.bead_changed.emit(bead_obj)
                            self.currentBead = bead_obj
                        self.token_changed.emit(tkn_obj)
                        self.currentToken = tkn_obj



            
