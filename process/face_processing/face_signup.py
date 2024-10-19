import numpy as np
import time
from typing import Tuple

from process.face_processing.face_utils import FaceUtils
from process.database.config import DataBasePaths


class FaceSignUp:
    def __init__(self):
        self.database = DataBasePaths()
        self.face_utils = FaceUtils()

        # variable que inicia la cuenta regresiva
        self.countdown_start = None

    def process(self, face_image: np.ndarray, user_code: str) -> Tuple[np.ndarray, bool, str]:
        # 1- check face detection (detectar rostro)
        check_face_detect, face_info, face_save = self.face_utils.check_face(face_image)
        if check_face_detect is False:
            self.countdown_start = None
            return face_image, False, "No se detectó ningún rostro!"

        # 2- face mesh (malla facial)
        check_face_mesh, face_mesh_info = self.face_utils.face_mesh(face_image)
        if check_face_mesh is False:
            self.countdown_start = None
            return face_image, False, "No se detectó la malla facial!"

        # 3- extract face mesh (extraer malla facial)
        face_mesh_points_list = self.face_utils.extract_face_mesh(face_image, face_mesh_info)

        # 4- check face center (verificar si el rostro está centrado)
        check_face_center = self.face_utils.check_face_center(face_mesh_points_list)

        if check_face_center:
            if self.countdown_start is None:
                # iniciar cuenta regresiva (guardar el momento en que comenzo a estar centrado el rostro)
                self.countdown_start = time.time()

            # calcular el tiempo que ha pasado desde que comenzo la cuenta regresiva
            elapsed_time = time.time() - self.countdown_start
            # calcular el tiempo restante de la cuenta regresiva
            remaining_time = max(0, 3 - int(elapsed_time))

            # Mostrar la cuenta regresiva en la ventana
            # 5- check state (verificar estado)
            self.face_utils.show_state_sign_up(face_image, state=check_face_center, countdown_time=remaining_time)

            # Si la cuenta regresiva ha terminado, llego a 0 segundos
            if remaining_time == 0:
                # 6- extract face info (extraer información del rostro)
                face_bbox = self.face_utils.extract_face_bbox(face_image, face_info)
                face_points = self.face_utils.extract_face_points(face_image, face_info)

                # 7- face crop (recortar rostro)
                face_crop = self.face_utils.face_crop(face_save, face_bbox)

                # 8- save face (guardar rostro)
                check_save_image = self.face_utils.save_face(face_crop, user_code, self.database.faces)
                return face_image, check_save_image, "Rostro guardado con éxito!"

        # Si el rostro no esta centrado, reinciar la cuenta regresiva
        else:
            self.countdown_start = None
            self.face_utils.show_state_sign_up(face_image, state=check_face_center, countdown_time=0)

        return face_image, False, "Rostro no centrado"
