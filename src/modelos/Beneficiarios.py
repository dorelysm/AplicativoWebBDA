from config.bd import app, db, ma

class Beneficiario(db.Model):
    __tablename__ = 'Beneficiario'
    num_beneficiario  = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    contacto = db.Column(db.String(50))
    direccion = db.Column(db.String(50))

    def __init__(self, nombre, contacto, direccion):
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion

with app.app_context():
    db.create_all()

class BeneficiarioSchema(ma.Schema):
    class Meta:
        fields = ('num_beneficiario', 'nombre', 'contacto', 'direccion')