import pyttsx3

def say_something():
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    tts.setProperty("rate", 150)
    tts.setProperty("volume", 1)
    for voice in voices:
        if voice.name == 'Anna':
            tts.setProperty('voice', voice.id)

    tts.say('Заменить перегоревший предохранитель.')
    tts.runAndWait()