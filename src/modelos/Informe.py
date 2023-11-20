from config.bd import app, db, ma

class Informe(db.Model):
    __tablename__ = 'Informe'

    id  = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(10))
    año = db.Column(db.Integer)
    id_bodega = db.Column(db.Integer, db.ForeignKey('Bodega.id'))
    kg_entrantes = db.Column(db.Integer)
    kg_salientes = db.Column(db.Integer)

    def __init__(self, mes = None, año = None, id_bodega = None,
                 kg_entrantes = None, kg_salientes = None):
        self.mes = mes
        self.año = año
        self.id_bodega = id_bodega
        self.kg_entrantes = kg_entrantes
        self.kg_salientes = kg_salientes

with app.app_context():
    db.create_all()

class InformeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'mes', 'año', 'id_bodega', 'kg_entrantes', 'kg_salientes')