from config.bd import app, db, ma

class Usuario(db.Model):
    __tablename__ = 'User'

    id  = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, email, password):
        self.email = email
        self.password = password

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id','email','password')