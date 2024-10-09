import os
import sys
import flet as ft
import logging as log

log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.main import GraphicalUserInterface


#app.GraphicalUserInterface()
#app.frame.mainloop()

def main(page: ft.Page):
    # Inicializar la interfaz gráfica desde el módulo main
    app = GraphicalUserInterface(page)


# Ejecutar la aplicación Flet desde este archivo
ft.app(target=main)
