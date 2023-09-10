import flet as ft
from core.frontend import constants


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
    return ft.View(
        route="/iteraction",
        controls=[
            tool_bar
        ]
    )
