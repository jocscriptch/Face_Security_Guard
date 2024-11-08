import flet as ft
from process.gui.components.buttons import ButtonFactory

class DashBoardPage:
    def __init__(self, page):
        self.page = page
        self.button_factory = ButtonFactory()

    def show(self):
        # Fondo blanco para la página
        self.page.bgcolor = ft.colors.WHITE

        # Menú lateral
        menu_lateral = ft.Container(
            content=ft.Column(
                [
                    ft.Text("FACEGUARD", size=12, color="#ffffff"),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Cerrar Sesión",
                            icon=ft.icons.CLOSE,
                            color="white",
                            bgcolor="red",
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                # Ajuste del padding para hacerlo más pequeño
                                elevation=5  # Elevación para sombra
                            ),
                            on_click=lambda e: print("Sesión cerrada")  # Acción al hacer clic
                        ),
                        width=130,  # Ajusta el ancho del botón
                        height=40,  # Ajusta el alto del botón
                        border_radius=8,
                        margin=ft.margin.only(top=500)
                    )

                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            width=150,
            bgcolor="#003366",
            padding=20
        )

        # Cuadro de búsqueda alineado en la parte superior al nivel de "FACEGUARD"
        cuadro_busqueda = ft.Container(
            content=ft.TextField(
                label="Filter user",
                prefix_icon=ft.icons.SEARCH,
                width=300,
                height=30,
                border_radius=ft.border_radius.all(8)
            ),
            padding=ft.padding.only(left=20, top=-5)  # Subir el cuadro de búsqueda ajustando el top para alinearlo mejor
        )

        # Tarjetas de usuario alineadas y con más espacio entre ellas
        user_cards = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Name User", weight="bold", color="#ffffff", text_align="center"),
                                ft.Text("src Image", color="#ffffff", text_align="center"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Alineación horizontal
                        ),
                        width=250,
                        height=150,
                        bgcolor="#003366",
                        border_radius=8,
                        padding=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color="#000000",
                            offset=ft.Offset(2, 2)
                        ),
                        margin=ft.margin.only(right=20)  # Añadir margen a cada tarjeta para mayor separación entre ellas
                    ) for _ in range(3)
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centrando las tarjetas
                spacing=30  # Espaciado adicional entre tarjetas
            ),
            padding=ft.padding.only(left=100, top=10)  # Mover las tarjetas hacia la derecha
        )

        # Tabla de usuarios centrada con columnas y filas distribuidas, expandida hacia abajo y la derecha
        user_table = ft.Container(
            content=ft.Column(
                [
                    # Cabecera de la tabla
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Name User", weight="bold", color="white", text_align="center"),
                                bgcolor="#003366",
                                alignment=ft.alignment.center,
                                padding=ft.padding.symmetric(vertical=10),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Text("Date register", weight="bold", color="white", text_align="center"),
                                bgcolor="#003366",
                                alignment=ft.alignment.center,
                                padding=ft.padding.symmetric(vertical=10),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Text("img user", weight="bold", color="white", text_align="center"),
                                bgcolor="#003366",
                                alignment=ft.alignment.center,
                                padding=ft.padding.symmetric(vertical=10),
                                expand=True
                            ),
                            ft.Container(
                                width=50  # Columna para el icono de eliminación
                            )
                        ]
                    ),
                    ft.Divider(height=1, color="grey"),  # Línea divisoria

                    # Filas de la tabla
                    ft.Row(
                        [
                            ft.Text("Cristofer", expand=True, text_align="center", color="black"),
                            ft.Text("2024-11-07 13:49:08", expand=True, text_align="center", color="black"),
                            ft.Text("process/database/faces/Cristofer.png", expand=True, text_align="center", color="black"),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color="red")  # Botón de eliminación
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10
                    ),
                    ft.Row(
                        [
                            ft.Text("Andrey", expand=True, text_align="center", color="black"),
                            ft.Text("2024-11-07 13:49:08", expand=True, text_align="center", color="black"),
                            ft.Text("process/database/faces/Andrey.png", expand=True, text_align="center", color="black"),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color="red")  # Botón de eliminación
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10
                    ),
                    ft.Row(
                        [
                            ft.Text("Jocsan", expand=True, text_align="center", color="black"),
                            ft.Text("2024-11-07 13:49:08", expand=True, text_align="center", color="black"),
                            ft.Text("process/database/faces/Jocsan.png", expand=True, text_align="center", color="black"),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color="red")  # Botón de eliminación
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10
                    ),
                    ft.Row(
                        [
                            ft.Text("Enoc", expand=True, text_align="center", color="black"),
                            ft.Text("2024-11-07 13:49:08", expand=True, text_align="center", color="black"),
                            ft.Text("process/database/faces/Enoc.png", expand=True, text_align="center", color="black"),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color="red")  # Botón de eliminación
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10
                    ),
                    # Puedes añadir más filas aquí si es necesario
                ]
            ),
            padding=ft.padding.all(20),
            bgcolor="#ffffff",
            border_radius=8,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color="#000000",
                offset=ft.Offset(2, 2)
            ),
            height=370,  # Ajuste para expandir la tabla hacia abajo
            width=1070  # Aumenta el ancho para extender la tabla más hacia la derecha
        )

        # Contenido principal
        main_content = ft.Column(
            [
                cuadro_busqueda,
                user_cards,
                user_table
            ],
            spacing=20
        )

        # Estructura general del dashboard
        content_row = ft.Row(
            [
                menu_lateral,
                main_content
            ],
            spacing=20
        )

        # Mostrar la vista en la página
        self.page.controls.clear()
        self.page.add(content_row)
        self.page.update()