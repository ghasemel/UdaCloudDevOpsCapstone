from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flask.logging import create_logger
import logging
import sys

from config import Config


logging.basicConfig(filename='app.log', level=logging.DEBUG)

mode = 'test'
if len(sys.argv) > 1:
    mode = sys.argv[1]

print(f"mode: {mode}")

db_config = 'postgresql-test'
if mode == 'prod':
    db_config = 'postgresql-prod'

app = Flask(__name__)
app.config.from_object(Config(section=db_config))
db = SQLAlchemy(app)

log = create_logger(app)
log.setLevel(logging.DEBUG)
