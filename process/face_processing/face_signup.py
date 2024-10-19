# Registro de personas mediante reconocimiento facial
import numpy as np
import time
from typing import Tuple

from process.face_processing.face_utils import FaceUtils
from process.database.config import DataBasePaths

import time


class FaceSignUp:
    def __init__(self):
        self.database = DataBasePaths()
        self.face_utils = FaceUtils()
        self.countdown_start = None  # Momento en que inicia la cuenta regresiva

    def process(self, face_image: np.ndarray, username: str) -> Tuple[np.ndarray, bool, str]:
        # 1- check face detection (detectar rostro)
        check_face, face_info, face_save = self.face_utils.check_face(face_image)
        if check_face is False:
            self.countdown_start = None  # Reiniciar la cuenta regresiva si no hay rostro
            return face_image, False, "No se detectó ningún rostro!"

        # 2- face mesh (malla facial)
        check_face_mesh, face_mesh_info = self.face_utils.face_mesh(face_image)
        if check_face_mesh is False:
            self.countdown_start = None  # Reiniciar la cuenta regresiva si no hay malla facial
            return face_image, False, "No se detectó la malla facial!"

        # 3- extract face mesh (extraer malla facial)
        face_mesh_points_list = self.face_utils.extract_face_mesh(face_image, face_mesh_info)

        # 4- check face center (verificar si el rostro está centrado)
        check_face_center = self.face_utils.check_face_center(face_mesh_points_list)

        # Si el rostro está centrado
        if check_face_center:
            if self.countdown_start is None:
                # Iniciar cuenta regresiva (guardar el momento en que comenzó a estar centrado)
                self.countdown_start = time.time()

            # Calcular el tiempo que ha pasado desde que comenzó la cuenta regresiva
            elapsed_time = time.time() - self.countdown_start
            remaining_time = max(0, 3 - int(elapsed_time))  # Tiempo restante de la cuenta regresiva

            # Mostrar la cuenta regresiva
            self.face_utils.show_state_sign_up(face_image, state=True, countdown_time=remaining_time)

            # Si la cuenta regresiva llegó a 0, capturar la imagen
            if remaining_time == 0:
                # 6- extract face info (extraer información del rostro)
                face_bbox = self.face_utils.extract_face_bbox(face_image, face_info)

                # extraer puntos faciales
                face_points = self.face_utils.extract_face_points(face_image, face_info)

                # 7- align faces (alinear rostros)
                face_aligned = self.face_utils.align_faces(face_save, face_points)

                # 8- face crop (recortar rostro)
                face_cropped = self.face_utils.face_crop(face_aligned, face_bbox)

                # 9- save face (guardar rostro)
                check_save_img = self.face_utils.save_face(face_cropped, username, self.database.faces)

                return face_image, check_save_img, "Rostro guardado con éxito!"

        # Si el rostro no está centrado
        else:
            # Reiniciar la cuenta regresiva
            self.countdown_start = None
            self.face_utils.show_state_sign_up(face_image, state=False, countdown_time=0)

        return face_image, False, "Rostro no centrado"