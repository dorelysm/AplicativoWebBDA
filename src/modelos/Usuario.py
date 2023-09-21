from flask_login import UserMixin
from config.bd import app, db, ma

class Usuario(db.Model):
    __tablename__ = 'User'

    id  = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(10), nullable=False)

    def __init__(self, email, password, nombre, cedula, rol):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.cedula = cedula
        self.rol = rol

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id','email','password', 'nombre', 'cedula', 'rol')