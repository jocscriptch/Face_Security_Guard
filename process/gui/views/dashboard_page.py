import flet as ft
from bson import ObjectId

from mongodb.db_functions import get_total_users, db, fs, is_user_active
from process.gui.image_paths import ImagePaths

class DashBoardPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content_shown = False
        self.home_active = True
        self.dashboard_active = False
        self.image_paths = ImagePaths()

    def show(self):
        self.page.clean()
        self.page.title = "Admin Dashboard"
        self.page.theme_mode = "dark"
        self.page.padding = 0
        self.page.bgcolor = '#13161c'

        # Barra lateral
        sidebar = ft.Container(
            content=ft.Column(
                [
                    ft.Text("FልCE𝒢UARD", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.TextButton("Home", icon=ft.icons.HOME, on_click=self.navigate_home),
                    ft.TextButton("Dashboard", icon=ft.icons.DASHBOARD, on_click=self.toggle_dashboard),
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.TextButton("Cerrar Sesión", icon=ft.icons.EXIT_TO_APP, on_click=self.logout),
                ],
                spacing=10,
                expand=True
            ),
            width=200,
            bgcolor='#191C24',
            padding=20
        )

        # Contenido de la página Home
        home_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Bienvenido a Face Security Guard", size=30, weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Text("El sistema avanzado de seguridad basado en reconocimiento facial.", size=18,
                            color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.Text(
                        "Face Security Guard es una plataforma diseñada para proteger tus sistemas mediante reconocimiento facial.",
                        size=16, color=ft.colors.WHITE),
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.Row(
                        [
                            self.create_image_container("Inicio de App", self.image_paths.init_system_img),
                            self.create_image_container("Registro Facial", self.image_paths.facial_register_img),
                            self.create_image_container("Escaneo Facial", self.image_paths.facial_scan_img),
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
            margin=ft.padding.only(left=40)
        ) if self.home_active else ft.Container()

        # Contenedor principal
        self.page.add(
            ft.Row(
                [
                    sidebar,
                    ft.Column(
                        [
                            home_content,
                            self.show_dashboard()
                        ],
                        expand=True
                    )
                ],
                expand=True
            )
        )
        self.page.update()

    def create_image_container(self, title: str, image_path: str):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    ft.Image(src=image_path, width=250, height=300, fit=ft.ImageFit.CONTAIN)
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=300,
            padding=10,
            bgcolor='#191C24',
            border_radius=8,
            alignment=ft.alignment.center
        )

    def generate_line_chart(self):
        # Obtener la lista de usuarios y sus conexiones
        users = db.users.find()
        user_names = []
        connections = []

        for user in users:
            user_names.append(user["username"])
            connections.append(len(user["access_logs"]))

        # Crear puntos de datos y series de ejemplo
        data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(x=i, y=connections[i]) for i in range(len(user_names))],
                stroke_width=6,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
                below_line_bgcolor=ft.colors.with_opacity(0.1, ft.colors.CYAN)
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(x=i, y=connections[i] * 0.8) for i in range(len(user_names))],
                stroke_width=6,
                color=ft.colors.PINK,
                curved=True,
                stroke_cap_round=True,
                below_line_bgcolor=ft.colors.with_opacity(0.1, ft.colors.PINK)
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(x=i, y=connections[i] * 0.5) for i in range(len(user_names))],
                stroke_width=6,
                color=ft.colors.LIGHT_GREEN,
                curved=True,
                stroke_cap_round=True,
                below_line_bgcolor=ft.colors.with_opacity(0.1, ft.colors.LIGHT_GREEN)
            ),
        ]

        # Configurar el gráfico de líneas
        chart = ft.LineChart(
            data_series=data_series,
            border=ft.Border(
                bottom=ft.BorderSide(2, ft.colors.GREY_600)
            ),
            left_axis=ft.ChartAxis(
                #title_size=12,
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(f"{i}", color=ft.colors.GREY_400, rotate=0))
                    # Alineación horizontal
                    for i in range(0, max(connections) + 5, 5)
                ],
                labels_size=5,
                title=ft.Text("Conexiones", color=ft.colors.GREY_400)
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(user_names[i], color=ft.colors.GREY_400))
                    for i in range(len(user_names))
                ],
                labels_size=24,  # Ajustar el tamaño de las etiquetas en el eje X
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_800, width=0.5, dash_pattern=[3, 3]),
            vertical_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_800, width=0.5, dash_pattern=[3, 3]),
            max_y=max(connections) + 5,
            min_y=0,
            expand=True,
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            width=650,
            height=350
        )

        # Envolver el gráfico en un Container para aplicar el margen
        chart_container = ft.Container(
            content=chart,
            margin=ft.margin.only(left=10, bottom=60, right=10)
        )

        return chart_container

    def show_dashboard(self):
        # Obtener el total de usuarios
        total_users = get_total_users()  # Llamamos a la función que obtiene el total de usuarios

        stats_cards = ft.Row(
            [
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.Text("Total Usuarios", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE),
                                ft.Text("Todos los usuarios registrados", size=12, color=ft.colors.WHITE54),
                                ft.Row([ft.Text(str(total_users), size=32, weight=ft.FontWeight.BOLD,
                                                color=ft.colors.WHITE),
                                        ft.Icon(ft.icons.PEOPLE, color=ft.colors.CYAN)]),
                            ],
                            spacing=5
                        ),
                        padding=20,
                        bgcolor='#1E1E2F',
                        border_radius=12,
                    ),
                    elevation=6,
                ),
            ],
            spacing=10
        )

        # Obtener la lista de usuarios
        users = db.users.find()
        rows = []

        for user in users:
            username = user.get("username", "")
            image_id = user.get("image_id", "")
            image_name = fs.get(ObjectId(image_id)).filename if image_id else "Desconocida"
            status = is_user_active(username)

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(username, color=ft.colors.WHITE)),
                        ft.DataCell(ft.Text(image_name, color=ft.colors.WHITE)),
                        ft.DataCell(ft.Text(status, color=ft.colors.CYAN if status == "Activo" else ft.colors.RED)),
                    ]
                )
            )

        # Crear la tabla de usuarios con un estilo moderno y simplificado
        users_table = ft.DataTable(
            bgcolor="#2A2D3E",  # Fondo de la tabla
            border_radius=10,  # Bordes redondeados para suavidad
            heading_row_color=ft.colors.BLACK12,  # Color de fondo del encabezado
            data_row_color={ft.ControlState.HOVERED: "0x30FFFFFF"},  # Color al pasar el cursor
            column_spacing=50,  # Espaciado entre columnas
            columns=[
                ft.DataColumn(
                    ft.Text("Nombre de Usuario", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD)
                ),
                ft.DataColumn(
                    ft.Text("Imagen", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD)
                ),
                ft.DataColumn(
                    ft.Text("Estado", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD)
                ),
            ],
            rows=rows,
        )

        line_chart = self.generate_line_chart()
        content = ft.Row(
            [
                ft.Container(content=users_table, expand=1),
                ft.Container(content=line_chart, expand=1, margin=ft.margin.only(left=10)),
            ],
            spacing=20
        )

        return ft.Column(
            [
                stats_cards,
                ft.Divider(color=ft.colors.WHITE24),
                content
            ],
            spacing=20
        ) if self.content_shown else ft.Container()

    def toggle_dashboard(self, e):
        if not self.dashboard_active:
            self.dashboard_active = True
            self.home_active = False
            self.content_shown = True
            self.show()

    def navigate_home(self, e):
        if not self.home_active:
            self.home_active = True
            self.dashboard_active = False
            self.content_shown = False
            self.show()

    def logout(self, e):
        print("Cerrando sesión...")
        self.page.update()

