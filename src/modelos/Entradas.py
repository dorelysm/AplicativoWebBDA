from config.bd import db, ma, app

class Entrada(db.Model):
    __tablename__ = 'Entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_benefactor = db.Column(db.Integer, db.ForeignKey('Benefactor.id'))
    id_subcategoria = db.Column(db.Integer, db.ForeignKey('Subcategoria.id'))
    fecha = db.Column(db.String(50))
    cantidad_peso = db.Column(db.Integer)
    cantidad_unidades = db.Column(db.Integer)
    unidad_de_medida = db.Column(db.String(50))
    vencimiento = db.Column(db.String(50))
    observaciones = db.Column(db.String(500))

    proceso_de_inventarios = db.Column(db.Boolean)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('Vehiculo.id'))
    num_factura = db.Column(db.String(50))
    ingresado_al_sistema = db.Column(db.Boolean)
    tipo = db.Column(db.String(50))
    
    num_documento_siigo = db.Column(db.Integer)
    cantidad_averiada_vencida_kg = db.Column(db.Integer)
    cantidad_buen_estado_kg = db.Column(db.Integer)
    cantidad_aprobada_kg = db.Column(db.Integer)

    def __init__(self, id_benefactor = None, id_subcategoria = None, fecha = None, 
                 cantidad_peso= None, cantidad_unidades = None, 
                 unidad_de_medida = None, vencimiento = None, 
                 observaciones = None, proceso_de_inventarios = None, 
                 id_vehiculo = None, num_factura = None, ingresado_al_sistema = None, 
                 tipo = None, num_documento_siigo = None,
                 cantidad_averiada_vencida_kg = None, cantidad_buen_estado_kg = None,
                 cantidad_aprobada_kg = None):
        #self.id = id
        self.id_benefactor = id_benefactor
        self.id_subcategoria = id_subcategoria
        self.fecha = fecha
        self.cantidad_peso = cantidad_peso
        self.cantidad_unidades = cantidad_unidades
        self.unidad_de_medida = unidad_de_medida
        self.vencimiento = vencimiento
        self.observaciones = observaciones
        self.proceso_de_inventarios = proceso_de_inventarios
        self.id_vehiculo = id_vehiculo
        self.num_factura = num_factura
        self.ingresado_al_sistema = ingresado_al_sistema
        self.tipo = tipo
        self.num_documento_siigo = num_documento_siigo
        self.cantidad_averiada_vencida_kg = cantidad_averiada_vencida_kg
        self.cantidad_buen_estado_kg = cantidad_buen_estado_kg
        self.cantidad_aprobada_kg = cantidad_aprobada_kg


with app.app_context():
    db.create_all()

class EntradaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_benefactor', 'id_subcategoria', 'fecha', 'cantidad_peso',
                  'cantidad_unidades', 'unidad_de_medida', 'vencimiento',
                  'observaciones', 'proceso_de_inventarios', 'id_vehiculo', 'num_factura',
                  'ingresado_al_sistema', 'tipo', 'num_documento_siigo',
                  'cantidad_averiada_vencida_kg', 'cantidad_buen_estado_kg', 
                  'cantidad_aprobada_kg')
