import pyttsx3
from constants import TextToAudioSettings

def text_To_Audio(outputContent):
    RATE = TextToAudioSettings.RATE
    VOLUME = TextToAudioSettings.VOLUME

    engine = pyttsx3.init()

    engine.setProperty('rate', RATE)

    engine.setProperty('volume', VOLUME)

    text = outputContent
    engine.say(text)

    engine.runAndWait()