from config.bd import app, db, ma

class Producto(db.Model):
    __tablename__ = 'Producto'

    id  = db.Column(db.Integer, primary_key=True)
    subcategoria = db.Column(db.Integer, db.ForeignKey('Subcategoria.id'))
    descripcion = db.Column(db.String(500))
    peso = db.Column(db.Integer)

    def __init__(self, subcategoria, descripcion, peso):
        self.subcategoria = subcategoria
        self.descripcion = descripcion
        self.peso = peso

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id','subcategoria','descripcion', 'peso')