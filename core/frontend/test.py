import pyrebase
import flet
from flet import *
import datetime
from functools import partial


config = {
    "apiKey": "AIzaSyBXjdgvvO2K50WjHvnO-UYBkMb25gfTQe4",
    "authDomain": "hack-it-df775.firebaseapp.com",
    "projectId": "hack-it-df775",
    "storageBucket": "hack-it-df775.appspot.com",
    "messagingSenderId": "47867283538",
    "appId": "1:47867283538:web:1e441d139b0a7702d1f78b",
    "databaseURL": "",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class UserWidget(UserControl):
    def __init__(
            self,
            title: str,
            sub_title: str,
        ):
        self.title = title
        self.sub_title = sub_title
        super().__init__()


    def InputTextField(self, text: str):
        return Container(
            alignment=alignment.center,
            content=TextField(
                height=48,
                width=255,
                bgcolor="#f0f3f6",
                hint_text=text,
            ),
        )


    def build(self):
        self._title = Container(
            alignment=alignment.center,
            content=Text(
                self.title,
                size=15,
                text_align="center",
                weight="bold",
                color="black",
            ),
        )

        self._sub_title = Container(
            alignment=alignment.center,
            content=Text(
                self.sub_title,
                size=10,
                text_align="center",
                color="black"
            ),
        )

        return Column(
            horizontal_alignment="center",
            controls=[
                Container(padding=10),
                self._title,
                self._sub_title,
            ],
        )


def main(page: Page):
    page.title = "Flet with FB"
    page.bgcolor = "#f0f3f6"
    page.horizontal_alignment = "center"
    page.vertical_alignment = " center"

    def _main_column_():
        return Container(
            width=280,
            height=600,
            bgcolor="#ffffff",
            padding=12,
            border_radius=35,
            content=Column(
                spacing=20,
                horizontal_alignment="center",
            ),
        )

    _sign_in_ = UserWidget(
        "Welcome back!",
        "Enter your account details below",
    )

    _register_ = UserWidget(
        "Registration!",
        "Register your email and password below",
    )

    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(Container(padding=15))
    _sign_in_main.content.controls.append(_sign_in_)

    _reg_main = _main_column_()
    _reg_main.content.controls.append(Container(padding=15))
    _reg_main.content.controls.append(_register_)

    page.add(
        Row(
            alignment="center",
            spacing=25,
            controls=[
                _sign_in_main,
                _reg_main,
            ],
        )
    )


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")
