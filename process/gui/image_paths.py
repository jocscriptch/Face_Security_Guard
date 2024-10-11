from pydantic import BaseModel

from process.gui.assets.images.gui_init_image import gui_init_image_path
from process.gui.assets.images.gui_register_image import gui_register_image_path


#from process.gui.assets.images.register_button import register_button_path

class ImagePaths(BaseModel):
    # main image
    init_img: str = gui_init_image_path

    # secondary window
    register_img: str = gui_register_image_path
