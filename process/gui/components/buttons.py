import flet as ft


class ButtonFactory:
    def create_gradient_button(self, text, on_click, font_family=""):
        return ft.Container(
            height=50,
            width=170,
            border_radius=ft.border_radius.all(10),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.BLUE, ft.colors.PURPLE]
            ),
            content=ft.ElevatedButton(
                text=text,
                on_click=on_click,
                color=ft.colors.WHITE,
                width=170,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor={"": ft.colors.TRANSPARENT},
                    text_style=ft.TextStyle(size=20, font_family=font_family),
                )
            )
        )
