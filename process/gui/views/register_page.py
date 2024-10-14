import flet as ft
from process.gui.components.buttons import ButtonFactory
from process.gui.components.textfields import TextFieldFactory
from process.gui.image_paths import ImagePaths


class RegisterPage:
    def __init__(self, page, images: ImagePaths, go_back_to_login, on_register):
        self.page = page
        self.images = images
        self.go_back_to_login = go_back_to_login
        self.on_register = on_register
        self.button_factory = ButtonFactory()
        self.textfield_factory = TextFieldFactory()

    def show(self):
        self.page.title = "Registro Facial"

        # Imagen de fondo de la pantalla de registro
        background_image = ft.Container(
            width=1280,
            height=720,
            image_src=self.images.register_img,
            image_fit=ft.ImageFit.COVER
        )

        # texfield
        username_label_and_field = self.textfield_factory.create_text_with_label(
            label_text="Nombre de Usuario",
            field_label="Nombre de usuario",
            hint_text="Ingresa tu nombre de usuario",
            label_size=25,
            text_size=16,
            width=300,
            font_family="PattaSemiBold",
            label_top=240,
            label_left=518,
            textfield_top=300,
            textfield_left=495,
        )

        # Botón para volver a la pantalla de login
        back_button = self.button_factory.create_gradient_button(
            text="Volver",
            on_click=self.go_back_to_login,
            font_family="PattaRegular",
            color_start=ft.colors.CYAN,
            color_end=ft.colors.PURPLE,
            width=150,
            height=50,
            icon="arrow_back",
            icon_color="white"
        )

        # Botón de registrar
        register_button = self.button_factory.create_gradient_button(
            text="Registrar",
            on_click=self.on_register,
            font_family="PattaRegular",
            color_start=ft.colors.CYAN,
            color_end=ft.colors.PURPLE,
            width=150,
            height=50
        )

        # Contenedor para el botón Volver
        back_button_container = ft.Container(
            content=back_button,
            top=0,    # posición Y
            left=0    # posición X
        )

        # Contenedor para el botón Registrar
        register_button_container = ft.Container(
            content=register_button,
            top=420,  # posición Y
            left=565  # posición X
        )

        # Usar un Stack para superponer la imagen de fondo y los controles posicionados
        content_stack = ft.Stack(
            controls=[
                background_image,
                *username_label_and_field,
                back_button_container,
                register_button_container

            ]
        )

        # Mostrar los elementos en la página
        self.page.controls.clear()
        self.page.add(content_stack)
        self.page.update()
