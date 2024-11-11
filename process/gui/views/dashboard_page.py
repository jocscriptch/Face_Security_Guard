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

    def generate_bar_chart(self):
        # Obtener la lista de usuarios y sus conexiones
        users = db.users.find()
        user_names = []
        connection_counts = []
        colors = [ft.colors.CYAN, ft.colors.PINK, ft.colors.LIGHT_GREEN, ft.colors.ORANGE,
                  ft.colors.BLUE]  # Colores variados

        for i, user in enumerate(users):
            username = user["username"]
            num_connections = len(user["access_logs"])

            # Agregar nombre del usuario y cantidad de conexiones a las listas
            user_names.append(username)
            connection_counts.append(num_connections)

        # Crear las barras
        bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=connection_counts[i],
                        width=40,
                        color=colors[i % len(colors)],  # Asignar color cíclicamente
                        tooltip=f"{user_names[i]}: {connection_counts[i]} conexiones",
                        border_radius=4
                    )
                ]
            ) for i in range(len(user_names))
        ]

        # Configurar el gráfico de barras
        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.colors.GREY_600),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(f"{i}", color=ft.colors.GREY_400))
                    for i in range(0, max(connection_counts) + 5, 5)
                ],
                title=ft.Text("Conexiones", color=ft.colors.GREY_400)
            ),
            bottom_axis=ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=i, label=ft.Text(user_names[i], color=ft.colors.GREY_400))
                        for i in range(len(user_names))],
                title=ft.Text("Usuarios", color=ft.colors.GREY_400)
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_800, width=0.5, dash_pattern=[3, 3]),
            vertical_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_800, width=0.5, dash_pattern=[3, 3]),
            max_y=max(connection_counts) + 5,
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
        total_users = get_total_users()

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
            bgcolor="#2A2D3E",
            border_radius=10,
            heading_row_color=ft.colors.BLACK12,
            data_row_color={ft.ControlState.HOVERED: "0x30FFFFFF"},
            column_spacing=50,
            columns=[
                ft.DataColumn(ft.Text("Nombre de Usuario", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Imagen", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Estado", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD)),
            ],
            rows=rows,
        )

        bar_chart = self.generate_bar_chart()
        content = ft.Row(
            [
                ft.Container(content=users_table, expand=1),
                ft.Container(content=bar_chart, expand=1, margin=ft.margin.only(left=10)),
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

