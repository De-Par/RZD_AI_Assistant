import flet as ft
from time import sleep
from dataset import headers
from core.frontend import constants


def HomeView(page, params, basket):
    res = []

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        toggle_theme_button.selected = not toggle_theme_button.selected
        page.update()

    def header_to_dummies(header: list):
        res_ = []
        for sample in header:
            for model in sample.split(', ')[1:]:
                res_.append(ft.dropdown.Option(model))
        return res_

    def greetings():
        sleep(0.5)
        page.snack_bar = ft.SnackBar(
            ft.Text(
                value=constants.T_GREETINGS,
                size=15,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=ft.colors.BLACK,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    def go2ieraction(e):
        if dropdown.value:
            page.train_model = dropdown.value
            page.go('/iteraction')

    dropdown = ft.Dropdown(
                    options=header_to_dummies(headers),
                    width=150,
                    dense=True,
                    border_color=ft.colors.BLACK,
                    color=ft.colors.RED,
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    autofocus=True,
                )

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
    tool_bar = ft.AppBar(
        center_title=True,
        actions=[toggle_theme_button]
    )
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
                dropdown,
                ft.Divider(opacity=0, height=30),
                ft.ElevatedButton(
                    "OK",
                    bgcolor=constants.RED,
                    color=ft.colors.WHITE,
                    width=100,
                    height=35,
                    on_click=go2ieraction,
                ),
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
    greetings()
    return ft.View(
        route="/",
        controls=[
            tool_bar,
            ft.Container(
                image_src="./core/frontend/assets/images/background.png",
                image_opacity=0.35,
                image_fit=ft.ImageFit.COVER,
                expand=True,
                alignment=ft.alignment.center,
                content=center_card
            ),
            ft.Divider(opacity=0, height=30),
        ]
    )
