import cv2
import numpy as np
import time
from typing import Tuple

from process.face_processing.face_utils import FaceUtils
# from process.database.config import DataBasePaths
from process.gui.image_paths import ImagePaths


class FaceLogIn:
    def __init__(self, images: ImagePaths):
        # self.database = DataBasePaths()
        self.face_utils = FaceUtils()
        self.images = images

        self.matcher = None
        self.user_name = None
        self.comparison = False
        self.cont_frame = 0
        self.login_success_start_time = None

        # Cargar imágenes para superponer
        self.img_liveness_verification = cv2.imread(self.images.liveness_verification_img, cv2.IMREAD_UNCHANGED)
        self.img_see_cam = cv2.imread(self.images.see_cam_img, cv2.IMREAD_UNCHANGED)
        self.img_check = cv2.imread(self.images.check_img, cv2.IMREAD_UNCHANGED)
        self.img_blinkings = cv2.imread(self.images.blinkings_img, cv2.IMREAD_UNCHANGED)
        self.img_success = cv2.imread(self.images.sucess_liveness_img, cv2.IMREAD_UNCHANGED)
        self.img_error = cv2.imread(self.images.liveness_error_img, cv2.IMREAD_UNCHANGED)

    def reset_cont_frame(self):
        self.cont_frame = 0
        self.matcher = None
        self.user_name = None
        self.comparison = False
        self.login_success_start_time = None

    def process(self, face_image: np.ndarray) -> Tuple[np.ndarray, bool, str]:
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
        if not self.matcher:
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
            if not self.matcher:
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

            if self.matcher:
                self.face_utils.face_mesh_detector.config_color((255, 255, 0))  # Cyan
                self.face_utils.draw_face_rectangle(face_image, face_bbox, color=(0, 255, 0))  # Verde
            else:
                self.face_utils.draw_face_rectangle(face_image, face_bbox)

            # Si se detectaron 3 parpadeos y no se ha realizado la comparación
            if self.face_utils.blink_counter >= 3 and not self.comparison:
                # Leer base de datos de rostros
                faces_database, names_database, info = self.face_utils.read_face_database()

                # Si no hay rostros guardados
                if len(faces_database) == 0:
                    self.face_utils.show_state_login(face_image, False)
                    return face_image, False, "No hay rostros registrados!"

                # Recortar el rostro capturado de la imagen actual
                face_crop = self.face_utils.face_crop(face_save, face_bbox)

                if face_crop is None:
                    self.face_utils.show_state_login(face_image, False)
                    return face_image, False, "No se pudo capturar el rostro."

                # Comparar rostros usando el método de comparación definido en FaceUtils
                self.matcher, self.user_name = self.face_utils.face_matching_with_antispoofing(face_crop,
                                                                                               faces_database,
                                                                                               names_database)
                if self.matcher:
                    self.login_success_start_time = time.time()
                    # Guardar registro de acceso
                    self.face_utils.user_check_in(self.user_name)
                    self.face_utils.show_state_login(face_image, True)
                else:
                    # Si no hay coincidencia
                    if self.img_error is not None:
                        face_image = self.face_utils.overlay_image(face_image, self.img_error, 0, 0)
                    self.face_utils.show_state_login(face_image, False)
                    return face_image, False, "Acceso denegado"
        else:
            # Si el rostro no está centrado, reiniciar el contador
            self.face_utils.blink_counter = 0
            cv2.putText(face_image, "Mira de frente a la camara!", (400, 600),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Verificar si han pasado 3 segundos desde que se logró el acceso
        if self.login_success_start_time and (time.time() - self.login_success_start_time >= 2):
            return face_image, True, "Acceso concedido"

        return face_image, False, "Procesando"
