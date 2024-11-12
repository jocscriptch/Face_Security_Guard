from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Obtener la URI desde la variable de entorno
uri = os.getenv("MONGODB_URI")


def get_database(db_name):
    # Devuelve la conexion de la base de datos
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Conexión exitosa a MongoDB Atlas!")
        return client[db_name]
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
