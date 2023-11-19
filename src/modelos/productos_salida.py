from config.bd import db, ma, app

class Producto_salida(db.Model):
    __tablename__ = 'Producto_salida'

    id  = db.Column(db.Integer, primary_key=True)
    id_producto_inventario = db.Column(db.Integer, db.ForeignKey('Producto_inventario.id'))
    id_salida = db.Column(db.Integer, db.ForeignKey('Salida.id'))
    cantidad_unidades = db.Column(db.Integer)
    peso = db.Column(db.Double)
    aporte_solidario = db.Column(db.Integer)

    def __init__(self, id_producto_inventario = None, id_salida = None, 
                 cantidad_unidades= None, peso= None, 
                 aporte_solidario = None):
        self.id_producto_inventario = id_producto_inventario
        self.id_salida = id_salida
        self.cantidad_unidades = cantidad_unidades
        self.peso = peso
        self.aporte_solidario = aporte_solidario

with app.app_context():
    db.create_all()

class Producto_salidaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_producto_inventario', 'id_salida', 'cantidad_unidades', 
                  'peso', 'aporte_solidario')