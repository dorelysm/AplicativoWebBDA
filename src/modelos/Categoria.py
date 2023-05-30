from config.bd import app, db, ma

class Categoria(db.Model):
    __tablename__ = 'Categoria'

    id  = db.Column(db.Integer, primary_key=True)
    id_bodega = db.Column(db.Integer, db.ForeignKey('Bodega.id'))
    descripcion = db.Column(db.String(500))

    def __init__(self, id_bodega, descripcion):
        self.id_bodega = id_bodega
        self.descripcion = descripcion

with app.app_context():
    db.create_all()

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('id','id_bodega','descripcion')