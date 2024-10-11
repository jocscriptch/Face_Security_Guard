from pydantic import BaseModel
import flet as ft

# mapper las fuentes

pattanakarn_font_light_path = "process/gui/assets/fonts/pattanakarn_font_family/PattanakarnLight.ttf"
pattanakarn_font_regular_path = "process/gui/assets/fonts/pattanakarn_font_family/PattanakarnRegular.ttf"
pattanakarn_font_medium_path = "process/gui/assets/fonts/pattanakarn_font_family/PattanakarnMedium.ttf"
pattanakarn_font_semibold_path = "process/gui/assets/fonts/pattanakarn_font_family/PattanakarnSemiBold.ttf"
pattanakarn_font_bold_path = "process/gui/assets/fonts/pattanakarn_font_family/PattanakarnBold.ttf"
pattanakarn_font_extrabold_path = "process/gui/assets/fonts/pattanakarn_font_family/PattanakarnExtraBold.ttf"


class FontPaths(BaseModel):
    pattanakarn_light: str = pattanakarn_font_light_path
    pattanakarn_regular: str = pattanakarn_font_regular_path
    pattanakarn_medium: str = pattanakarn_font_medium_path
    pattanakarn_semibold: str = pattanakarn_font_semibold_path
    pattanakarn_bold: str = pattanakarn_font_bold_path
    pattanakarn_extrabold: str = pattanakarn_font_extrabold_path


def register_fonts(page: ft.Page, fonts: FontPaths):
    page.fonts = \
        {
            "PattaLight": fonts.pattanakarn_light,
            "PattaRegular": fonts.pattanakarn_regular,
            "PattaMedium": fonts.pattanakarn_medium,
            "PattaSemiBold": fonts.pattanakarn_semibold,
            "PattaBold": fonts.pattanakarn_bold,
            "PattaExtraBold": fonts.pattanakarn_extrabold,
        }
