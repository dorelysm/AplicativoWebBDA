from config.bd import db, ma, app

class Producto_inventario(db.Model):
    __tablename__ = 'Producto_inventario'

    id  = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('Producto.id'))
    id_entrada = db.Column(db.Integer, db.ForeignKey('Entrada.id'))
    cantidad_unidades = db.Column(db.Integer)
    peso = db.Column(db.Double)
    vencimiento = db.Column(db.Date)
    cantidad_averiada_vencida = db.Column(db.Integer)
    cantidad_buen_estado = db.Column(db.Integer)
    cantidad_aprobada = db.Column(db.Integer)

    def __init__(self, id_producto = None, id_entrada= None, cantidad_unidades= None, peso= None, 
                 vencimiento= None, cantidad_averiada_vencida= None, 
                 cantidad_buen_estado= None, cantidad_aprobada= None):
        self.id_producto = id_producto
        self.id_entrada = id_entrada
        self.cantidad_unidades = cantidad_unidades
        self.peso = peso
        self.vencimiento = vencimiento
        self.cantidad_averiada_vencida = cantidad_averiada_vencida
        self.cantidad_buen_estado = cantidad_buen_estado
        self.cantidad_aprobada = cantidad_aprobada

with app.app_context():
    db.create_all()

class Producto_inventarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_producto', 'id_entrada', 'cantidad_unidades', 'peso', 
                 'vencimiento', 'cantidad_averiada_vencida', 
                 'cantidad_buen_estado', 'cantidad_aprobada')