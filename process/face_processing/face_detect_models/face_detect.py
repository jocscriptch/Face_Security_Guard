import numpy as np
import mediapipe as mp
import cv2
from typing import Any, Tuple


class FaceDetectMediapipe:
    def __init__(self):
        # mediapipe
        self.object_face_mp = mp.solutions.face_detection
        self.face_detector_mp = self.object_face_mp.FaceDetection(min_detection_confidence=0.7, model_selection=1)
        self.bbox = []
        self.face_points = []

    def face_detect_mediapipe(self, face_image: np.ndarray) -> Tuple[bool, Any]:
        rgb_image = face_image.copy()
        rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)

        faces = self.face_detector_mp.process(rgb_image)
        if faces.detections is None:
            return False, faces
        else:
            return True, faces

    def extract_face_bbox_mediapipe(self, width_img: int, height_img: int, face_info: Any):
        self.bbox = []
        for face in face_info.detections:
            bbox = face.location_data.relative_bounding_box
            x1, y1, w_face, h_face = bbox.xmin, bbox.ymin, bbox.width, bbox.height
            x1, y1, w_face, h_face = int(x1 * width_img), int(y1 * height_img), int(w_face * width_img), int(h_face * height_img)
            xf, yf = x1 + w_face, y1 + h_face

            x1 = max(0, x1)
            y1 = max(0, y1)
            xf = min(width_img, xf)
            yf = min(height_img, yf)

            self.bbox = [x1, y1, xf, yf]
        return self.bbox

    def extract_face_points_mediapipe(self, width_img: int, height_img: int, face_info: Any):
        self.face_points = []
        for face in face_info.detections:
            key_points = face.location_data.relative_keypoints
            for i, points in enumerate(key_points):
                x, y = int(points.x * width_img), int(points.y * height_img)
                self.face_points.append([x, y])

        return self.face_points