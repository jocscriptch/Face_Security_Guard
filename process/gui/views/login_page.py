import flet as ft
from process.gui.components.buttons import ButtonFactory
from process.gui.image_paths import ImagePaths


class LoginPage:
    def __init__(self, page, images: ImagePaths, go_to_register, go_to_login):
        self.page = page
        self.images = images
        self.go_to_login = go_to_login
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

        # Botón de iniciar sesión
        login_button = self.button_factory.create_gradient_button(
            text="Iniciar Sesión",
            on_click=self.go_to_login,
            font_family="PattaRegular"
        )

        # Botón de registro
        register_button = self.button_factory.create_gradient_button(
            text="Acceder",
            on_click=self.go_to_register,
            font_family="PattaRegular"
        )

        # Contenedores con padding para ajustar la posición de los botones
        register_button_container = ft.Container(
            content=register_button,
            padding=ft.padding.only(left=880, top=595)  # posicion del botón
        )

        login_button_container = ft.Container(
            content=login_button,
            padding=ft.padding.only(left=174, top=595)
        )

        # Stack para superponer el fondo y los botones
        content_stack = ft.Stack(
            controls=[background_image, register_button_container, login_button_container]
        )

        # Mostrar la vista en la página
        self.page.controls.clear()
        self.page.add(content_stack)
        self.page.update()