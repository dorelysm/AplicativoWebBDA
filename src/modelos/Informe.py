from config.bd import app, db, ma

class Informe(db.Model):
    __tablename__ = 'Informe'

    id  = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(50))

    def __init__(self, info):
        self.info = info

with app.app_context():
    db.create_all()

class InformeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'info')