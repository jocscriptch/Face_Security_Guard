import flet as ft
from process.gui.components.buttons import ButtonFactory


class DashBoardPage:
    def __init__(self, page):
        self.page = page
        self.button_factory = ButtonFactory()

    def show(self):
        # Menú lateral con bordes redondeados y sombras
        menu_lateral = ft.Container(
            content=ft.Column(
                [
                    ft.IconButton(icon=ft.icons.HOME, icon_size=30, tooltip="Inicio"),
                    ft.IconButton(icon=ft.icons.LOCATION_ON, icon_size=30, tooltip="Ubicación"),
                    ft.IconButton(icon=ft.icons.EVENT, icon_size=30, tooltip="Calendario"),
                    ft.IconButton(icon=ft.icons.SETTINGS, icon_size=30, tooltip="Configuración"),
                    ft.IconButton(icon=ft.icons.POWER_SETTINGS_NEW, icon_size=30, tooltip="Salir"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20
            ),
            width=80,
            bgcolor=ft.colors.TEAL_800,
            padding=10,
            border_radius=ft.border_radius.all(12),  # Bordes redondeados
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.BLACK)  # Sombra
        )

        # Cuadro de búsqueda con bordes redondeados
        cuadro_busqueda = ft.Container(
            content=ft.TextField(
                hint_text="Buscar Ciudad",
                prefix_icon=ft.icons.SEARCH,
                width=400,
                border_radius=ft.border_radius.all(12)  # Bordes redondeados en el TextField
            ),
            padding=10
        )

        # Sección de contenido principal con contenedores redondeados y sombras
        seccion_principal = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configuración - Día", size=24),
                    ft.Container(
                        width=600, height=200, bgcolor=ft.colors.TEAL,
                        border_radius=ft.border_radius.all(12),
                        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK)
                    ),
                    ft.Text("Configuración - Semana", size=24),
                    ft.Container(
                        width=600, height=200, bgcolor=ft.colors.TEAL,
                        border_radius=ft.border_radius.all(12),
                        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK)
                    ),
                ],
                spacing=10
            ),
            padding=20,
            bgcolor=ft.colors.TEAL_900,
            border_radius=ft.border_radius.all(12),
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.BLACK)
        )

        # Otras ciudades con dropdown redondeado y sombra
        dropdown_ciudades = ft.Container(
            content=ft.Dropdown(
                label="Otras ciudades",
                options=[
                    ft.dropdown.Option("Lima"),
                    ft.dropdown.Option("Bogotá"),
                    ft.dropdown.Option("Buenos Aires"),
                ],
                width=200,
                border_radius=ft.border_radius.all(12)  # Bordes redondeados en el Dropdown
            ),
            padding=10,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK)
        )

        # Estructura general del dashboard
        content_row = ft.Row(
            [
                menu_lateral,  # Menú lateral ahora está en un Container con bgcolor
                ft.Column(
                    [
                        cuadro_busqueda,
                        ft.Row(
                            [
                                seccion_principal,
                                ft.Column(
                                    [
                                        ft.Text("Aspectos destacados de hoy", size=20),
                                        ft.Container(
                                            width=200, height=100, bgcolor=ft.colors.TEAL,
                                            border_radius=ft.border_radius.all(12),
                                            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK)
                                        ),
                                        ft.Container(
                                            width=200, height=100, bgcolor=ft.colors.TEAL,
                                            border_radius=ft.border_radius.all(12),
                                            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK)
                                        ),
                                        ft.Container(
                                            width=200, height=100, bgcolor=ft.colors.TEAL,
                                            border_radius=ft.border_radius.all(12),
                                            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK)
                                        ),
                                        ft.Text("Otras ciudades"),
                                        dropdown_ciudades
                                    ]
                                )
                            ],
                            spacing=20
                        )
                    ]
                )
            ],
            spacing=10
        )

        # Mostrar la vista en la página
        self.page.controls.clear()  # Limpiar la página
        self.page.add(content_row)  # Añadir el contenido
        self.page.update()  # Actualizar la página
