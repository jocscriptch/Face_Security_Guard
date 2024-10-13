import flet as ft

class ButtonFactory:
    def create_gradient_button(self, text, on_click, font_family="", icon=None, icon_color=None, height=50, width=None):
        # Si no se especifica el ancho, lo calculamos basado en la longitud del texto
        button_width = width if width is not None else max(200, len(text) * 12)

        return ft.Container(
            height=height,  # Ajustamos el alto según el argumento
            width=button_width,  # Ajustamos el ancho según el argumento o calculado
            border_radius=ft.border_radius.all(10),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.BLUE, ft.colors.PURPLE]
            ),
            content=ft.ElevatedButton(
                text=text,
                on_click=on_click,
                icon=icon,
                icon_color=icon_color,
                color=ft.colors.WHITE,
                width=button_width,
                height=height,  # Ajustamos el alto del botón
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor={"": ft.colors.TRANSPARENT},
                    text_style=ft.TextStyle(size=20, font_family=font_family),
                )
            )
        )
