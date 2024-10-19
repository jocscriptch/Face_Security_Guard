""" Aca hay herramientas para la facilitar la deteccion de rostros,
como por ejemplo, recordar el rostro de una persona, dibujar sobre el rostro, etc."""
import os
import numpy as np
import cv2
import math
import datetime
from typing import List, Tuple, Any

from process.face_processing.face_detect_models.face_detect import FaceDetectMediapipe
from process.face_processing.face_mesh_models.face_mesh import FaceMeshMediapipe


class FaceUtils:
    def __init__(self):
        # face detect
        self.face_detector = FaceDetectMediapipe()

        # face mesh
        self.face_mesh_detector = FaceMeshMediapipe()

        # face matcher

        self.angle = None

    # detect
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

    # guardar rostro
    def save_face(self, face_crop: np.ndarray, username: str, faces_path: str):
        if len(face_crop) != 0:
            if -5 < self.angle < 5:
                #faces_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f"{faces_path}/{username}.png", face_crop)
                return True

        else:
            return False



    # funciones para alinear el rostro
    def face_rotate(self, face_image: np.ndarray, angle: float, center: Tuple[int, int]):
        h, w, _ = face_image.shape
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        face_rotated = cv2.warpAffine(face_image, matrix, (w, h))
        return face_rotated

    # calcular angulo de rotacion
    def calculate_rotation_angle(self, right_eye_x: int, right_eye_y: int, left_eye_x: int, left_eye_y: int):
        delta_x = left_eye_x - right_eye_x
        delta_y = left_eye_y - right_eye_y
        angle_rad = math.atan2(delta_y, delta_x)
        angle_deg = math.degrees(angle_rad)
        angle_deg %= 360
        return angle_deg

    # alinear rostros
    def align_faces(self, face_image: np.ndarray, face_key_points: List[List[int]]):
        h, w, _ = face_image.shape

        # ojos
        right_eye_x, right_eye_y = face_key_points[0][0], face_key_points[0][1]
        left_eye_x, left_eye_y = face_key_points[1][0], face_key_points[1][1]

        # angulo
        self.angle = self.calculate_rotation_angle(right_eye_x, right_eye_y, left_eye_x, left_eye_y)
        if self.angle > 180:
            self.angle -= 360

        # centrar el rostro
        center = ((right_eye_x + left_eye_x) // 2, (right_eye_y + left_eye_y) // 2)
        aligned_face = self.face_rotate(face_image, self.angle, center)
        return aligned_face

    # funcion para dibujar y manejar estado de la captura facial
    def show_state_sign_up(self, face_image: np.ndarray, state: bool, countdown_time: int):
        if state:
            if countdown_time > 0:
                text = f"Capturando rostro en {countdown_time}..."
            else:
                text = "Capturando rostro!"

            # Mostrar el texto en la ventana
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 1)

            # Cambiar el color de la malla facial a verde
            self.face_mesh_detector.config_color((0, 255, 0))
        else:
            text = "Rostro no encontrado, mira la camara!"
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 0), 1)

            # Cambiar el color de la malla facial a rojo
            self.face_mesh_detector.config_color((255, 0, 0))
