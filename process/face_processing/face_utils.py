""" Aca hay herramientas para la facilitar la deteccion de rostros,
como por ejemplo, recordar el rostro de una persona, dibujar sobre el rostro, etc."""
import os
import numpy as np
import cv2
import datetime
from typing import List, Tuple, Any

from process.face_processing.face_detect_models.face_detect import FaceDetectMediapipe
from process.face_processing.face_mesh_models.face_mesh import FaceMeshMediapipe
from process.face_processing.face_matcher_models.face_matcher import FaceMatcherModels


class FaceUtils:
    def __init__(self):
        # face detect
        self.face_detector = FaceDetectMediapipe()
        # face mesh
        self.face_mesh_detector = FaceMeshMediapipe()
        # face matcher
        self.face_matcher = FaceMatcherModels()

        # variables
        self.angle = None
        self.face_db = []
        self.face_names = []
        self.distance: float = 0.0
        self.matching: bool = False
        self.user_registered = False

        self.blink_counter = 0
        self.blink_detected = False
        self.EAR_THRESHOLD = 0.21

        # Número de frames consecutivos que el EAR está por debajo del umbral
        self.EAR_CONSEC_FRAMES = 3
        self.frame_counter = 0

    # detect
    def compute_ear(self, eye_points):
        # Calcular distancias entre puntos verticales y horizontales del ojo
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        EAR = (A + B) / (2.0 * C)
        return EAR

    def detect_blink(self, face_points: List[List[int]]) -> bool:
        if len(face_points) != 468:
            return False

        # Índices de los puntos del ojo izquierdo y derecho
        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]

        # Obtener los puntos de los ojos
        left_eye = np.array([face_points[i][1:] for i in left_eye_indices])
        right_eye = np.array([face_points[i][1:] for i in right_eye_indices])

        # Calcular el EAR para cada ojo
        left_EAR = self.compute_ear(left_eye)
        right_EAR = self.compute_ear(right_eye)

        EAR = (left_EAR + right_EAR) / 2.0

        # Umbral para considerar que el ojo está cerrado
        EYE_CLOSED_THRESHOLD = 0.21  # Ajusta este valor según tus pruebas

        # Detección de parpadeo
        if EAR < EYE_CLOSED_THRESHOLD:
            if not self.blink_detected and self.blink_counter < 3:
                self.blink_counter += 1
                self.blink_detected = True
        else:
            self.blink_detected = False

        return self.blink_detected

    def overlay_image(self, background, overlay, x, y):
        # Superpone una imagen sobre el fondo en la posición (x, y)
        h, w = overlay.shape[:2]
        if y + h > background.shape[0] or x + w > background.shape[1]:
            return background

        if overlay.shape[2] == 4:
            # Overlay con canal alfa
            alpha_overlay = overlay[:, :, 3] / 255.0
            alpha_background = 1.0 - alpha_overlay
            for c in range(0, 3):
                background[y:y + h, x:x + w, c] = (alpha_overlay * overlay[:, :, c] +
                                                   alpha_background * background[y:y + h, x:x + w, c])
        else:
            # Overlay sin canal alfa
            background[y:y + h, x:x + w] = overlay

        return background

    def draw_face_rectangle(self, face_image: np.ndarray, face_bbox: List[int],
                            color: Tuple[int, int, int] = (0, 165, 255)):
        # Color naranja en BGR
        x1, y1, xf, yf = face_bbox
        cv2.rectangle(face_image, (x1, y1), (xf, yf), color, 2)

    def check_face(self, face_image: np.ndarray) -> Tuple[bool, Any, np.ndarray]:
        face_save = face_image.copy()
        check_face, face_info = self.face_detector.face_detect_mediapipe(face_image)
        return check_face, face_info, face_save

    def extract_face_bbox(self, face_image: np.ndarray, face_info: Any):
        h_img, w_img, _ = face_image.shape
        bbox = self.face_detector.extract_face_bbox_mediapipe(w_img, h_img, face_info)
        return bbox

    def extract_face_points(self, face_image: np.ndarray, face_info: Any):
        h_img, w_img, _ = face_image.shape
        face_points = self.face_detector.extract_face_points_mediapipe(h_img, w_img, face_info)
        return face_points

    # face mesh
    def face_mesh(self, face_image: np.ndarray) -> Tuple[bool, Any]:
        check_face_mesh, face_mesh_info = self.face_mesh_detector.face_mesh_mediapipe(face_image)
        return check_face_mesh, face_mesh_info

    def extract_face_mesh(self, face_image: np.ndarray, face_mesh_info: Any) -> List[List[int]]:
        face_mesh_points_list = self.face_mesh_detector.extract_face_mesh_points(face_image, face_mesh_info, viz=True)
        return face_mesh_points_list

    def check_face_center(self, face_points: List[List[int]]) -> bool:
        check_face_center = self.face_mesh_detector.check_face_center(face_points)
        return check_face_center

    # recordar rostro
    def face_crop(self, face_image: np.ndarray, face_bbox: List[int]) -> np.ndarray:
        h, w, _ = face_image.shape
        offset_x, offset_y = int(w * 0.025), int(h * 0.025)
        x1, y1, xf, yf = face_bbox
        x1, y1, xf, yf = x1 - offset_x, y1 - (offset_y * 4), xf + offset_x, yf
        return face_image[y1:yf, x1:xf]

    # guardar rostro (revisar si funcina)
    def save_face(self, face_crop: np.ndarray, user_code: str, path: str):
        if len(face_crop) != 0:
            cv2.imwrite(f"{path}/{user_code}.png", face_crop)
            return True

        else:
            return False

    # maneja estado del registro facial
    def show_state_sign_up(self, face_image: np.ndarray, state: bool, countdown_time: int):
        if state:
            if countdown_time > 0:
                text = f"Capturando rostro en {countdown_time} segundos..."

            else:
                text = "Capturando Rostro!"

            # Mostrar el texto en la imagen de la ventana
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 1)

            # cambiar el color de la malla facial a verde
            self.face_mesh_detector.config_color((0, 255, 0))

        else:
            text = "Rostro no encontrado, mira la camara!"
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255), 1)

            # cambiar el color de la malla facial a rojo
            self.face_mesh_detector.config_color((0, 0, 255))

    # maneja estado del inicio de sesion
    def show_state_login(self, face_image: np.ndarray, state: bool):
        if state:
            text = 'Rostro Aprobado, ingresando...'
            color = (0, 255, 0)  # Verde
        elif state is None:
            text = 'Verificando Rostro, mira la camara!'
            color = (255, 255, 0)  # Cyan
        elif state is False:
            # Si no hay rostros registrados,
            text = 'Lo sentimos, debes registrarse!'
            color = (0, 0, 255)  # Rojo

        size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
        dim, baseline = size_text[0], size_text[1]
        cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0), cv2.FILLED)
        cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, color, 1)
        self.face_mesh_detector.config_color(color)

    # leer base de datos
    def read_face_database(self, database_path: str) -> Tuple[List[np.ndarray], List[str], str]:
        self.face_db: List[np.ndarray] = []
        self.face_names: List[str] = []

        for file in os.listdir(database_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(database_path, file)
                img_read = cv2.imread(img_path)
                if img_read is not None:
                    self.face_db.append(img_read)
                    self.face_names.append(os.path.splitext(file)[0])

        return self.face_db, self.face_names, f'Comparando {len(self.face_db)} rostros!'

    # comparar rostros funciona perfecto
    def face_matching(self, current_face: np.ndarray, face_db: List[np.ndarray], name_db: List[str]) -> Tuple[
        bool, str]:
        user_name: str = ''
        for idx, face_img in enumerate(face_db):
            self.matching, self.distance = self.face_matcher.face_matching_facenet512_model(current_face, face_img)
            print(f'Validando rostro con: {name_db[idx]}')
            print(f'matching: {self.matching} distance: {self.distance}')
            if self.matching:
                user_name = name_db[idx]
                return self.matching, user_name
        return False, 'Rostro Desconocido!'

    # registrar usuario y guardar fecha y hora
    def user_check_in(self, user_name: str, user_path: str):
        if not self.user_registered:
            now = datetime.datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            user_file_path = os.path.join(user_path, f"{user_name}.txt")
            with open(user_file_path, "a") as user_file:
                user_file.write(f'\nAcesso autorizado: {date_time}\n')

            self.user_registered = True
