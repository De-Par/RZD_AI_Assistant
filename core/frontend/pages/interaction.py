import flet as ft
from core.frontend import constants
import whisper
import pyaudio
import wave


def convert_voice_to_text(page):
    record_voice()

    page.snack_bar = ft.SnackBar(
        ft.Text("Stop your voice. Processing...",
            size=15,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD
        ),
        bgcolor=constants.RED,
        duration=1500
    )
    page.snack_bar.open = True
    page.update()

    model = whisper.load_model("base")
    audio = whisper.load_audio(constants.OUTPUT_PATH)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text


def record_voice():
    p = pyaudio.PyAudio()
    stream = p.open(format=constants.FRT, channels=constants.CHAN, rate=constants.RT, input=True, frames_per_buffer=constants.CHUNK)
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


def do_record(e):
    print('RECORDING')
    res = convert_voice_to_text(e.page)
    print(res)


def do_forced_record(page):
    print('FORCED RECORDING')
    res = convert_voice_to_text(page)
    print(res)


def IteractionView(page: ft.Page, params, basket):
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        toggle_theme_button.selected = not toggle_theme_button.selected
        page.update()


    toggle_theme_button = ft.IconButton(
        icon="dark_mode",
        on_click=change_theme,
        selected_icon="light_mode",
        tooltip=constants.T_CHANGE_THEME,
        style=ft.ButtonStyle(
            color={
                "": ft.colors.BLACK,
                "selected": ft.colors.WHITE
            },
        )
    )

    back_button = ft.IconButton(
        icon= ft.icons.ARROW_BACK_ROUNDED,
        on_click=page.go('/'),
    )
    tool_bar = ft.AppBar(
        title=ft.Text(value=f'{page.train_model}'),
        center_title=True,
        actions=[toggle_theme_button]
    )

    # Card on the center
    center_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.IconButton(
                    icon = ft.icons.MIC,
                    width=200,
                    height=200,
                    icon_size=200,
                    icon_color=ft.colors.GREEN,
                    on_click=do_record,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=350,
        height=450,
        alignment=ft.alignment.center,
    )
    return ft.View(
        route="/iteraction",
        controls=[
            tool_bar,
            ft.Container(center_card, alignment=ft.alignment.center)
        ]
    )
