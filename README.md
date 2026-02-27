# projectcs50
#### Video Demo:  <URL HERE>
#### Description:
Sitio para realizar consultas a chats personalizados, para usarlo debe ser un usuario registrado, en caso de no serlo, tiene la opción de registrarse en el sitio.
Los usuarios registrados pueden iniciar sesión y al hacerlo verán el chat con la IA, este chat ademas del campo para escribir preguntas, tinee un selector de tipo de agente con el cual se comunciarán.
Leyes: es un agente espcializado en legislación penal uruguaya, al cual se le podrá realizar pregunats inherentes a este tema.
Ortografía: es una agente especializado en gramática y ortogradía al cual se podrá enviar un texto y este hará la correción.
Manual: es un agente especializado en un manula de usuario al cual se le podrán hace preguntas sobre la funcionalidad de un determiando programa y responderá en base al manual de usaurio.
El sitio implementa una base de datos para almacenar un historial de preguntas realizadas.


### Install
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

### API KEY de Gemini
#### En este caso usare Gemini como Agente de IA, para poder usarlo es necesario obtener una API Key, para ello debemos de solicitar una de forma gratuita en: https://aistudio.google.com/
#### Una vez obtenida hay que pegar dicha clave en el archivo .env, junto a la clave correspondiente
```bash
# reemplaza "tu_llave_aqui_sin_comillas" por la clave obtenida
GEMINI_API_KEY=tu_llave_aqui_sin_comillas
```