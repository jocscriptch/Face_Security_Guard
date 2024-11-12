import cv2
import flet as ft
import time

from process.gui.image_paths import ImagePaths
from process.gui.fonts_paths import FontPaths, register_fonts
from process.gui.views.dashboard_page import DashBoardPage
from process.gui.views.login_page import LoginPage
from process.gui.views.register_page import RegisterPage
from process.face_processing.face_signup import FaceSignUp
from process.face_processing.face_login import FaceLogIn
from process.gui.components.alertdialogs import AlertDialogFactory
from mongodb.db_functions import insert_user, get_user


class GraphicalUserInterface:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Seguridad Facial - IA"
        self.page.window_width = 1280
        self.page.window_height = 720
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_maximizable = False

        # fondo oscuro
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = ft.colors.BLACK

        # Instanciar ImagePaths y FontPaths
        self.images = ImagePaths()
        self.fonts = FontPaths()

        self.face_sign_up = FaceSignUp(self.images)
        self.face_login = FaceLogIn(self.images)
        self.user_list = []
        self.user_access = None

        # Registrar las fuentes
        register_fonts(self.page, self.fonts)

        # Instanciar vistas
        self.login_view = LoginPage(page, self.images, self.show_register, self.show_login)
        self.register_view = RegisterPage(page, self.images, self.show_init, self.on_register)
        self.dashboard_view = DashBoardPage(self.page, self)

        # **Instanciar AlertDialogFactory**
        self.alert_factory = AlertDialogFactory(self.page)

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
        username = self.register_view.username_textfield.value.strip()

        if len(username) == 0:
            self.alert_factory.show_warning_dialog("¡Información incompleta! Por favor, ingrese un nombre de usuario.")
            return

        # Verificar si el usuario ya está registrado en MongoDB
        existing_user = get_user(username)
        if existing_user:
            self.alert_factory.show_warning_dialog(f"¡Usuario {username} ya registrado!")
            return

        # Iniciar la captura de video al registrar
        self.show_register_capture(username)

    def close_window_video_capture(self):
        cv2.destroyAllWindows()
        print("Ventana de captura cerrada.")

    # captura de video en el registro
    def show_register_capture(self, username):
        # Captura de video con OpenCV
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                self.alert_factory.show_error_dialog("Error al acceder a la cámara")
                break

            # Procesar la imagen (registro facial)
            frame, save_img, info = self.face_sign_up.process(frame, username)

            # Mostrar el frame en una ventana
            cv2.imshow('Captura Facial', frame)

            # Cerrar la ventana luego de 3 segundos desde que se guardó la imagen
            if self.face_sign_up.success_start_time and time.time() - self.face_sign_up.success_start_time >= 3:
                # Intenta insertar el usuario en MongoDB
                if save_img:
                    result = insert_user(username, save_img)
                    self.alert_factory.show_success_dialog(f"Usuario {username} registrado exitosamente!")

                self.close_window_video_capture()
                self.show_init()  # Ir al inicio
                break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    # captura de video en el login
    def show_login_capture(self):
        self.face_login.reset_cont_frame()
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                self.alert_factory.show_error_dialog("Error al acceder a la cámara")
                # print("Error al acceder a la cámara")
                break

            # procesar la imagen (iniciar sesión facial)
            frame, self.user_access, info, username = self.face_login.process(frame)
            cv2.imshow('Inicio Sesion Facial', frame)

            # Si el usuario tiene acceso, mostrar el dashboard
            if self.user_access:
                self.alert_factory.show_success_dialog(f"¡Bienvenido {username} 🤖!")
                self.dashboard_view.show()

            if self.user_access and time.time() - start_time >= 2:
                self.close_window_video_capture()
                break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_login(self, e=None):
        self.show_login_capture()

    def init_app(self):
        return self.page
