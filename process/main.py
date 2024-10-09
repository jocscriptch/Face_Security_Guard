import os
import flet as ft
import logging as log
import imutils
import cv2
from PIL import Image, ImageTk

from process.gui.image_paths import ImagePaths
from process.database.config import DataBasePaths
#from process.face_processing.face_signup import FacialSignup
#from process.face_processing.face_login import FacialLogin


class GraphicalUserInterface:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Seguridad Facial"
        self.page.window_width = 1280
        self.page.window_height = 720
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Instanciar ImagePaths para obtener la ruta de la imagen
        self.images = ImagePaths()

        # Crear la interfaz
        self.main()

    def main(self):
        # Usar la imagen de fondo desde ImagePaths
        background_container = ft.Container(
            content=ft.Text(""),
            width=1280,
            height=720,
            alignment=ft.alignment.center,
            image_src=self.images.init_img,  # Imagen de fondo
            image_fit=ft.ImageFit.COVER
        )

        # Añadir el contenedor con la imagen de fondo a la página
        self.page.add(background_container)

    # Función para inicializar la app en la página de Flet
    def init_app(self):
        return self.page