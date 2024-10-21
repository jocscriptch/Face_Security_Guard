import numpy as np
from process.face_processing.face_utils import FaceUtils
from process.database.config import DataBasePaths


class FaceLogIn:
    def __init__(self):
        self.face_utils = FaceUtils()
        self.database = DataBasePaths()

        self.matcher = None
        self.comparison = False
        self.cont_frame = 0

    def reset_cont_frame(self):
        self.cont_frame = 0

    def process(self, face_image: np.ndarray):
        # 1- check face detection (detectar rostro)
        check_face_detect, face_info, face_save = self.face_utils.check_face(face_image)
        # cv2.imshow("face_save", face_save)
        if check_face_detect is False:
            return face_image, self.matcher, "No se detectó ningún rostro!"

        # 2- face mesh (malla facial)
        check_face_mesh, face_mesh_info = self.face_utils.face_mesh(face_image)
        if check_face_mesh is False:
            return face_image, self.matcher, "No se detectó la malla facial!"

        # 3- extract face mesh (extraer malla facial)
        face_mesh_points_list = self.face_utils.extract_face_mesh(face_image, face_mesh_info)

        # 4- check face center (verificar si el rostro está centrado)
        check_face_center = self.face_utils.check_face_center(face_mesh_points_list)

        # 8- read database (leer base de datos)
        faces_database, names_database, info = self.face_utils.read_face_database(self.database.faces)

        # Sino hay rostros guardados
        if len(faces_database) == 0:
            self.face_utils.show_state_login(face_image, False)
            return face_image, self.matcher, ""

        # 5- show state login (mostrar estado de inicio de sesión)
        self.face_utils.show_state_login(face_image, state=self.matcher)

        if check_face_center:
            # 6- extract face info (extraer información del rostro)
            self.cont_frame += 1
            print(self.cont_frame)
            if self.cont_frame == 48:
                face_bbox = self.face_utils.extract_face_bbox(face_image, face_info)
                face_points = self.face_utils.extract_face_points(face_image, face_info)

                # 7- face crop (recortar rostro)
                face_crop = self.face_utils.face_crop(face_save, face_bbox)

                if not self.comparison and self.matcher is None:
                    self.comparison = True
                    # 9- compare faces (comparar rostros)
                    self.matcher, user_name = self.face_utils.face_matching(face_crop, faces_database, names_database)

                    if self.matcher:
                        # 10- save data & time (guardar datos y hora)
                        self.face_utils.user_check_in(user_name, self.database.users)
                        return face_image, self.matcher, "Acceso de Usuario Aprobado"
                    else:
                        self.face_utils.show_state_login(face_image, False)
                        return face_image, self.matcher, ""
            else:
                return face_image, self.matcher, "No se detectó ningún rostro!"
        else:
            return face_image, self.matcher, "Rostro no Centrado"
