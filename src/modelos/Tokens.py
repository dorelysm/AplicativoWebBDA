from config.bd import app, db, ma

class Token(db.Model):
    __tablename__ = 'Token'

    id  = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))

    def __init__(self, token):
        self.token = token

with app.app_context():
    db.create_all()

class TokenSchema(ma.Schema):
    class Meta:
        fields = ('id','token')