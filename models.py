import uuid
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, MONEY
from config import Config

app = Flask('__main__')
app.config.from_object(Config())
db = SQLAlchemy(app)


class Goods(db.Model):
    __tablename__ = 'goods'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.VARCHAR(length=400), nullable=False)
    description = db.Column(db.Text, nullable=True)
    stock = db.Column(db.Float, nullable=False)
    price = db.Column(MONEY, nullable=False)

    # run the first time we create a new result
    def __init__(self, name, description, stock, price):
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price

    # to represent the object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

    # convert to json
    def json(self):
        return {
            "id": self.id if self.id is not None else "Null",
            "name": self.name,
            "description": self.description,
            "stock": self.stock,
            "price": self.price
        }
