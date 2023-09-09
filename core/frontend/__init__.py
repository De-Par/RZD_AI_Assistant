from . import constants
import flet as ft
import os
import pyaudio
import wave
import whisper
from time import sleep


def greetings(pg):
    pg.snack_bar = ft.SnackBar(
        ft.Text(
            constants.T_GREETINGS,
            size=15,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE
        ),
        bgcolor=ft.colors.BLACK,
        duration=2000
    )
    pg.snack_bar.open = True
    pg.update()


def record_voice():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=constants.FRT,
        channels=constants.CHAN,
        rate=constants.RT,
        input=True,
        frames_per_buffer=constants.CHUNK
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

    ROOT_PATH = os.getcwd()
    OUTPUT_PATH = os.path.join(ROOT_PATH, constants.OUTPUT_PATH)

    pg.snack_bar = ft.SnackBar(
        ft.Text("Stop your voice. Processing...",
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
    whisper.load_audio(OUTPUT_PATH)
    audio = whisper.load_audio(OUTPUT_PATH)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text


def app(page: ft.Page):
    my_result = ft.Text()

    def get_data(e):
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Recording...",
                 size   = 15,
                 weight = ft.FontWeight.BOLD,
                 color  = ft.colors.WHITE
            ),
            bgcolor  = "green",
            duration = constants.REC_SEC * 1000
        )
        page.snack_bar.open = True
        page.update()

        my_result.value = convert_voice_to_text(page)
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

        toggle_theme_button.selected = not toggle_theme_button.selected
        page.update()

    toggle_theme_button = ft.IconButton(
        icon="dark_mode",
        on_click=change_theme,
        selected_icon="light_mode",
        tooltip=constants.T_CHANGE_THEME,
        style=ft.ButtonStyle(
            color={"": ft.colors.BLACK, "selected": ft.colors.WHITE},
        )
    )

    logo_icon = ft.Image(
        src=f"/icons/rzd_2.png",
        width=80,
        height=80,
        fit=ft.ImageFit.CONTAIN,
    )

    tool_bar = ft.AppBar(
        title=logo_icon,
        center_title=True,
        bgcolor="dark",
        actions=[toggle_theme_button]
    )

    main_content = ft.Column([
        ft.Text("Record sound to text", size=30, weight="bold", text_align=ft.TextAlign.CENTER),
        ft.Divider(),
        ft.Text("Record only 5 seconds!", size=20, weight="bold"),
        ft.ElevatedButton("record", bgcolor=constants.RED, on_click=get_data, color=ft.colors.WHITE, tooltip=constants.T_START_REC),
        my_result],
        height=500,
        width=400,
        spacing=20,
        horizontal_alignment="center"
    )

    body = ft.Container(
        width=400,
        height=400,
        padding=20,
        # gradient=LinearGradient(
        #     begin=alignment.top_center,
        #     end=alignment.bottom_center,
        #     colors=['#E21A1A', '#E2531A'],
        # ),
        image_opacity=0.8,
        image_src="assets/images/background_2.png",
        border_radius=15,
        content=main_content
    )

    page.title = constants.APP_NAME
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 20
    page.window_width = 500
    page.window_height = 700
    page.window_min_width = 300
    page.window_min_height = 650

    page.add(
        tool_bar,
        body
    )

    sleep(0.5)
    greetings(page)
