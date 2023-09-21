from config.bd import app, db, ma
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

class Usuario(db.Model):
    __tablename__ = 'User'

    id  = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(10), nullable=False)

    def __init__(self, email, password, nombre, cedula, rol):
        self.email = email
        self.set_password(password)
        self.nombre = nombre
        self.cedula = cedula
        self.rol = rol
        
    def set_password(self, password):
        # Genera el hash de la contraseña y la almacena en el campo password_hash
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Comprueba si la contraseña proporcionada coincide con el hash almacenado
        return bcrypt.check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id','email', 'nombre', 'cedula', 'rol')