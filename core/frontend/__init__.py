from . import constants
import flet as ft
import pyaudio
import wave
import whisper
from time import sleep
from dataset import headers


def header_to_dummies(header: list):
    res = []
    for sample in header:
        for model in sample.split(', ')[1:]:
            res.append(ft.dropdown.Option(model))
    return res


def greetings(page: ft.Page):
    sleep(0.5)
    page.snack_bar = ft.SnackBar(
        ft.Text(
            value  = constants.T_GREETINGS,
            size   = 15,
            weight = ft.FontWeight.BOLD,
            color  = ft.colors.WHITE,
            text_align = ft.TextAlign.CENTER,
        ),
        bgcolor  = ft.colors.BLACK,
        duration = 2000
    )
    page.snack_bar.open = True
    page.update()


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
    my_result = ft.Text()

    def get_data(e):
        page.snack_bar = ft.SnackBar(
            ft.Text(
                value  = "Recording...",
                size   = 15,
                weight = ft.FontWeight.BOLD,
                color  = ft.colors.WHITE
            ),
            bgcolor  = ft.colors.GREEN,
            duration = constants.REC_SEC * 1000
        )
        page.snack_bar.open = True
        page.update()

        my_result.value = convert_voice_to_text(page)
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        # page.update() todo
        toggle_theme_button.selected = not toggle_theme_button.selected
        page.update()


    toggle_theme_button = ft.IconButton(
        icon          = "dark_mode",
        on_click      = change_theme,
        selected_icon = "light_mode",
        tooltip       = constants.T_CHANGE_THEME,
        style         = ft.ButtonStyle(
                            color = {
                                "":         ft.colors.BLACK,
                                "selected": ft.colors.WHITE
                            },
                        )
    )

    tool_bar = ft.AppBar(
        # title        = logo_icon,
        center_title = True,
        actions      = [toggle_theme_button]
    )

    main_content = ft.Column(
        [
            ft.Text(
                value      = "Record sound to text",
                size       = 30,
                weight     = ft.FontWeight.BOLD,
                text_align = ft.TextAlign.CENTER
            ),
            ft.Divider(),
            ft.Text(
                value  = "Record only 5 seconds!",
                size   = 20,
                weight = ft.FontWeight.BOLD
            ),
            ft.ElevatedButton(
                text     = "record",
                bgcolor  = constants.RED,
                on_click = get_data,
                color    = ft.colors.WHITE,
                tooltip  = constants.T_START_REC
            ),
            my_result
        ],
        height               = 500,
        width                = 400,
        spacing              = 20,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
    )

    body = ft.Container(
        width         = 400,
        height        = 400,
        padding       = 20,
        image_opacity = 0.8,
        image_src     = "./core/frontend/assets/images/background.png",
        border_radius = 15,
        content       = main_content
    )

    page.title                = constants.APP_NAME
    page.horizontal_alignment = "center"
    page.vertical_alignment   = "center"
    page.theme_mode           = "light"
    page.padding              = 0
    page.window_width         = 1200
    page.window_height        = 800
    page.window_min_width     = 450
    page.window_min_height    = 650



    # Card on the center
    center_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(
                    src="./core/frontend/assets/icons/rzd.png",
                    width=160,
                    height=160,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Divider(opacity=0, height=1),
                ft.Text(
                    value="Выберите модель поезда:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.colors.BLACK
                ),
                ft.Divider(opacity=0, height=5),
                ft.Dropdown(
                    options=header_to_dummies(headers),
                    width=150,
                    dense=True,
                    border_color=ft.colors.BLACK,
                    color=ft.colors.RED,
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
                ),
                ft.Divider(opacity=0, height=30),
                ft.ElevatedButton("OK", bgcolor=constants.RED, on_click=get_data, color=ft.colors.WHITE, width=100, height=35),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.colors.with_opacity(0.2, color=ft.colors.WHITE),
        border_radius=5,
        width=350,
        height=450,
        blur=20,
        border=ft.border.all(1, '#000000')
    )


    page.add(
        # Toolbar
        tool_bar,
        # Divider
        #ft.Divider(opacity=0, height=30),

        # Background
        ft.Container(
            image_src = "./core/frontend/assets/images/background.png",
            image_fit = ft.ImageFit.COVER,
            expand    = True,
            alignment=ft.alignment.center,
            content=center_card

        ),

        # Divider
        ft.Divider(opacity=0, height=30),
    )

    greetings(page)
