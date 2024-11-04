from flask import Flask, render_template, url_for, redirect, flash, abort
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, DateField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from functools import wraps

# Inicialización de la app
app = Flask(__name__)
load_dotenv()

# Configuración de la base de datos y otras configuraciones
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inicialización de las extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Modelo de Rol
class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    rol_usuario = db.Column(db.String(50), nullable=False)

# Modelo de Usuario
class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.Integer, nullable=False, unique=True)
    
    roles = db.relationship('Roles', backref='usuario', uselist=False)

    # Definir la relación hacia ContenidoUsuario
    contenidosUsuario = db.relationship('ContenidoUsuario', back_populates='usuario', lazy=True)

    def get_id(self):
        return self.id_usuario

# Modelo Materia
class Materias(db.Model):
    __tablename__ = 'Materias'
    id_materia = db.Column(db.Integer, primary_key=True)
    nombre_materia = db.Column(db.String(100), nullable=False)
    nombre_profesor = db.Column(db.String(100), nullable=False)

    # Definir la relación con Modulo
    modulos = db.relationship("Modulo", back_populates="materia")

# Modelo Modulo
class Modulo(db.Model):
    __tablename__ = 'Modulo'
    id_modulo = db.Column(db.Integer, primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('Materias.id_materia', ondelete="CASCADE"), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    # Definir la relación correctamente con la clase Materia
    materia = db.relationship("Materias", back_populates="modulos")

    # Relación con Contenidos (uno a muchos)
    contenidos = db.relationship('Contenido', backref='modulo', cascade="all, delete-orphan")

# Modelo Contenido 
class Contenido(db.Model):
    __tablename__ = 'Contenido'
    id_contenido = db.Column(db.Integer, primary_key=True)
    id_modulo = db.Column(db.Integer, db.ForeignKey('Modulo.id_modulo', ondelete="CASCADE"), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    archivo_pdf = db.Column(db.String(255))  # Guarda la ruta del PDF

    # Definir la relación hacia ContenidoUsuario
    contenidosUsuario = db.relationship('ContenidoUsuario', back_populates='contenido', lazy=True)

# Modelo ContenidoUsuario (relaciona el contenido con el usuario y el estado de completado)
class ContenidoUsuario(db.Model):
    __tablename__ = 'ContenidoUsuario'
    id_contUsuario = db.Column(db.Integer, primary_key=True)
    id_contenido = db.Column(db.Integer, db.ForeignKey('Contenido.id_contenido'), nullable=False)  # Cambia 'id_contenido' por 'Contenido.id_contenido'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)  # Cambia 'id_usuario' por 'usuario.id_usuario'
    completado = db.Column(db.Boolean, default=False)
    enlace = db.Column(db.String(255), nullable=True)  # Enlace opcional

    # Relación con Usuario (muchos a uno)
    usuario = db.relationship('Usuario', back_populates='contenidosUsuario', lazy=True)
    contenido = db.relationship('Contenido', back_populates='contenidosUsuario', lazy=True)  # Asegúrate de que 'contenidosUsuario' esté en el modelo Contenido

# Modelo Calendario
class Evento(db.Model):
    __tablename__ = 'Calendario'
    id_evento = db.Column(db.Integer, primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('Materias.id_materia'))
    fecha = db.Column(db.Date)
    evento = db.Column(db.String(100))

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Declarar los formularios
class FormLogin(FlaskForm):
    dni = StringField(
        'dni',
        validators=[InputRequired(), Length(min=8, max=10, message="El DNI debe tener entre 8 y 10 dígitos")],
        render_kw={"placeholder": "DNI"}
    )
    contraseña = PasswordField(
        'contraseña',
        validators=[InputRequired(), Length(min=10, max=25)],
        render_kw={"placeholder": "Contraseña"}
    )
    submit = SubmitField('Iniciar sesión')

class FormRegistro(FlaskForm):
    dni = StringField(
        'dni',
        validators=[InputRequired(), Length(min=8, max=10, message="El DNI debe tener entre 8 y 10 dígitos")],
        render_kw={"placeholder": "DNI"}
    )
    nombre = StringField(
        'nombre',
        validators=[InputRequired(), Length(max=30)],
        render_kw={"placeholder": "Nombre"}
    )
    apellido = StringField(
        'apellido',
        validators=[InputRequired(), Length(max=30)],
        render_kw={"placeholder": "Apellido"}
    )
    email = EmailField(
        'email',
        validators=[InputRequired(), Length(max=60)],
        render_kw={"placeholder": "Email"}
    )
    contraseña = PasswordField(
        'contraseña',
        validators=[InputRequired(), Length(min=10)],
        render_kw={"placeholder": "Contraseña"}
    )
    submit = SubmitField('Registrarse')

class FormMateria(FlaskForm):
    nombre_materia = StringField(
        "Nombre de la materia",
        validators=[InputRequired(), Length(max=100)],
        render_kw={"placeholder": "Nombre de la materia"}
    )
    nombre_profesor = StringField(
        "Nombre del profesor",
        validators=[InputRequired(), Length(max=100)],
        render_kw={"placeholder": "Nombre del profesor"}
    )
    submit = SubmitField("Crear materia")

# class FormEvaluacion(FlaskForm):
#     fecha = DateField(
#         "Fecha",
#         format='%Y-%m-%d',
#         validators=[InputRequired()]
#     )
#     tipo_evaluacion = StringField(
#         "Tipo de evaluación",
#         validators=[InputRequired(), Length(max=20)],
#         render_kw={"placeholder": "examen/tarea/proyecto"}
#     )
#     descripcion = TextAreaField(
#         "Descripción",
#         validators=[InputRequired()],
#         render_kw={"placeholder": "Descripción de la evaluación"}
#     )
#     submit = SubmitField("Agregar evaluación")

# class FormEvento(FlaskForm):
#     fecha = DateField(
#         "Fecha",
#         format='%Y-%m-%d',
#         validators=[InputRequired()]
#     )
#     evento = StringField(
#         "Evento",
#         validators=[InputRequired(), Length(max=100)],
#         render_kw={"placeholder": "Nombre del evento"}
#     )
#     submit = SubmitField("Agregar evento")

# Decorador para requerir un rol específico
def rol_requerido(rol):
    def decorador(f):
        @wraps(f)
        def decorado_funcion(*args, **kwargs):
            user_rol = Roles.query.filter_by(id_usuario=current_user.id_usuario).first()
            if user_rol and user_rol.rol_usuario == rol:
                return f(*args, **kwargs)
            else:
                abort(403)
        return decorado_funcion
    return decorador

# Rutas
@app.route('/', methods=["GET", "POST"])
def iniciar_sesion():
    form = FormLogin()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(dni=form.dni.data).first()
        if user and bcrypt.check_password_hash(user.contraseña, form.contraseña.data):
            login_user(user)
            return redirect(url_for('inicio'))
        else:
            flash("DNI o contraseña inválidos")
    return render_template('iniciar_sesion.html', form=form)

@login_required
@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    return render_template("inicio.html")

@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    form = FormRegistro()
    if form.validate_on_submit():
        hashed_contraseña = bcrypt.generate_password_hash(form.contraseña.data)
        nuevo_usuario = Usuario(
            dni=form.dni.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            contraseña=hashed_contraseña
        )
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('iniciar_sesion'))
        except IntegrityError:
            db.session.rollback()
            flash('El nombre de usuario ya está en uso. Por favor elige otro.')
            return redirect(url_for('registrarse'))
    return render_template("registrarse.html", form=form)

@login_required
@app.route("/materias", methods=["POST", "GET"])
def materias():
    materias = Materias.query.all()
    form = FormMateria()
    if form.validate_on_submit():
        nueva_materia = Materias(
            nombre_materia=form.nombre_materia.data,
            nombre_profesor=form.nombre_profesor.data
        )
        db.session.add(nueva_materia)
        db.session.commit()
        flash("Materia creada con éxito.")
        return redirect(url_for("materias"))
    return render_template("materias.html", materias=materias, form=form)

@login_required
@app.route("/materia/<int:materia_id>/contenidos", methods=["GET", "POST"])
def contenidos(materia_id):
    # Obtener la materia específica
    materia = Materias.query.get_or_404(materia_id)
    
    # Obtener los módulos que pertenecen a la materia específica usando id_materia en lugar de materia_id
    modulos = Modulo.query.filter_by(id_materia=materia_id).all()
    
    # Obtener los contenidos que pertenecen a los módulos de esta materia
    contenidos = Contenido.query.filter(Contenido.id_modulo.in_([modulo.id_modulo for modulo in modulos])).all()
    
    return render_template("contenidos.html", materia=materia, contenidos=contenidos, modulos=modulos)



# @login_required
# @app.route("/materia/<int:materia_id>/evaluaciones", methods=["GET", "POST"])
# def evaluaciones(materia_id):
#     materia = Materia.query.get_or_404(materia_id)
#     form = FormEvaluacion()
#     if form.validate_on_submit():
#         nueva_evaluacion = Evaluacion(
#             id_materia=materia.id_materia,
#             fecha=form.fecha.data,
#             tipo_evaluacion=form.tipo_evaluacion.data,
#             descripcion=form.descripcion.data
#         )
#         db.session.add(nueva_evaluacion)
#         db.session.commit()
#         flash("Evaluación agregada con éxito.")
#         return redirect(url_for('evaluaciones', materia_id=materia_id))
#     evaluaciones = Evaluacion.query.filter_by(id_materia=materia.id_materia).all()
#    return render_template("evaluaciones.html", materia=materia, evaluaciones=evaluaciones, form=form)

# @login_required
# @app.route("/materia/<int:materia_id>/calendario", methods=["GET", "POST"])
# def calendario(materia_id):
#     materia = Materia.query.get_or_404(materia_id)
#     form = FormEvento()
#     if form.validate_on_submit():
#         nuevo_evento = Evento(
#             id_materia=materia.id_materia,
#             fecha=form.fecha.data,
#             evento=form.evento.data
#         )
#         db.session.add(nuevo_evento)
#         db.session.commit()
#         flash("Evento agregado con éxito.")
#         return redirect(url_for('calendario', materia_id=materia_id))
#     eventos = Evento.query.filter_by(id_materia=materia.id_materia).all()
#     return render_template("calendario.html", materia=materia, eventos=eventos, form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('iniciar_sesion'))

if __name__ == '__main__':
    app.run(debug=True)
