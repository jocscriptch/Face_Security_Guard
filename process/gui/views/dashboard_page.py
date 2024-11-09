import flet as ft

class DashBoardPage:
    def __init__(self, page: ft.Page):
        self.page = page

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
                    ft.TextButton("Dashboard", icon=ft.icons.DASHBOARD, on_click=lambda _: print("Dashboard")),
                    ft.TextButton("Vehicles", icon=ft.icons.DIRECTIONS_CAR, on_click=lambda _: print("Vehicles")),
                    ft.TextButton("Drivers", icon=ft.icons.PEOPLE, on_click=lambda _: print("Drivers")),
                    ft.TextButton("Trips", icon=ft.icons.CALENDAR_TODAY, on_click=lambda _: print("Trips")),
                    ft.TextButton("Packages", icon=ft.icons.INVENTORY, on_click=lambda _: print("Packages")),
                    ft.TextButton("Maintenance", icon=ft.icons.BUILD, on_click=lambda _: print("Maintenance")),
                    ft.TextButton("Settings", icon=ft.icons.SETTINGS, on_click=lambda _: print("Settings")),
                ],
                spacing=10,
                expand=True
            ),
            width=200,
            bgcolor=ft.colors.BLUE_GREY_900,
            padding=20
        )

        # Cabecera (con el padding envuelto en un Container)
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Dashboard", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Container(width=20),  # Espaciador en lugar de Spacer
                    ft.Container(
                        content=ft.TextField(hint_text="Search...", bgcolor=ft.colors.BLUE_GREY_800, border_radius=ft.border_radius.all(10), text_size=12),
                        width=200
                    ),
                    ft.IconButton(ft.icons.PERSON, icon_color=ft.colors.WHITE),
                ],
                alignment="center",
            ),
            padding=20,
            bgcolor=ft.colors.BLUE_GREY_800,
        )

        # Tarjetas de estadísticas
        stats_cards = ft.Row(
            [
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.Text("Total Users", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE),
                                ft.Text("All registered users", size=12, color=ft.colors.WHITE54),
                                ft.Row([ft.Text("1,234", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), ft.Icon(ft.icons.PEOPLE, color=ft.colors.CYAN)]),
                            ],
                            spacing=5
                        ),
                        padding=20,
                        bgcolor=ft.colors.BLUE_GREY_900,
                        border_radius=8
                    ),
                ),
                # Repite el código para otras tarjetas como Total Orders, Total Inventory y Revenue
            ],
            spacing=10
        )

        # Tabla de vehículos
        vehicles_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Vehicle")),
                ft.DataColumn(ft.Text("Type")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text("Van 001")), ft.DataCell(ft.Text("Van")), ft.DataCell(ft.Text("Available"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Truck 002")), ft.DataCell(ft.Text("Truck")), ft.DataCell(ft.Text("Maintenance"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Bus 003")), ft.DataCell(ft.Text("Bus")), ft.DataCell(ft.Text("Available"))]),
                ft.DataRow(cells=[ft.DataCell(ft.Text("Car 004")), ft.DataCell(ft.Text("Car")), ft.DataCell(ft.Text("Rented"))]),
            ],
        )

        # Contenedor principal
        self.page.add(
            ft.Row(
                [
                    sidebar,
                    ft.Column(
                        [
                            header,
                            stats_cards,
                            vehicles_table,
                        ],
                        expand=True
                    )
                ],
                expand=True
            )
        )
        self.page.update()  # Asegúrate de actualizar la página después de los cambios