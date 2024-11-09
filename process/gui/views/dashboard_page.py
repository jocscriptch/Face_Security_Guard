import flet as ft


class DashBoardPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content_shown = False  # Bandera para controlar la visibilidad
        self.home_active = True  # Estado de Home
        self.dashboard_active = False  # Estado de Dashboard

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
                            color=ft.colors.WHITE),
                    ft.Text("El sistema avanzado de seguridad basado en reconocimiento facial.", size=18,
                            color=ft.colors.WHITE),

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
                            self.create_image_container("Características", "https://link-a-tu-imagen-1.jpg"),
                            self.create_image_container("Verificación Facial", "https://link-a-tu-imagen-2.jpg"),
                            self.create_image_container("Seguridad Avanzada", "https://link-a-tu-imagen-3.jpg"),
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

    def create_image_container(self, title: str, image_url: str):
        """ Función para crear un contenedor con imagen y título """
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Image(src=image_url, width=250, height=250),  # Tamaño ajustable según necesidad
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=300,
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=8
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

        # Tabla de vehículos (inicialmente oculta)
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

        return stats_cards if self.content_shown else ft.Container()

    def logout(self, e):
        """ Manejar clic en el botón de Cerrar Sesión """
        self.page.add(ft.Text("Sesión cerrada."))
        self.page.update()  # Actualizar la página después de cerrar sesión