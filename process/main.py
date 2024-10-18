import flet as ft
from process.gui.image_paths import ImagePaths
from process.gui.fonts_paths import FontPaths, register_fonts
from process.gui.views.dashboard_page import DashBoardPage
from process.gui.views.login_page import LoginPage
from process.gui.views.register_page import RegisterPage

#from process.face_processing.face_signup import FacialSignup
#from process.face_processing.face_login import FacialLogin


class GraphicalUserInterface:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Seguridad Facial - IA"
        self.page.window_width = 1280
        self.page.window_height = 720
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_maximizable = False

        # Establecer un color de fondo oscuro para la página
        self.page.theme_mode = ft.ThemeMode.DARK  # Habilitar tema oscuro
        self.page.bgcolor = ft.colors.BLACK  # O establecer un color específico

        # Instanciar ImagePaths y FontPaths para obtener las rutas
        self.images = ImagePaths()
        self.fonts = FontPaths()

        # Registrar las fuentes
        register_fonts(self.page, self.fonts)

        # Instanciar vistas, pasando `self.images` a `LoginView` y `RegisterPage`
        self.login_view = LoginPage(page, self.images, self.show_register, self.show_login)
        self.register_view = RegisterPage(page, self.images, self.show_init, self.on_register)
        self.dashboard_view = DashBoardPage(page)

        # Mostrar la vista de login inicialmente
        self.show_init()

    def show_init(self, e=None):
        self.page.title = "Sistema de Seguridad Facial - IA"
        self.login_view.show()

    def show_register(self, e=None):
        self.register_view.show()

    def on_register(self, e=None):
        # Lógica para cuando se presione "Registrar"
        print("Registrar clicked!")
        # registrar las credenciales loginFacial, etc.
        # ir al login

    def show_login(self, e=None):
        # Lógica para cuando se presione "Iniciar Sesión"
        print("Iniciar Sesión clicked!")
        self.dashboard_view.show()
        # validar las credenciales loginFacial, etc.
        # ir al dashboard

    # Función para inicializar la app en la página de Flet
    def init_app(self):
        return self.page