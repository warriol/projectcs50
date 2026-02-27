import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Message
import google.generativeai as genai
from dotenv import load_dotenv

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

if __name__ == "__main__":
    app.run(debug=True)