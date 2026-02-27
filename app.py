import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Message
import google.generativeai as genai
from dotenv import load_dotenv
from flask import jsonify
import csv

# Cargar variables desde el archivo .env
load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración de sesión
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Inicializar DB con la app
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Cargo el csv
basedir = os.path.abspath(os.path.dirname(__file__))
ruta_csv = os.path.join(basedir, 'data', 'train.csv')

def cargar_contexto_csv(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"CRÍTICO: El archivo {ruta_csv} no existe.")
        return ""
    
    conocimiento = ""

    try:
        with open(ruta_csv, mode='r', encoding='utf-8-sig') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                ctx = fila.get('contexto', '').strip()
                res = fila.get('respuesta', '').strip()
                if ctx and res:
                    conocimiento += f"SITUACIÓN: {ctx}\nPROCEDIMIENTO: {res}\n---\n"
        return conocimiento
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        return ""
    
base_conocimiento = cargar_contexto_csv(ruta_csv)

PROMPTS = {
    "legal": "Eres un abogado experto en derecho penal uruguayo. Responde siempre en español, utilizando un lenguaje técnico pero claro. Debes fundamentar tus respuestas con base en el Código Penal y Código de Faltas de Uruguay. Si la pregunta no está relacionada con derecho penal, indica que no puedes responder. Eres un asistente experto en normativa legal del Ministerio del Interior de Uruguay. Responde de forma técnica, formal y precisa.",
    "corrector": "Eres un profesor de lengua española con excelente ortografía y gramática, tienes como tareas: Revisarás el texto que se te envíe y harás las correcciones necesarias. Verifica que al comienzo de cada párrafo haya una sangría de 5 espacios. Entre un párrafo y el siguiente, debe haber un interlineado. Si hay texto entre comillas indica que es un pasaje textual, se espera que no hagas correcciones orográficas o gramaticales de los pasajes textuales, pero si el mismo esta escrito en minúsculas debes cambiar el texto del pasaje textual a mayúsculas. Presentarás como respuesta el texto corregido y al final una lista con las correcciones que hayas realizado",
    "manual": f"""Eres un asistente técnico experto del Ministerio del Interior. Tu única fuente de verdad es la siguiente base de conocimientos: {base_conocimiento} INSTRUCCIONES CRÍTICAS: 1. Analiza la pregunta del usuario y busca conceptos relacionados en la columna 'Situación'. 2. Si la pregunta es similar o trata sobre el mismo tema que una 'Situación', responde usando el 'Procedimiento'. 3. Puedes parafrasear la respuesta para que suene natural, pero mantén los datos técnicos exactos. 4. Si la información no está en la base de conocimientos, di: 'Lo siento, no tengo información oficial sobre ese procedimiento específico en el manual'."""
}

@app.route("/")
def index():
    # Si el usuario ya está logueado, al dashboard del chat
    if session.get("user_id"):
        return redirect("/dashboard")
    
    # Si no, mostramos la página de bienvenida con opción de login/registro
    return render_template("index.html")

# En app.py
@app.route("/register", methods=["GET", "POST"])
def register():
    # Olvidar cualquier user_id previo
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # 1. Validaciones
        if not username or not password or not confirmation:
            flash("Todos los campos son obligatorios")
            return redirect("/register")
        
        if password != confirmation:
            flash("Las contraseñas no coinciden")
            return redirect("/register")

        # 2. Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso")
            return redirect("/register")

        # 3. Crear el nuevo usuario
        hash_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hash_pw)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # 4. Iniciar sesión automáticamente
            session["user_id"] = new_user.id
            flash("¡Cuenta creada con éxito!")
            return redirect("/")
            
        except Exception as e:
            db.session.rollback()
            flash("Ocurrió un error al crear la cuenta")
            return redirect("/register")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Olvidar cualquier user_id previo
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 1. Validar que se enviaron los datos
        if not username or not password:
            flash("Debe proporcionar usuario y contraseña")
            return redirect("/login")

        # 2. Buscar al usuario en la DB
        user = User.query.filter_by(username=username).first()

        # 3. Verificar si el usuario existe y la contraseña es correcta
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Usuario o contraseña incorrectos")
            return redirect("/login")

        # 4. Recordar al usuario en la sesión
        session["user_id"] = user.id
        flash(f"¡Bienvenido de nuevo, {user.username}!")
        return redirect("/dashboard")

    # Si es GET, mostrar el formulario
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Olvidar cualquier user_id previo
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect("/login")
    
    # Consultamos el historial de mensajes de este usuario
    history = Message.query.filter_by(user_id=session["user_id"]).order_by(Message.timestamp.asc()).all()
    return render_template("dashboard.html", history=history)

@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.get_json()
    pregunta_usuario = data.get("message")
    tipo_ia = data.get("type")
    
    if not pregunta_usuario:
        return jsonify({"answer": "Error: No se recibió ninguna pregunta."}), 400

    try:
        # 1. Configurar el modelo con el prompt específico
        instruction = PROMPTS.get(tipo_ia, PROMPTS["legal"])
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash-lite", system_instruction=instruction)

        # 2. Generar la respuesta
        response = model.generate_content(pregunta_usuario)
        respuesta_ia = response.text

        # 3. Guardar en la base de datos (SQLAlchemy)
        nuevo_mensaje = Message(
            user_id=session["user_id"],
            pregunta=pregunta_usuario,
            respuesta=respuesta_ia,
            tipo_ia=tipo_ia
        )
        db.session.add(nuevo_mensaje)
        db.session.commit()

        # 4. Enviar respuesta al frontend
        return jsonify({
            "answer": respuesta_ia,
            "status": "success"
        })

    except Exception as e:
        print(f"Error con Gemini: {e}")
        return jsonify({"answer": "Lo siento, hubo un error procesando tu consulta con la IA."}), 500

    
if __name__ == "__main__":
    app.run(debug=True)