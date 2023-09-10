import flet_route

from . import constants
import flet as ft
import pyaudio
import wave
import whisper
from flet_route import path
from .pages import (
    home, interaction
)




def record_voice():
    p = pyaudio.PyAudio()
    stream = p.open(
        format            = constants.FRT,
        channels          = constants.CHAN,
        rate              = constants.RT,
        input             = True,
        frames_per_buffer = constants.CHUNK
    )
    frames = []

    for _ in range(0, int(constants.RT / constants.CHUNK * constants.REC_SEC) + 1):
        data = stream.read(constants.CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    w = wave.open(constants.OUTPUT_PATH, 'wb')
    w.setnchannels(constants.CHAN)
    w.setsampwidth(p.get_sample_size(constants.FRT))
    w.setframerate(constants.RT)
    w.writeframes(b''.join(frames))
    w.close()


def convert_voice_to_text(pg):
    record_voice()

    pg.snack_bar = ft.SnackBar(
        ft.Text(
            value  = "Stop your voice. Processing...",
            size   = 15,
            color  = ft.colors.WHITE,
            weight = ft.FontWeight.BOLD
        ),
        bgcolor  = constants.RED,
        duration = 1500
    )
    pg.snack_bar.open = True
    pg.update()

    model = whisper.load_model("base")
    whisper.load_audio(constants.OUTPUT_PATH)
    audio = whisper.load_audio(constants.OUTPUT_PATH)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text


def app(page: ft.Page):
    app_routes = [
        path(
            '/',
            clear=True,
            view=home.HomeView
        ),
        path(
            '/iteraction',
            clear=True,
            view=interaction.IteractionView
        )

    ]
    flet_route.Routing(
        page=page,
        app_routes=app_routes,
    )

    page.title = constants.APP_NAME
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 450
    page.window_min_height = 650
    page.go(page.route)
