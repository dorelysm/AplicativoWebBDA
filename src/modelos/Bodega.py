from config.bd import app, db, ma

class Bodega(db.Model):
    __tablename__ = 'Bodega'

    id  = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)

    def __init__(self, nombre):
        self.nombre = nombre

with app.app_context():
    db.create_all()

class BodegaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre')