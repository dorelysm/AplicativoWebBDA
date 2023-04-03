from config.bd import db, ma, app

class Entrada(db.Model):
    __tablename__ = 'Entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_benefactor = db.Column(db.Integer, db.ForeignKey('Benefactor.id'))
    id_categoria = db.Column(db.Integer, db.ForeignKey('Categoria.id'))
    fecha = db.Column(db.String(50))
    cantidad_peso = db.Column(db.Integer)
    cantidad_unidades = db.Column(db.Integer)
    unidad_de_medida = db.Column(db.String(50))
    estibas = db.Column(db.Integer)
    ubicacion = db.Column(db.String(100))
    bodega = db.Column(db.Integer)
    observaciones = db.Column(db.String(500))


    def __init__(self, id_benefactor, id_categoria, fecha, cantidad_peso, cantidad_unidades, unidad_de_medida, estibas, ubicacion, bodega, observaciones):
        #self.id = id
        self.id_benefactor = id_benefactor
        self.id_categoria = id_categoria
        self.fecha = fecha
        self.cantidad_peso = cantidad_peso
        self.cantidad_unidades = cantidad_unidades
        self.unidad_de_medida = unidad_de_medida
        self.estibas = estibas
        self.ubicacion = ubicacion
        self.bodega = bodega
        self.observaciones = observaciones

with app.app_context():
    db.create_all()

class EntradaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_benefactor', 'id_categoria', 'fecha', 'cantidad_peso', 'cantidad_unidades', 'unidad_de_medida', 'estibas', 'ubicacion', 'bodega', 'observaciones')
