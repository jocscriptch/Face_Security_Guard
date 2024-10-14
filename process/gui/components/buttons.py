import flet as ft


class ButtonFactory:
    @staticmethod
    def create_gradient_button(text, on_click, font_family="", icon=None, icon_color=None, height=50, width=None,
                               color_start=ft.colors.BLUE, color_end=ft.colors.PURPLE):
        # Si no se especifica el ancho, calcular segun la longitud del texto
        button_width = width if width is not None else max(200, len(text) * 12)

        return ft.Container(
            height=height,
            width=button_width,
            border_radius=ft.border_radius.all(10),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[color_start, color_end]
            ),
            content=ft.ElevatedButton(
                text=text,
                on_click=on_click,
                icon=icon,
                icon_color=icon_color,
                color=ft.colors.WHITE,
                width=button_width,
                height=height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor={"": ft.colors.TRANSPARENT},
                    text_style=ft.TextStyle(size=20, font_family=font_family),
                )
            )
        )
