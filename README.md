# Mini App de Notas con Flask

Una aplicación web sencilla para crear, editar y eliminar notas. Construida con Python, Flask y SQLite.

## Características

- Crear, editar y eliminar notas.
- Autenticación básica de usuarios.
- Paginación para mostrar las notas.
- Recuperación de contraseña por correo electrónico (configurable).
- Uso de SQLite para almacenamiento local.

## Tecnologías usadas

- Python 3.x
- Flask
- Flask-Mail
- Flask-Migrate
- SQLite
- Tailwind CSS

## Instalación

1. Clonar este repositorio.

2. Crear un entorno virtual:
   python -m venv venv
   source venv/bin/activate ( En Windows: venv\Scripts\activate )

4. Instalar dependencias:
   pip install -r requirements.txt

6. Crear archivo .env con tus variables de entorno (ejemplo en .env.example)

7. Ejecuta la app con : flask run --debug

# Uso
Regístrate o inicia sesión para gestionar tus notas.

Crea, edita y elimina notas fácilmente.
Usa la función de recuperación de contraseña si la olvidas.
