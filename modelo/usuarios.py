from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.now)
    # Relación con la tabla login
    login_info = db.relationship('Login', backref='perfil', uselist=False)

class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    # Relación con logins (uno a muchos)
    logins = db.relationship('Login', backref='rol_perfil', lazy=True)

class Login(db.Model, UserMixin):
    __tablename__ = 'login'
    id_login = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_rol')) # Llave foránea a tabla rol
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False) # Texto plano
    activo = db.Column(db.Boolean, default=True, nullable=False)
    def get_id(self):
        return str(self.id_login)
    @property
    def is_active(self):
        return self.activo

class Historial_Medico(db.Model):
    __tablename__ = 'historial_medico'
    id_historial = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True)
    edad = db.Column(db.Integer)
    fecha_nac = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    nombre_paciente = db.Column(db.String(100))
    antecedentes = db.Column(db.Text)
    enfermedad_actual = db.Column(db.Text)
    indicaciones = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    # Nuevos Campos Clínicos
    altura = db.Column(db.String(20))
    peso = db.Column(db.String(20))
    tension = db.Column(db.String(20))
    # Nuevos Datos Administrativos
    direccion = db.Column(db.Text)
    sexo = db.Column(db.String(10))
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    estado_cierre = db.Column(db.Boolean, default=False)

class Cita(db.Model):
    __tablename__ = 'tabla_citas'
    id_cita = db.Column('id_citas', db.Integer, primary_key=True)
    nombre_paciente = db.Column('nombres', db.String(100), nullable=False)
    apellido_paciente = db.Column('apellidos', db.String(100), nullable=False)
    cedula = db.Column(db.String(20))
    # 'fecha' es un timestamp en PostgreSQL (combina fecha y hora)
    fecha_cita = db.Column('fecha', db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default='Pendiente')
    motivo = db.Column(db.String(255))
    id_bot_sic = db.Column(db.BigInteger)


class Examen(db.Model):
    __tablename__ = 'tabla_examenes'
    id_examenes = db.Column(db.Integer, primary_key=True)
    nombre_examen = db.Column(db.String(100), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    precio = db.Column(db.Numeric(10, 2))
    descripcion = db.Column(db.Text)
    
    # Relación para obtener el nombre de la categoría fácilmente
    cat = db.relationship('Categoria', backref='examenes', lazy=True)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Factura(db.Model):
    __tablename__ = 'facturacion'
    id_factura = db.Column(db.Integer, primary_key=True)
    nombre_paciente = db.Column(db.String(150), nullable=False)
    id_examenes = db.Column(db.Integer, db.ForeignKey('tabla_examenes.id_examenes'))
    precio_final = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_facturacion = db.Column(db.DateTime, default=datetime.now)
    id_transaccion = db.Column(db.String(50)) # Para agrupar items de una misma venta
    estado_cierre = db.Column(db.Boolean, default=False)
    
    # Relación para obtener el examen vinculado
    examen = db.relationship('Examen', backref='facturas', lazy=True)

class PagoDetalle(db.Model):
    __tablename__ = 'pago_detalle'
    id_pago = db.Column(db.Integer, primary_key=True)
    id_transaccion = db.Column(db.String(50), nullable=False) # Vinculo con id_transaccion de Factura
    metodo = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    tasa_bcv = db.Column(db.Numeric(10, 4), default=1.0) # Guardar con 4 decimales
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.now)

class HorarioDisponible(db.Model):
    __tablename__ = 'horarios_disponibles'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    ocupado = db.Column(db.Boolean, default=False) # True si ya alguien agendó esa hora

    class Sessiones(db.Model):
        __tablename__ = 'sessiones'
        id_session = db.Column(db.Integer, primary_key=True)
        id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
        fecha = db.Column(db.Date, nullable=False)
        hora = db.Column(db.Time, nullable=False)
        acciones = db.Column(db.Text)
    

