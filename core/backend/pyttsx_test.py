import pyttsx3


def text_to_speech(text):
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    tts.setProperty("rate", 150)
    tts.setProperty("volume", 1)
    for voice in voices:
        if voice.name == 'Anna':
            tts.setProperty('voice', voice.id)

    tts.say(text)
    tts.runAndWait()
