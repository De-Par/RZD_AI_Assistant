import flet as ft
from core.frontend import constants
import whisper
import pyaudio
import wave
import numpy as np
import pandas as pd
from core.backend.pyttsx_test import *
from sentence_transformers import SentenceTransformer, util
import os
import pyttsx3
import cyrtranslit


class AIAssistant:
    def __init__(self, dataset_path: str):
        self.curr_requests = 0
        self.max_requests = 3
        self.last_entropy = ''
        self.curr_entropy = ''

        self.data = pd.read_excel(dataset_path, index_col=0)
        if os.path.exists('./core/backend/encoded.npy'):
            encoded = pd.DataFrame(np.load('./core/backend/encoded.npy', allow_pickle=True))
        else:
            encoded = self.encode_dataset(self.data, np.arange(1, 6))
            encoded = encoded.to_numpy(copy=True)
            np.save('./core/backend/encoded.npy', encoded)
        self.encoded = encoded
        self.model = SentenceTransformer('distiluse-base-multilingual-cased')

    def encode_dataset(self, dataset, columns_to_encode):
        model = SentenceTransformer('distiluse-base-multilingual-cased')
        encoded = pd.DataFrame()
        for i in range(dataset.shape[1]):
            new_column = []
            if i in columns_to_encode:
                for j in range(dataset.shape[0]):
                    try:
                        new_column.append(model.encode(dataset.iloc[j, i]))
                    except:
                        new_column.append(model.encode("NaN"))
            else:
                new_column = dataset[dataset.columns[i]]
            encoded[dataset.columns[i]] = new_column
        return encoded

    def init_new_question(self):
        self.curr_requests = 0
        self.last_entropy = ''

    def run(self, e):
        page = e.page
        while self.curr_requests <= self.max_requests:
            # 1) Listen user
            input_ = self.VTT(page)
            # 2) is this a solution
            if 'solution':
                input_encoded = self.model.encode(input_, convert_to_tensor=True)
                mx = float('-inf')
                ans = []
                ansj = float('-inf')

                for i in range(self.encoded.shape[0]):
                    for j in range(2, self.encoded.shape[1] - 3):

                        if self.data.iloc[i, 1] != page.train_model:
                            continue
                        scores = util.pytorch_cos_sim(input_encoded, self.encoded.loc[i, j])
                        if scores > mx:
                            mx = scores
                            ans.clear()
                            ans.append(i)
                            ansj = j
                        elif scores == mx:
                            ans.append(i)
                            ansj = j
                # Попали в reason (Победа)
                if ansj == self.data.shape[1] - 3:
                    text_to_speech(self.data.iloc[ans[0], ansj + 1])
                    print(self.data.iloc[ans[0], ansj])
                    return ans[0], ansj + 1
                else:
                    # Need a little bit more information
                    print(*ans)
                    return self.second_attempt(ans, ansj + 1, e)

    def second_attempt(self, ans, ansj, e):
        print(*ans, ansj)
        page = e.page
        wrong = []
        print(ansj)
        if ansj >= self.data.shape[1]:
            # Ошибка разбора (не удалось установить причину)
            return -1, -1
        for reason in range(self.encoded.shape[0]):
            if self.data.iloc[reason, ansj] not in wrong:
                self.TTS('Правда ли, что ' + self.data.iloc[reason, ansj] + '?')
                inp = self.VTT(page)

                inp = inp.lower()
                print(inp)
                if 'нет' in inp:
                    wrong.append(self.data.iloc[reason, ansj])
                elif 'да' in inp:
                    print('da')
                    print(ansj, len(self.data.columns))
                    if (ansj == (len(self.data.columns) - 3)):
                        print('yes first variant')
                        self.TTS(self.data.iloc[reason, ansj + 1])
                        return reason, ansj + 1
                    else:
                        print('yes second variant')
                        new_indexes = []
                        for i in range(self.encoded.shape[0]):
                            if self.data.iloc[reason, ansj] == self.data.iloc[i, ansj]:
                                new_indexes.append(i)
                        return self.second_attempt(new_indexes, ansj + 1, e)

    def VTT(self, page: ft.Page):
        record_voice()
        model = whisper.load_model("base")
        audio = whisper.load_audio(constants.OUTPUT_PATH)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)
        print("INPUT ---> " + cyrtranslit.to_cyrillic(result.text))
        return cyrtranslit.to_cyrillic(result.text)

    def TTS(self, msg):
        tts = pyttsx3.init()
        voices = tts.getProperty('voices')
        tts.setProperty('voice', 'ru')
        tts.setProperty("rate", 150)
        tts.setProperty("volume", 1)
        for voice in voices:
            if voice.name == 'Anna':
                tts.setProperty('voice', voice.id)

        tts.say(msg)
        tts.runAndWait()


def record_voice():
    p = pyaudio.PyAudio()
    stream = p.open(format=constants.FRT, channels=constants.CHAN, rate=constants.RT, input=True,
                    frames_per_buffer=constants.CHUNK)
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


def IteractionView(page: ft.Page, params, basket):
    assistant = AIAssistant(constants.DATASET_PATH)

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
        icon=ft.icons.ARROW_BACK_ROUNDED,
        on_click=page.go('/'),
    )
    tool_bar = ft.AppBar(
        title=ft.Text(value=f'{page.train_model}', color=constants.RED, weight=ft.FontWeight.BOLD, size=20),
        center_title=True,
        actions=[toggle_theme_button]
    )

    # Card on the center
    center_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.IconButton(
                    icon=ft.icons.MIC,
                    width=100,
                    height=100,
                    icon_size=100,
                    icon_color=ft.colors.GREEN,
                    on_click=assistant.run,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=350,
        height=450,
        alignment=ft.alignment.center,
    )
    result = ft.Text()
    return ft.View(
        route="/iteraction",
        padding=0,
        controls=[
            tool_bar,
            ft.Container(center_card,
                         alignment=ft.alignment.center,
                         image_src="./core/frontend/assets/images/background_2.png",
                         image_fit=ft.ImageFit.COVER,
                         expand=True,
                         image_opacity=0.35
                         ),
            result
        ]
    )
