from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask.logging import create_logger
import logging

from config import Config
from models import Goods

app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app)

log = create_logger(app)
log.setLevel(logging.DEBUG)


@app.route('/health')
def health_status():
    return {"status": "OK"}


@app.route('/api/v1/goods', methods=['POST'])
def add():
    """ add a new merchandise """
    if request.method == 'POST':
        merchandise = request.json
        log.debug(f"insert merchandise: {merchandise}")

        new_merchandise = Goods(
            name=merchandise["name"],
            description=merchandise["description"],
            stock=merchandise["stock"],
            price=merchandise["price"]
        )
        log.debug(f"json merchandise successfully decoded to object: {new_merchandise.json()}")

        db.session.add(new_merchandise)
        log.debug("merchandise successfully added to session")

        db.session.commit()

        log.debug(f"add merchandise with id: {new_merchandise.id}")

        return new_merchandise.json()


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
