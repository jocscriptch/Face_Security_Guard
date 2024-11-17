from bson import ObjectId
import gridfs
from mongodb.db_connection import get_database

from datetime import datetime, timedelta
import cv2
import numpy as np

# Nombre de la base de datos
DB_NAME = "FaceGuardSecurity"
db = get_database(DB_NAME)
fs = gridfs.GridFS(db)


def insert_user(username, image):
    """Inserta un nuevo usuario con su imagen en la base de datos."""
    # Verificar si el usuario ya existe
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        return None  # Retorna None si el usuario ya existe

    # Convertir la imagen en binario
    _, buffer = cv2.imencode('.png', image)
    image_id = fs.put(buffer.tobytes(), filename=f"{username}.png")

    # Crear documento de usuario
    user_data = {
        "username": username,
        "image_id": image_id,
        "access_logs": []
    }

    result = db.users.insert_one(user_data)
    return result.inserted_id  # Retorna el ID del nuevo usuario


def add_access_log(username):
    """Añade un registro de acceso al usuario especificado."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.users.update_one(
        {"username": username},
        {"$push": {"access_logs": timestamp}}
    )
    print(f"Registro de acceso añadido para el usuario: {username}")


def get_user(username):
    """Obtiene los datos de un usuario especificado."""
    user = db.users.find_one({"username": username})
    if user:
        print(f"Usuario encontrado: {user}")
    else:
        print("Usuario no encontrado.")
    return user


def get_image_by_id(image_id):
    """Obtiene la imagen de un usuario usando su ID de imagen."""
    image_binary = fs.get(ObjectId(image_id)).read()
    # Convertir de binario a imagen de OpenCV
    image_array = np.frombuffer(image_binary, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def get_total_users():
    """Obtiene el total de usuarios registrados en la base de datos."""
    total_users = db.users.count_documents({})
    return total_users


def is_user_active(username):
    """Verifica si un usuario está activo basándose en los registros de acceso."""
    user = db.users.find_one({"username": username})
    if user and user.get("access_logs"):
        # Suponemos que el usuario está activo si su último acceso fue en las últimas 5 minutos.
        last_access_time = user["access_logs"][-1]  # Tomamos el último registro de acceso
        last_access_time = datetime.strptime(last_access_time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        # Si el último acceso fue en los últimos 20 minutos, lo consideramos activo
        if now - last_access_time <= timedelta(minutes=20):
            return "Activo"
    return "Inactivo"
