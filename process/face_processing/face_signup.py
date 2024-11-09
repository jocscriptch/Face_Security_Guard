import cv2
import numpy as np
import time
from typing import Tuple

from process.face_processing.face_utils import FaceUtils
# from process.database.config import DataBasePaths
from process.gui.image_paths import ImagePaths
from mongodb.db_functions import insert_user


class FaceSignUp:
    def __init__(self, images: ImagePaths):
        # self.database = DataBasePaths()
        self.face_utils = FaceUtils()
        self.images = images
        self.countdown_start = None
        self.success_start_time = None
        self.save_image_flag = False
        self.no_blink_start_time = time.time()
        self.liveness_error_displayed = False
        self.save_image_start_time = None

        # Cargar imgs para superponer
        self.img_liveness_verification = cv2.imread(self.images.liveness_verification_img, cv2.IMREAD_UNCHANGED)
        self.img_see_cam = cv2.imread(self.images.see_cam_img, cv2.IMREAD_UNCHANGED)
        self.img_check = cv2.imread(self.images.check_img, cv2.IMREAD_UNCHANGED)
        self.img_blinkings = cv2.imread(self.images.blinkings_img, cv2.IMREAD_UNCHANGED)
        self.img_success = cv2.imread(self.images.sucess_liveness_img, cv2.IMREAD_UNCHANGED)
        self.img_error = cv2.imread(self.images.liveness_error_img, cv2.IMREAD_UNCHANGED)

    def process(self, face_image: np.ndarray, user_code: str) -> Tuple[np.ndarray, bool, str]:
        # 1- Detección de rostro
        check_face_detect, face_info, face_save = self.face_utils.check_face(face_image)
        if not check_face_detect:
            self.face_utils.blink_counter = 0
            return face_image, False, "No se detectó ningún rostro!"

        # 2- Malla facial
        check_face_mesh, face_mesh_info = self.face_utils.face_mesh(face_image)
        if not check_face_mesh:
            self.face_utils.blink_counter = 0
            return face_image, False, "No se detectó la malla facial!"

        # 3- Extraer puntos de la malla facial
        face_mesh_points_list = self.face_utils.extract_face_mesh(face_image, face_mesh_info)

        # 4- Verificar si el rostro está centrado
        check_face_center = self.face_utils.check_face_center(face_mesh_points_list)

        # Superponer imágenes
        if not self.save_image_flag:
            if self.img_liveness_verification is not None:
                face_image = self.face_utils.overlay_image(face_image, self.img_liveness_verification, 0, 0)
            if self.img_see_cam is not None:
                face_image = self.face_utils.overlay_image(face_image, self.img_see_cam, 880, 0)
            if self.img_blinkings is not None:
                face_image = self.face_utils.overlay_image(face_image, self.img_blinkings, 880, 250)
        else:
            # Mostrar imagen de éxito
            if self.img_success is not None:
                face_image = self.face_utils.overlay_image(face_image, self.img_success, 0, 0)

        if check_face_center:
            if not self.save_image_flag:
                # Mostrar imagen de check si el rostro está centrado
                if self.img_check is not None:
                    face_image = self.face_utils.overlay_image(face_image, self.img_check, 1050, 90)

                # Mostrar contador de parpadeos
                cv2.putText(face_image, f'Parpadeos: {int(self.face_utils.blink_counter)}', (1030, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Detectar parpadeos
            blink_detected = self.face_utils.detect_blink(face_mesh_points_list)

            # Dibujar rectángulo alrededor del rostro
            face_bbox = self.face_utils.extract_face_bbox(face_image, face_info)

            if self.save_image_flag:
                self.face_utils.face_mesh_detector.config_color((255, 255, 0))  # Cyan
                self.face_utils.draw_face_rectangle(face_image, face_bbox, color=(0, 255, 0))  # Verde
            else:
                self.face_utils.draw_face_rectangle(face_image, face_bbox)

            # Si se detectaron 3 parpadeos y no se ha guardado la imagen
            if self.face_utils.blink_counter >= 3 and not self.save_image_flag:
                if self.save_image_start_time is None:
                    self.save_image_start_time = time.time()
                delay = 2  # Tiempo de espera en segundos
                time_since_blinks = time.time() - self.save_image_start_time
                if time_since_blinks >= delay:
                    # Guardar el rostro en MongoDB
                    face_crop = self.face_utils.face_crop(face_save, face_bbox)
                    insert_user(user_code, face_crop)  # Usar la función insert_user
                    self.save_image_flag = True
                    self.success_start_time = time.time()
                else:
                    # Mostrar cuenta regresiva
                    countdown = int(delay - time_since_blinks) + 1
                    cv2.putText(face_image, f"Capturando rostro en {countdown} segundos...", (400, 650),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            else:
                # Reiniciar el temporizador si no hay tres parpadeos consecutivos
                self.save_image_start_time = None
        else:
            # Si el rostro no está centrado, reiniciar el contador y el temporizador
            self.face_utils.blink_counter = 0
            self.save_image_start_time = None
            cv2.putText(face_image, "Mira de frente a la camara!", (400, 600),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Verificar si han pasado 3 segundos desde que se guardó la imagen
        if self.success_start_time and (time.time() - self.success_start_time >= 3):
            return face_image, True, "Proceso completado"

        return face_image, False, "Proceso en curso"
