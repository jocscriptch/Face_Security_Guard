import flet as ft
from process.gui.components.buttons import ButtonFactory
from process.gui.image_paths import ImagePaths


class LoginPage:
    def __init__(self, page, images: ImagePaths, go_to_register):
        self.page = page
        self.images = images
        self.go_to_register = go_to_register
        self.button_factory = ButtonFactory()

    def show(self):
        # Imagen de fondo de la pantalla de login
        background_image = ft.Container(
            width=1280,
            height=720,
            image_src=self.images.init_img,
            image_fit=ft.ImageFit.COVER
        )

        # Botón de registro
        register_button = self.button_factory.create_gradient_button(
            text="Registrarse",
            on_click=self.go_to_register,
            font_family="PattaRegular"
        )

        # Contenedor para posicionar el botón
        button_container = ft.Container(
            content=register_button,
            top=600,
            left=800
        )

        # Stack para colocar fondo y botón
        content_stack = ft.Stack(
            controls=[background_image, button_container]
        )

        # Mostrar la vista en la página
        self.page.controls.clear()
        self.page.add(content_stack)
        self.page.update()
