from config.bd import db, ma, app

class Merma(db.Model):
    __tablename__ = 'Merma'
    id = db.Column(db.Integer, primary_key=True)
    id_entrada = db.Column(db.Integer, db.ForeignKey('Entrada.id'))
    tipo = db.Column(db.String(50))
    fecha = db.Column(db.String(50))
    cantidad_peso = db.Column(db.Integer)
    cantidad_unidades = db.Column(db.Integer)
    unidad_de_medida = db.Column(db.String(50))
    observaciones = db.Column(db.String(500))
    num_doc_merma_siigo = db.Column(db.Integer)


    def __init__(self, id_entrada, tipo, fecha, cantidad_peso, 
                 cantidad_unidades, unidad_de_medida, observaciones,
                 num_doc_merma_siigo):
        #self.id = id
        self.id_entrada = id_entrada
        self.tipo = tipo
        self.fecha = fecha
        self.cantidad_peso = cantidad_peso
        self.cantidad_unidades = cantidad_unidades
        self.unidad_de_medida = unidad_de_medida
        self.observaciones = observaciones
        self.num_doc_merma_siigo = num_doc_merma_siigo
        

with app.app_context():
    db.create_all()

class MermaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_entrada', 'tipo', 'fecha', 'cantidad_peso', 
                  'cantidad_unidades', 'unidad_de_medida', 'observaciones',
                  'num_doc_merma_siigo')
        