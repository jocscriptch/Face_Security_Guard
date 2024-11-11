from pydantic import BaseModel

from process.gui.assets.images.gui_init_image import gui_init_image_path
from process.gui.assets.images.gui_register_image import gui_register_image_path
from process.gui.assets.images.liveness_verification import liveness_verification_image_path
from process.gui.assets.images.liveness_error import liveness_error_image_path
from process.gui.assets.images.sucess_liveness import sucess_liveness_image_path
from process.gui.assets.images.check import check_image_path
from process.gui.assets.images.see_cam import see_cam_image_path
from process.gui.assets.images.blinkings import blinkings_image_path
from process.gui.assets.images.init_system import init_system_image_path
from process.gui.assets.images.facial_register import facial_register_image_path
from process.gui.assets.images.facial_scan import facial_scan_image_path


class ImagePaths(BaseModel):
    # main image
    init_img: str = gui_init_image_path

    # secondary window
    register_img: str = gui_register_image_path

    # liveness verification
    liveness_verification_img: str = liveness_verification_image_path

    # liveness error
    liveness_error_img: str = liveness_error_image_path

    # sucess liveness
    sucess_liveness_img: str = sucess_liveness_image_path

    # check
    check_img: str = check_image_path

    # see cam
    see_cam_img: str = see_cam_image_path

    # blinkings
    blinkings_img: str = blinkings_image_path

    # init_system
    init_system_img: str = init_system_image_path

    # facial_register
    facial_register_img: str = facial_register_image_path

    # facial_scan
    facial_scan_img: str = facial_scan_image_path