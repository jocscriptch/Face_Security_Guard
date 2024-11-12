
# Sistema de Seguridad Facial 🤖

Sistema de Seguridad Facial (Face Security Guard) es un proyecto desarrollado en Python que ofrece funcionalidades avanzadas de reconocimiento y verificación facial. El sistema permite realizar un  registro facial de usuarios y posteriormente realizar un inicio de sesión facial para autenticar la identidad del usuario, garantizando que quien inicia sesión es una persona real y no una fotografía o un robot.

## 🕹️Funcionalidades del Sistema

- **Registro Facial:** Permite el registro de usuarios en el sistema mediante el proceso de una captura facial.

- **Login Facial:** Autentica a los usuarios a través del reconocimiento facial, asegurando que la persona que intenta iniciar sesión es quien dice ser.

- **Detección de Vivacidad:** Implementación de mecanismos de liveness detection para prevenir intentos de suplantación de identidad mediante fotografías o bots.

- **Interfaz Intuitiva:** Interfaz de usuario desarrollada con [Flet](https://flet.dev/) que facilita la interacción y navegación entre las diferentes funcionalidades del sistema.

## 🗄️ Almacenamiento de Datos
El sistema utiliza [MongoDB Atlas](https://www.mongodb.com/es/atlas) para almacenar de manera segura la información de los usuarios y sus capturas faciales, garantizando escalabilidad, seguridad y rendimiento para el manejo de datos.

## 💻Requisitos de la Máquina y Sistema Operativo

Si deseas ejecutar este sistema y que funcione correctamente, es necesario contar con los siguientes requisitos en tu ordenador:

### **Hardware**

- **Procesador (CPU):**
  - **Intel:** Intel Core i3 o i5 de 10ª generación o superior.
  - **AMD:** AMD Ryzen 5 o superior.
- **Memoria RAM:** Mínimo 8 GB.
- **Tarjeta Gráfica (Opcional pero Recomendada):** GPU compatible con OpenCV para acelerar el procesamiento facial.

**Nota:** El procesamiento de reconocimiento facial consume una cantidad considerable de recursos. Contar con un procesador potente y suficiente memoria RAM garantiza un rendimiento fluido y reduce los tiempos de procesamiento.

### **Software**

- **Sistema Operativo:** Windows 10 o superior.
- **PyCharm IDE:** Este proyecto fue desarrollado en [PyCharm Community Edition 2024.2.4](https://www.jetbrains.com/pycharm/) 

- **Visual Studio 2022:**
  - **Componentes Necesarios:** Herramientas de desarrollo para C++.
- **Python:** Versión 3.11.3.
- **CMake:** Herramienta de automatización de compilación.

**Nota:** Algunas librerías utilizadas en el proyecto dependen de C++.

## Instalación y Ejecución en PyCharm

**1- Clona el repositorio:** 

 ```git clone https://github.com/jocscriptch/Face_Security_Guard.git```

**2- Configura tu entorno virutal:**

Si estas en Pycharm el mismo IDE lo realiza automaticamente o si prefieres lo puedes hacer manualmente con la siguiente instrucción: 

```python -m venv venv```

**3- Instalar las Dependencias:** 

Asegúrate de que pip esté actualizado y luego instala las dependencias listadas en requirements.txt.

```pip install --upgrade pip```

```pip install -r requirements.txt```

**4- Ejecutar el proyecto:** 

Dentro de PyCharm puedes ejecutar el proyecto de la siguiente forma:

```python app/main.py```
## Screenshots
Ventana de Inicio del Sistema
![flet_UKZzXPGVuk](https://github.com/user-attachments/assets/21a3baef-6d8d-4d82-94f7-e820d4773d90)

Ventana de Registro Facial
![flet_YQRuVho4Sr](https://github.com/user-attachments/assets/f5a2918a-44f6-46e8-848c-571fc4eb517a)

Ventana del Dashboard Administrativo
![image](https://github.com/user-attachments/assets/09a824a0-0a17-49ba-b23f-011e6a9688bf)

**Nota:** Las otras ventanas son en tiempo real utilizando la libreria de OpenCV

## Desarrolladores
<img src="https://github.com/jocscriptch.png" width="30" height="30" alt="Foto de perfil de Jocsan"> [![Jocsan Ramírez Chaves](https://img.shields.io/badge/-Jocsan%20Ramírez%20Chaves-181717?style=for-the-badge&logo=github)](https://github.com/jocscriptch)

<img src="https://github.com/CristoferBV.png" width="30" height="30" alt="Foto de perfil de Cristofer"> [![Cristofer Barrios Valverde](https://img.shields.io/badge/-Cristofer%20Barrios%20Valverde-181717?style=for-the-badge&logo=github)](https://github.com/CristoferBV)

<img src="https://github.com/AndreyBV5.png" width="30" height="30" alt="Foto de perfil de Andrey"> [![Andrey Barrios Valverde](https://img.shields.io/badge/-Andrey%20Barrios%20Valverde-181717?style=for-the-badge&logo=github)](https://github.com/AndreyBV5)

<img src="https://github.com/enoc517.png" width="30" height="30" alt="Foto de perfil de Enoc"> [![Enoc Abarca Durán](https://img.shields.io/badge/-Enoc%20Abarca%20Durán-181717?style=for-the-badge&logo=github)](https://github.com/enoc517)
