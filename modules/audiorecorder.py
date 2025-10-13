#This module contains a function named record that takes a filepath of a txt file and converts it into an audio file.

from gtts import gTTS
def record(textfile,audfile):
    file = open(textfile,'r')
    content = file.read()
    file.close()
    tts = gTTS(text=content, lang='en')
    tts.save(audfile)