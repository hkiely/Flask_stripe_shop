from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.Integer, index=True)
    adjustable_quantity = db.Column(db.Boolean)

    def __repr__(self):
        return '<Item {}>'.format(self.name)