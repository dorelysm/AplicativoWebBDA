from config.bd import db, ma, app

class Salida(db.Model):
    __tablename__ = 'Salida'
    id = db.Column(db.Integer, primary_key=True)
    id_beneficiario = db.Column(db.Integer, db.ForeignKey('Beneficiario.num_beneficiario'))
    id_entrada = db.Column(db.Integer, db.ForeignKey('Entrada.id'))
    fecha = db.Column(db.String(50))
    bodega = db.Column(db.Integer)
    cantidad_peso = db.Column(db.Integer)
    cantidad_unidades = db.Column(db.Integer)
    unidad_de_medida = db.Column(db.String(50))
    aporte_solidario = db.Column(db.Integer)
    observaciones = db.Column(db.String(500))
    tipo = db.Column(db.String(50))


    def __init__(self, id_beneficiario, id_entrada, fecha, bodega, cantidad_peso, 
                 cantidad_unidades, unidad_de_medida, aporte_solidario, observaciones,
                 tipo):
        #self.id = id
        self.id_beneficiario = id_beneficiario
        self.id_entrada = id_entrada
        self.fecha = fecha
        self.bodega = bodega
        self.cantidad_peso = cantidad_peso
        self.cantidad_unidades = cantidad_unidades
        self.unidad_de_medida = unidad_de_medida
        self.aporte_solidario = aporte_solidario
        self.observaciones = observaciones
        self.tipo = tipo

with app.app_context():
    db.create_all()

class SalidaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_beneficiario', 'id_entrada', 'fecha', 'bodega', 
                  'cantidad_peso', 'cantidad_unidades', 'unidad_de_medida', 
                  'aporte_solidario', 'observaciones','tipo')
        