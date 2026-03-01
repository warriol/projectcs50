# Help Desk Assistant 🤖⚖️✍️
#### Video Demo:  [link to Youtube video](<https://www.google.com>)
#### Description:
Proyecto Final para CS50x - Harvard University

Help Desk Assistant es una aplicación web diseñada para optimizar los flujos de trabajo en el Ministerio del Interior de Uruguay (o cualquier entorno institucional). Utiliza Inteligencia Artificial avanzada para proporcionar soporte en tres áreas críticas: asesoramiento legal normativo, corrección ortográfica técnica y asistencia basada en manuales de procedimientos internos.

# ⭐ Características Principales

- *IA Multimodal*: Selector dinámico de personalidad de IA que adapta el comportamiento de Gemini (Google AI) según la necesidad:

    1. **Asesor Legal**: Especializado en normativa y lenguaje formal.

    2. **Corrector Ortográfico**: Refina la redacción técnica y profesional.

    3. **Manual de Soporte**: Respuestas precisas basadas en una base de conocimientos privada (archivo CSV).

- *Interfaz de Chat Moderna*: Experiencia de usuario fluida con burbujas de chat diferenciadas por colores, indicadores de carga (spinners) y renderizado de Markdown para respuestas estructuradas.

- *Gestión de Conocimiento Privada*: Implementación de una arquitectura donde la base de datos de procedimientos se mantiene en una carpeta protegida en el servidor, garantizando que la información sensible no sea accesible públicamente.

- *Sistema de Usuarios Robusto*: Registro y autenticación segura con hash de contraseñas, sesiones de usuario y gestión de historial personal de consultas.

# 🛠️ Tecnologías Utilizadas

- Backend: Python 3.13 con Flask.

- Base de Datos: SQLAlchemy (ORM) con SQLite.

- IA: Google Generative AI (Modelo Gemini 2.0 Flash-lite).

- Frontend: HTML5, CSS3, Bootstrap 5 y JavaScript asíncrono (Fetch API).

- Seguridad: Werkzeug para hashing y Python-dotenv para gestión de variables de entorno.

# 📂 Estructura del Proyecto

- app.py: Lógica principal, rutas de Flask y configuración de la IA.

- models.py: Definición de los esquemas de base de datos para usuarios y mensajes.

- data/: Carpeta privada que contiene el manual de procedimientos en formato CSV.

- static/: Archivos públicos (CSS, JavaScript del chat y logos).

- templates/: Plantillas de Jinja2 para la interfaz web.

# 🚀 Instalación y Uso

- Clona el repositorio.

- Instala las dependencias: pip install -r requirements.txt.

- Crea un archivo .env y añade tu GEMINI_API_KEY.

- Inicia la aplicación: flask run.

# 💾 Comandos útiles

```bash
## verificar la version de python
python --version

## crear entorno virtual
python -m venv venv

## activar entorno virtual
.\venv\Scripts\activate

## instalar flask
pip install Flask

## manejo de sessiones y comunicación con APIS
pip install flask-session python-dotenv

## Flask-SQLAlchemy
pip install flask-sqlalchemy

## Liberia de Google
pip install -U google-generativeai

## Librería para leer archivo .env
pip install python-dotenv

# Guardar dependencias en caso de nuevas instalaciones
pip freeze > requirements.txt
```

# 🔑 API KEY de Gemini

En este caso usare Gemini como Agente de IA, para poder usarlo es necesario obtener una API Key, para ello debemos de solicitar una de forma gratuita en: https://aistudio.google.com/

Una vez obtenida hay que pegar dicha clave en el archivo .env, junto a la clave correspondiente

```bash
# reemplaza "tu_llave_aqui_sin_comillas" por la clave obtenida
GEMINI_API_KEY=tu_llave_aqui_sin_comillas
```