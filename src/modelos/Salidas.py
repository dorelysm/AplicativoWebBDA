from config.bd import db, ma, app

class Salida(db.Model):
    __tablename__ = 'Salida'
    id = db.Column(db.Integer, primary_key=True)
    id_beneficiario = db.Column(db.Integer, db.ForeignKey('Beneficiario.num_beneficiario'))
    fecha = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    aporte_solidario = db.Column(db.Integer)
    
    ingresado_siigo = db.Column(db.String(1)) #Cambiar por Boolean
    num_doc_siigo = db.Column(db.Integer)
    observaciones = db.Column(db.String(500))

    def __init__(self, id_beneficiario, fecha, tipo, aporte_solidario, 
                 ingresado_siigo, num_doc_siigo, observaciones):
        #self.id = id
        self.id_beneficiario = id_beneficiario
        self.fecha = fecha
        self.tipo = tipo
        self.aporte_solidario = aporte_solidario
        self.ingresado_siigo = ingresado_siigo
        self.num_doc_siigo = num_doc_siigo
        self.observaciones = observaciones
        
with app.app_context():
    db.create_all()

class SalidaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_beneficiario', 'fecha', 'tipo',
                  'aporte_solidario', 'ingresado_siigo', 'num_doc_siigo', 'observaciones')
        