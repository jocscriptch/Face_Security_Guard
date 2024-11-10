import flet as ft
from process.gui.image_paths import ImagePaths

class DashBoardPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content_shown = False  # Bandera para controlar la visibilidad
        self.home_active = True  # Estado de Home
        self.dashboard_active = False  # Estado de Dashboard
        self.image_paths = ImagePaths()  # Instancia de ImagePaths para acceder a las rutas de imagen

    def show(self):
        self.page.clean()  # Limpia cualquier contenido anterior de la página
        self.page.title = "Flet Admin Dashboard"
        self.page.theme_mode = "dark"
        self.page.padding = 0
        self.page.bgcolor = ft.colors.BLACK

        # Barra lateral
        sidebar = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Flet Admin", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.TextButton("Home", icon=ft.icons.HOME, on_click=self.navigate_home),
                    ft.TextButton("Dashboard", icon=ft.icons.DASHBOARD, on_click=self.toggle_dashboard),
                    ft.Divider(color=ft.colors.WHITE24),  # Separador antes del botón de cerrar sesión
                    ft.TextButton("Cerrar Sesión", icon=ft.icons.EXIT_TO_APP, on_click=self.logout),
                ],
                spacing=10,
                expand=True
            ),
            width=200,
            bgcolor=ft.colors.BLUE_GREY_900,
            padding=20
        )

        # Contenido de la página Home (Bienvenida y Descripción)
        home_content = ft.Container(
            content=ft.Column(
                [
                    # Mensaje de bienvenida
                    ft.Text("Bienvenido a Face Security Guard", size=30, weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Text("El sistema avanzado de seguridad basado en reconocimiento facial.", size=18,
                            color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),

                    # Descripción del Proyecto
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.Text(
                        "Face Security Guard es una plataforma diseñada para proteger tus sistemas mediante reconocimiento facial, ofreciendo una solución eficaz y moderna para la verificación de identidad en entornos seguros.",
                        size=16, color=ft.colors.WHITE),

                    # Separador visual (para las imágenes)
                    ft.Divider(color=ft.colors.WHITE24),

                    # Imágenes con Títulos
                    ft.Row(
                        [
                            self.create_image_container("Características", self.image_paths.init_system_img),
                            self.create_image_container("Verificación Facial", self.image_paths.facial_register_img),
                            self.create_image_container("Seguridad Avanzada", self.image_paths.facial_scan_img),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            padding=20,
            margin=ft.padding.only(left=40)  # Ajusta el margen izquierdo para mover el texto
        ) if self.home_active else ft.Container()

        # Contenedor principal
        self.page.add(
            ft.Row(
                [
                    sidebar,
                    ft.Column(
                        [
                            home_content,  # Mostrar solo en Home
                            self.show_dashboard()  # Mostrar Dashboard
                        ],
                        expand=True
                    )
                ],
                expand=True
            )
        )
        self.page.update()  # Asegúrate de actualizar la página después de los cambios

    def create_image_container(self, title: str, image_path: str):
        """ Función para crear un contenedor con imagen y título """
        return ft.Container(
            content=ft.Column(
                [
                    # Título con ligero padding a la izquierda para moverlo un poco a la derecha
                    ft.Container(
                        content=ft.Text(
                            title,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=ft.padding.only(left=10)  # Ajuste de padding a la izquierda
                    ),
                    # Imagen centrada con mayor altura
                    ft.Image(src=image_path, width=250, height=300, fit=ft.ImageFit.CONTAIN),
                    # Aumenta la altura de la imagen
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER  # Centra el contenido de la columna
            ),
            width=300,  # Mantener el ancho original
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=8,
            alignment=ft.alignment.center  # Centra el contenedor en la fila
        )

    def toggle_dashboard(self, e):
        """ Mostrar o ocultar el contenido del Dashboard solo si no estamos en él """
        if not self.dashboard_active:
            self.dashboard_active = True
            self.home_active = False
            self.content_shown = True  # Mostrar contenido de Dashboard
            self.show()  # Refrescar la página para reflejar el cambio

    def navigate_home(self, e):
        """ No cambiar al mismo estado, solo cuando se hace clic en el otro botón """
        if not self.home_active:
            self.home_active = True
            self.dashboard_active = False
            self.content_shown = False  # Ocultar contenido de Dashboard
            self.show()  # Refrescar la página para ocultar el contenido del Dashboard

    def show_dashboard(self):
        """ Muestra el contenido del Dashboard si es necesario """
        stats_cards = ft.Row(
            [
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.Text("Total Usuarios", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE),
                                ft.Text("Todos los usuarios registrados", size=12, color=ft.colors.WHITE54),
                                ft.Row([ft.Text("1,234", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                        ft.Icon(ft.icons.PEOPLE, color=ft.colors.CYAN)]),
                            ],
                            spacing=5
                        ),
                        padding=20,
                        bgcolor=ft.colors.BLUE_GREY_900,
                        border_radius=8
                    ),
                ),
            ],
            spacing=10
        )

        # Agregar tabla de vehículos al Dashboard
        vehicles_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Vehículo")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text("Van 001")), ft.DataCell(ft.Text("Van")),
                                  ft.DataCell(ft.Text("Disponible"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Truck 002")), ft.DataCell(ft.Text("Camión")),
                                  ft.DataCell(ft.Text("Mantenimiento"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Bus 003")), ft.DataCell(ft.Text("Autobús")),
                                  ft.DataCell(ft.Text("Disponible"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Car 004")), ft.DataCell(ft.Text("Coche")),
                                  ft.DataCell(ft.Text("Alquilado"))]),
            ],
        )

        return ft.Column(
            [
                stats_cards,
                ft.Divider(color=ft.colors.WHITE24),
                vehicles_table  # Añadir la tabla aquí
            ],
            spacing=20
        ) if self.content_shown else ft.Container()

    def logout(self, e):
        """ Manejar clic en el botón de Cerrar Sesión """
        print("Cerrando sesión...")
        self.page.update()  # Actualizar la página después de cerrar sesión
