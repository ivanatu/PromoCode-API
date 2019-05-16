from . import db, promoapp

class Promo_code(db.Model):
    __tablename__ = 'promo_code'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True)
    event = db.Column(db.String(100))
    expiry_date = db.Column(db.DateTime)
    status = db.Column(db.String(100))
    price = db.Column(db.Float)
    radius = db.Column(db.Float)

    def __init__(self, code, event, expiry_date, status, price, radius):
        self.code = code
        self.event = event
        self.expiry_date = expiry_date
        self.status = status
        self.price = price
        self.radius = radius

    def __repr__(self):
        return '<Promo_code %r>' % self.code