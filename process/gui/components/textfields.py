import flet as ft


class TextFieldFactory:
    def create_text_with_label(self, label_text="", field_label="", hint_text="", font_family="", label_size=18,
                               text_size=16, width=300, height=None, password=False, filled=True,
                               label_top=0, label_left=0, textfield_top=0, textfield_left=0):
        # Contenedor para el texto explicativo con posición independiente
        label_container = ft.Container(
            content=ft.Text(
                value=label_text,
                size=label_size,
                color=ft.colors.WHITE,
                font_family=font_family
            ),
            top=label_top,
            left=label_left,
        )

        # Contenedor para el campo de texto con posición independiente
        text_field_container = ft.Container(
            content=ft.TextField(
                label=field_label,
                hint_text=hint_text,
                width=width,
                height=height,
                password=password,
                filled=filled,
                border_radius=10,
                border_color=ft.colors.BLUE,
                bgcolor=ft.colors.TRANSPARENT,
                text_style=ft.TextStyle(
                    font_family=font_family,
                    size=text_size,
                    color=ft.colors.BLACK
                ),
                label_style=ft.TextStyle(
                    color=ft.colors.WHITE,
                    size=15,
                    font_family=font_family
                )
            ),
            top=textfield_top,
            left=textfield_left,
        )

        # Retornar ambos controles como una lista para organizarlos en la posición deseada
        return [label_container, text_field_container]
