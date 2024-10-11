import flet as ft
from process.gui.components.buttons import ButtonFactory
from process.gui.image_paths import ImagePaths


class RegisterPage:
    def __init__(self, page, images: ImagePaths, go_back_to_login):
        self.page = page
        self.images = images
        self.go_back_to_login = go_back_to_login
        self.button_factory = ButtonFactory()

    def show(self):
        # Aquí podrías usar self.images para cualquier imagen necesaria
        register_text = ft.Text(
            "Ventana de Registro Facial",
            size=30,
            font_family="PattaRegular"
        )
        back_button = self.button_factory.create_gradient_button(
            text="Volver",
            on_click=self.go_back_to_login,
            font_family="PattaRegular"
        )

        # Mostrar en la página
        self.page.controls.clear()
        self.page.add(
            ft.Column(
                controls=[register_text, back_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.update()
