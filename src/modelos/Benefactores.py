from config.bd import app, db, ma

class Benefactor(db.Model):
    __tablename__ = 'Benefactor'

    id  = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    nit = db.Column(db.Integer, unique=True)
    contacto = db.Column(db.String(50))
    direccion = db.Column(db.String(50))

    def __init__(self, nombre, nit, contacto, direccion):
        self.nombre = nombre
        self.nit = nit
        self.contacto = contacto
        self.direccion = direccion

with app.app_context():
    db.create_all()

class BenefactorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nit', 'nombre', 'contacto', 'direccion')