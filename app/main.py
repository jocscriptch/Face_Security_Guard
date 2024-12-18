import os
import sys
import flet as ft
import logging as log

log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.flet_app import GraphicalUserInterface


def main(page: ft.Page):
    # Inicializar la interfaz gráfica desde el módulo main
    app = GraphicalUserInterface(page)


# Ejecutar la aplicación Flet
ft.app(target=main, assets_dir="../process/gui/assets")
