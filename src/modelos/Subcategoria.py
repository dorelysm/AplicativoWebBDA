from config.bd import app, db, ma

class Subcategoria(db.Model):
    __tablename__ = 'Subcategoria'

    id  = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.Integer, db.ForeignKey('Categoria.id'))
    descripcion = db.Column(db.String(500))

    def __init__(self, categoria, descripcion):
        self.categoria = categoria
        self.descripcion = descripcion

with app.app_context():
    db.create_all()

class SubcategoriaSchema(ma.Schema):
    class Meta:
        fields = ('id','categoria','descripcion')