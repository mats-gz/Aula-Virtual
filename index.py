from flask import Flask, render_template, url_for, redirect, flash
# Import todo lo relacionado a BD
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
# Import CORS, para permitir solicitudes HTTP de un origen diferente (o restringir)
from flask_cors import CORS
# Import migrate para poder renderizar los modelos declarados en la carpeta models, debera iniciarse cada vez que se realice cambios en esta carpeta
from flask_migrate import Migrate
# Import todo lo relacionado al Flask-WTF y Login/Register 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email
# Import Bcrypt para la encriptación de la contraseña
from flask_bcrypt import Bcrypt
# Import lo relacionado al dotenv para cargar todo lo que esta definido en el archivo .env (.gitignore)
from dotenv import load_dotenv
import os



#Inicialización de la app
app = Flask(__name__)
load_dotenv()

#compu del negro
#Conectac on BD, los archivos estan en un usuario .gitignore, se importan con el dotenv y el os
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://51702027:nicolas07.@localhost/AulaVirtual'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key para utilizar Flask-WTF
app.config['SECRET_KEY'] = 'una_clave_secreta_aleatoria'

#compu del mati
#Conectac on BD, los archivos estan en un usuario .gitignore, se importan con el dotenv y el os
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key para utilizar Flask-WTF
    #app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Añadirle propiedades a la aplicación
db = SQLAlchemy(app)
migrate = Migrate(app, db)  
CORS(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Declarar función para obtener el ID del usuario que se inició en el form del Login, para evitar que inicie sesion devuelta si ingresa a una ruta con login_required
@login_manager.user_loader
def user_loader(id_usuario):
    return Usuario.query.get(int(id_usuario))


# Definir modelos
# Modelo Rol
class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    rol_usuario = db.Column(db.String(50), nullable=False)

# Modelo Usuario
class Usuario(db.Model, UserMixin):
    __tablename__ = "Usuario"
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.Integer, nullable=False, unique=True)

    def get_id(self):
        return self.id_usuario  # Devuelve el ID del usuario

# Modelo Curso
class Curso(db.Model):
    __tablename__ = 'Cursos'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(50), nullable=False)

# Modelo Materia
class Materia(db.Model):
    __tablename__ = 'Materias'
    id_materia = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('Cursos.id_curso'))
    nombre_materia = db.Column(db.String(100), nullable=False)
    contenidos = db.relationship('Contenido', backref='materia', lazy=True)

# Modelo Contenido
class Contenido(db.Model):
    __tablename__ = 'Contenidos'
    id_contenido = db.Column(db.Integer, primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('Materias.id_materia'))
    tipo_contenido = db.Column(db.Enum('teórico', 'práctico'), nullable=False)
    descripcion = db.Column(db.Text)

# Modelo Evaluación
class Evaluacion(db.Model):
    __tablename__ = 'Evaluaciones'
    id_evaluacion = db.Column(db.Integer, primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('Materias.id_materia'))
    fecha = db.Column(db.Date)
    tipo_evaluacion = db.Column(db.Enum('examen', 'tarea', 'proyecto'), nullable=False)
    descripcion = db.Column(db.Text)

# Modelo Calendario
class Evento(db.Model):
    __tablename__ = 'Calendario'
    id_evento = db.Column(db.Integer, primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('Materias.id_materia'))
    fecha = db.Column(db.Date)
    evento = db.Column(db.String(100))


# Declarar los forms
# Form Login
class FormLogin(FlaskForm):
    dni = StringField(
        'dni', 
        validators=[ InputRequired(), Length(min=8, max=10, message="El DNI debe tener entre 8 y 10 dígitos")], 
        render_kw={"placeholder": "dni"}
    )
    
    contraseña = PasswordField(
        'contraseña', 
        validators=[InputRequired(), Length(min=10, max=25)], 
        render_kw={"placeholder": "contraseña"}
    )
    
    submit = SubmitField('Iniciar sesión')

# Form Register
class FormRegistro(FlaskForm):
    dni = StringField(
        'dni', 
        validators=[ InputRequired(), Length(min=8, max=10, message="El DNI debe tener entre 8 y 10 dígitos")], 
        render_kw={"placeholder": "dni"}
    )

    nombre = StringField(
        'nombre', 
        validators=[ InputRequired(), Length(max=30)], 
        render_kw={"placeholder": "nombre"}
    )

    apellido = StringField(
        'apellido', 
        validators=[ InputRequired(), Length(max=30)], 
        render_kw={"placeholder": "apellido"}
    )

    email = EmailField(
        'email', 
        validators=[ InputRequired(), Length(max=60)], 
        render_kw={"placeholder": "email"}
    )

    contraseña = PasswordField(
        'contraseña', 
        validators=[ InputRequired(), Length(min=10)], 
        render_kw={"placeholder": "contraseña"}
    )

    submit = SubmitField('Iniciar sesión')


# Declaración de rutas
@app.route('/', methods = ["GET", "POST"])
def inicio():
    form = FormLogin()

    # Una vez que el usuario ha ingresado el formulario, validarlo
    if form.validate_on_submit():
        # Obtener el primer DNI que coincida con el ingresado en el form
        user = Usuario.query.filter_by(dni=form.dni.data).first()  
        
        # Asegurarse que el user y la contraseña coincidan con lo que esta en la BD, la contraseña estaria encriptada gracias a Bcrypt
        if user and bcrypt.check_password_hash(user.contraseña, form.contraseña.data):
            login_user(user)
            return redirect(url_for('mostrar_cursos'))
        else:
            flash("DNI o contraseña inválidos")  

    return render_template('inicio.html', form=form)

@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
    form = FormRegistro()

    # Una vez que el usuario ha ingresado el formulario, validarlo
    if form.validate_on_submit():
        # Encriptar la contraseña ingresada
        hashed_contraseña = bcrypt.generate_password_hash(form.contraseña.data)

        # Crear un nuevo usuario con los datos del formulario
        nuevo_usuario = Usuario(
            dni = form.dni.data,
            nombre = form.nombre.data,
            apellido = form.apellido.data,
            email = form.email.data,
            contraseña = hashed_contraseña
        )

        # Agregar el nuevo usuario a la base de datos, al menos que ocurra el error de integridad, es decir, de duplicar un usuario ya existente
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
        except IntegrityError: # error de integridad (usuario ya existe)
            db.session.rollback() # Rollback de la transacción, para que no se agregue el usuario a la BD
            flash('El nombre de usuario ya está en uso. Por favor elige otro.')
            return redirect(url_for('registrarse'))
        
        return redirect(url_for('inicio'))
    
    return render_template("registrarse.html", form=form)


@app.route('/cursos')
@login_required
def mostrar_cursos():
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos)

# Ruta para mostrar Materias
@app.route('/materias/<int:id_curso>')
@login_required
def mostrar_materias(id_curso):
    materias = Materia.query.filter_by(id_curso=id_curso).all()
    return render_template('materias.html', materias=materias)

@app.route('/materias/<int:id_materia>/contenidos')
@login_required
def mostrar_contenidos(id_materia):
    contenidos = Contenido.query.filter_by(id_materia=id_materia).all()
    materia = Materia.query.get_or_404(id_materia)  # Obtener la materia por ID
    return render_template('contenidos.html', contenidos=contenidos, materia=materia)

if __name__ == "__main__":
    app.run(debug=True)