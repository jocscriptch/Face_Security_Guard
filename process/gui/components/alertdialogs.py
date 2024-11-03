import flet as ft


class AlertDialogFactory:
    def __init__(self, page: ft.Page):
        self.page = page

    def show_success_dialog(self, message: str, title: str = "Operación Exitosa"):
        def close_dialog(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_500),
                    ft.Text(title, size=20, weight="bold", color=ft.colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            content=ft.Text(message, color=ft.colors.WHITE),
            actions=[
                ft.TextButton("Aceptar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.show_dialog(dlg)
        self.page.update()

    def show_warning_dialog(self, message: str, title: str = "Advertencia"):
        def close_dialog(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.Icon(ft.icons.WARNING, color=ft.colors.ORANGE_500),
                    ft.Text(title, size=20, weight="bold", color=ft.colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            content=ft.Text(message, color=ft.colors.WHITE),
            actions=[
                ft.TextButton("Aceptar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.show_dialog(dlg)
        self.page.update()

    def show_error_dialog(self, message: str, title: str = "Problema"):
        def close_dialog(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.Icon(ft.icons.ERROR, color=ft.colors.RED_500),
                    ft.Text(title, size=20, weight="bold", color=ft.colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            content=ft.Text(message, color=ft.colors.WHITE),
            actions=[
                ft.TextButton("Aceptar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.show_dialog(dlg)
        self.page.update()
