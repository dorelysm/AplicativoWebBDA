from config.bd import app, db, ma

class Beneficiario(db.Model):
    __tablename__ = 'Beneficiario'
    num_beneficiario = db.Column(db.Integer, primary_key=True)
    nit_o_cc = db.Column(db.Integer, unique=True)
    nombre = db.Column(db.String(50))
    contacto = db.Column(db.String(50))
    direccion = db.Column(db.String(50))

    def __init__(self, nombre, nit_o_cc, contacto, direccion):
        self.nombre = nombre
        self.nit_o_cc = nit_o_cc
        self.contacto = contacto
        self.direccion = direccion

with app.app_context():
    db.create_all()

class BeneficiarioSchema(ma.Schema):
    class Meta:
        fields = ('num_beneficiario', 'nombre', 'nit_o_cc', 'contacto', 'direccion')