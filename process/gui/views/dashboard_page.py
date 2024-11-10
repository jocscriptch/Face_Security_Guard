import flet as ft
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
                    ft.Divider(color=ft.colors.WHITE24),
                    ft.TextButton("Cerrar Sesión", icon=ft.icons.EXIT_TO_APP, on_click=self.logout),
                ],
                spacing=10,
                expand=True
            ),
            width=200,
            bgcolor=ft.colors.BLUE_GREY_900,
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
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=8,
            alignment=ft.alignment.center
        )

    def generate_bar_chart(self):
        users = ["AndreyBV", "Cristofer", "Jocsan"]
        connections = [12, 8, 15]
        colors = [ft.colors.BLUE, ft.colors.DEEP_PURPLE, ft.colors.BLUE]

        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=connections[i],
                            width=30,
                            color=colors[i % len(colors)],
                            tooltip=f"{users[i]}: {connections[i]} conexiones"
                        ),
                    ],
                ) for i in range(len(users))
            ],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels_size=10, title=ft.Text("Usuarios Conectados")),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(users[i]))
                    for i in range(len(users))
                ],
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]),
            max_y=max(connections) + 5,
            expand=True,
        )
        return chart

    def show_dashboard(self):
        stats_cards = ft.Row(
            [
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.Text("Total Usuarios", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE),
                                ft.Text("Todos los usuarios registrados", size=12, color=ft.colors.WHITE54),
                                ft.Row([ft.Text("1,234", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), ft.Icon(ft.icons.PEOPLE, color=ft.colors.CYAN)]),
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

        vehicles_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Vehículo")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text("Van 001")), ft.DataCell(ft.Text("Van")), ft.DataCell(ft.Text("Disponible"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Truck 002")), ft.DataCell(ft.Text("Camión")), ft.DataCell(ft.Text("Mantenimiento"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Bus 003")), ft.DataCell(ft.Text("Autobús")), ft.DataCell(ft.Text("Disponible"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Car 004")), ft.DataCell(ft.Text("Coche")), ft.DataCell(ft.Text("Alquilado"))]),
            ],
        )

        bar_chart = self.generate_bar_chart()

        content = ft.Row(
            [
                ft.Container(content=vehicles_table, expand=1),
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
