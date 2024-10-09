from pydantic import BaseModel

from process.gui.assets.images.gui_init_image import gui_init_image_path


class ImagePaths(BaseModel):
    # main images
    init_img: str = gui_init_image_path
    #login_img: str = login_button_image_path
    #signup_img: str = signup_button_image_path

    # secondary windows
    #gui_signup_img: str = gui_signup_image_path
    #register_img: str = face_capture_image_path