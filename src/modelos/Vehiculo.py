from config.bd import app, db, ma

class Vehiculo(db.Model):
    __tablename__ = 'Vehiculo'

    id  = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(6), unique=True)
    conductor = db.Column(db.String(50))

    def __init__(self, matricula, conductor):
        self.matricula = matricula
        self.conductor = conductor

with app.app_context():
    db.create_all()

class VehiculoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'matricula', 'conductor')