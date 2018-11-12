# import modules
from datetime import datetime

from api.__init__ import databases

# washing class model with methods
class Washing(databases.Model):
    __tablename__ = 'Washing'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(20))
    price = databases.Column(databases.Integer)
    description = databases.Column(databases.String(300))
    date_created = databases.Column(databases.DateTime, default=datetime.utcnow())
    date_modified = databases.Column(databases.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, name, price, description):
        self.name = name 
        self.price = price
        self.description = description

    def save(self):
        databases.session.add(self)
        databases.session.commit()
