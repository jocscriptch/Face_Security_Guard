# Aca hay modelos de comparacion rostros
import face_recognition as fr
from deepface import DeepFace
from typing import Tuple
import cv2
import numpy as np
import json


class FaceMatcherModels:
    def __init__(self):
        self.models = [
            "VGG-Face",
            "Facenet",
            "Facenet512",
            "OpenFace",
            "DeepFace",
            "DeepID",
            "ArcFace",
            "Dlib",
            "SFace",
            "GhostFaceNet",
        ]

    def face_matching_face_recognition_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        face1 = cv2.cvtColor(face1, cv2.COLOR_BGR2RGB)
        face2 = cv2.cvtColor(face2, cv2.COLOR_BGR2RGB)

        face_loc1 = [(0, face1.shape[0], face1.shape[1], 0)]
        face_loc2 = [(0, face2.shape[0], face2.shape[1], 0)]

        face_encoding1 = fr.face_encodings(face1, known_face_locations=face_loc1)[0]
        face_encoding2 = fr.face_encodings(face2, known_face_locations=face_loc2)

        matching = fr.compare_faces(face_encoding1, face_encoding2, tolerance=0.55)
        distance = fr.face_distance(face_encoding1, face_encoding2)

        return matching[0], distance[0]

    # funcion de reconocimiento facial modelo VGG-Face
    def face_matching_vgg_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[0])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo Facenet
    def face_matching_facenet_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[1])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo Facenet512
    def face_matching_facenet512_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[2])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo OpenFace
    def face_matching_openface_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[3])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo DeepFace
    def face_matching_deepface_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[4])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo DeepID
    def face_matching_deepid_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[5])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo ArcFace
    def face_matching_arcface_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[6])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo Dlib
    def face_matching_dlib_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[7])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo SFace
    def face_matching_sface_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[8])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0

    # funcion de reconocimiento facial modelo GhostFaceNet
    def face_matching_ghostfacenet_model(self, face1: np.ndarray, face2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face1, img2_path=face2, model_name=self.models[9])
            matching, distance = result["verified"], result["distance"]
            return matching, distance
        except:
            return False, 0.0


