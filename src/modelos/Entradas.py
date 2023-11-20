from config.bd import db, ma, app

class Entrada(db.Model):
    __tablename__ = 'Entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_benefactor = db.Column(db.Integer, db.ForeignKey('Benefactor.id'))
    #fecha = db.Column(db.Date)
    fecha = db.Column(db.String(10))
    observaciones = db.Column(db.String(500))

    proceso_de_inventarios = db.Column(db.String(1)) #Cambiar por Boolean
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('Vehiculo.id'))
    num_factura = db.Column(db.String(50))
    ingresado_al_sistema = db.Column(db.String(1)) #Cambiar por Boolean
    tipo = db.Column(db.String(50))
    num_documento_siigo = db.Column(db.Integer)
    
    peso = db.Column(db.Integer)

    def __init__(self, id_benefactor = None, fecha = None,
                 observaciones = None, proceso_de_inventarios = None, 
                 id_vehiculo = None, num_factura = None, ingresado_al_sistema = None, 
                 tipo = None, num_documento_siigo = None, peso = 0):
        #self.id = id
        self.id_benefactor = id_benefactor
        self.fecha = fecha
        self.observaciones = observaciones
        self.proceso_de_inventarios = proceso_de_inventarios
        self.id_vehiculo = id_vehiculo
        self.num_factura = num_factura
        self.ingresado_al_sistema = ingresado_al_sistema
        self.tipo = tipo
        self.num_documento_siigo = num_documento_siigo
        self.peso = peso

with app.app_context():
    db.create_all()

class EntradaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_benefactor', 'fecha', 'observaciones', 
                  'proceso_de_inventarios', 'id_vehiculo', 'num_factura',
                  'ingresado_al_sistema', 'tipo', 'num_documento_siigo', 'peso')
