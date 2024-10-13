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
        self.page.title = "Registro Facial"
        # Imagen de fondo de la pantalla de registro
        background_image = ft.Container(
            width=1280,
            height=720,
            image_src=self.images.register_img,
            image_fit=ft.ImageFit.COVER
        )

        # Botón para volver a la pantalla de login
        back_button = self.button_factory.create_gradient_button(
            text="Volver",
            on_click=self.go_back_to_login,
            font_family="PattaRegular",
            width=150,
            height=50,
            icon="arrow_back",
            icon_color="white"
        )

        # Contenedor con padding para ajustar la posición del botón
        back_button_container = ft.Container(
            content=back_button,
            padding=ft.padding.only(left=0, top=0)
        )

        # Usar un Stack para colocar la imagen de fondo y el botón
        content_stack = ft.Stack(
            controls=[background_image, back_button_container]
        )

        # Mostrar el Stack en la página
        self.page.controls.clear()
        self.page.add(content_stack)
        self.page.update()
