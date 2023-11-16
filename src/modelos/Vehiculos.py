from config.bd import app, db, ma

class Vehiculo(db.Model):
    __tablename__ = 'Vehiculo'

    id  = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(6), unique=True)
    tipo = db.Column(db.String(50))
    capacidad = db.Column(db.Integer)
    empresa = db.Column(db.String(50))

    def __init__(self, matricula, tipo, capacidad, empresa):
        self.matricula = matricula
        self.tipo = tipo
        self.capacidad = capacidad
        self.empresa = empresa

with app.app_context():
    db.create_all()

class VehiculoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'matricula', 'tipo', 'capacidad', 'empresa')