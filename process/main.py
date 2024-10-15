import os
import cv2
import flet as ft
from process.database.config import DataBasePaths
from process.gui.image_paths import ImagePaths
from process.gui.fonts_paths import FontPaths, register_fonts
from process.gui.views.login_page import LoginPage
from process.gui.views.register_page import RegisterPage


class GraphicalUserInterface:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Seguridad Facial - IA"
        self.page.window_width = 1280
        self.page.window_height = 720
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_maximizable = False

        # Instanciar rutas de imágenes y fuentes
        self.images = ImagePaths()
        self.fonts = FontPaths()
        self.database = DataBasePaths()

        self.user_list = []

        # Registrar las fuentes
        register_fonts(self.page, self.fonts)

        # Instanciar vistas
        self.login_view = LoginPage(page, self.images, self.show_register, self.show_login)
        self.register_view = RegisterPage(page, self.images, self.show_init, self.on_register)

        # Mostrar la vista de login inicialmente
        self.show_init()

    def show_init(self, e=None):
        self.page.title = "Sistema de Seguridad Facial - IA"
        self.login_view.show()

    def show_register(self, e=None):
        self.register_view.show()

    def on_register(self, e=None):
        # Capturar el texto del campo de usuario
        username = self.register_view.username_textfield.value.strip()

        # Validar que el campo de usuario no esté vacío
        if len(username) == 0:
            print("¡Información incompleta! Por favor, ingrese un nombre de usuario.")
            return  # No continuar si el campo está vacío

        # Ruta del archivo del usuario
        user_file_path = os.path.join(self.database.users, f"{username}.txt")

        # Verificar si el usuario ya está registrado
        if os.path.exists(user_file_path):
            print(f"¡Usuario '{username}' ya registrado!")
            return  # No continuar si el usuario ya existe

        # Guardar usuario en txt por el momento (base de datos)
        with open(user_file_path, "w") as file:
            file.write(f"Usuario: {username}")
        print(f"¡Usuario {username} registrado exitosamente!")

        # Limpiar el campo de texto después de registrar
        self.register_view.username_textfield.value = ""
        self.register_view.username_textfield.update()

        # Iniciar la captura de video al registrar
        self.show_video_capture()

    def show_video_capture(self):
        # Captura de video con OpenCV
        cap = cv2.VideoCapture(1)  # (0: Cámara integrada, 1: IriumWebcam, 2: Etc)
        cap.set(3, 1280)
        cap.set(4, 720)

        while True:
            ret, frame = cap.read()  # Leer frame
            if not ret:
                print("Error al acceder a la cámara")
                break

            # Mostrar el frame en una ventana
            cv2.imshow('Captura Facial', frame)

            # Salir al presionar la tecla "Esc"
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_login(self, e=None):
        # Lógica para cuando se presione "Iniciar Sesión"
        print("Iniciar Sesión clicked!")

    def init_app(self):
        return self.page
