import os
import cv2
import flet as ft
import time
from process.database.config import DataBasePaths
from process.gui.image_paths import ImagePaths
from process.gui.fonts_paths import FontPaths, register_fonts
from process.gui.views.login_page import LoginPage
from process.gui.views.register_page import RegisterPage
from process.face_processing.face_signup import FaceSignUp


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
        self.face_sign_up = FaceSignUp()

        self.user_list = []

        # Registrar las fuentes
        register_fonts(self.page, self.fonts)

        # Instanciar vistas
        self.login_view = LoginPage(page, self.images, self.show_register, self.show_login)
        self.register_view = RegisterPage(page, self.images, self.show_init, self.on_register)

        # variables de video captura
        self.signup_window = None
        self.sign_up_video = None

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
        self.show_video_capture(username)

    # Debo construir este método para cerrar la video captura automáticamente
    def close_sign_up(self):
        cv2.destroyAllWindows()
        print("Ventana de captura cerrada.")

    def show_video_capture(self, username):
        # Captura de video con OpenCV
        cap = cv2.VideoCapture(1)  # (0: Cámara integrada, 1: IriumWebcam, 2: Etc)
        #cap = cv2.VideoCapture("http://192.168.0.5:4747/video")
        cap.set(3, 1280)
        cap.set(4, 720)

        start_time = time.time()  # Tomar el tiempo inicial

        while True:
            ret, frame = cap.read()  # Leer frame
            if not ret:
                print("Error al acceder a la cámara")
                break

            # Procesar la imagen (registro facial) pasando el nombre del usuario real
            frame, save_img, info = self.face_sign_up.process(frame, username)

            # Mostrar el frame en una ventana
            cv2.imshow('Captura Facial', frame)

            # Cerrar la ventana después de 3 segundos
            if save_img and time.time() - start_time >= 5:  # Comprobar si han pasado 3 segundos
                self.close_sign_up()
                break

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
