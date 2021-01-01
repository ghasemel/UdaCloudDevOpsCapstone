""" This file will initialize our Flask app and all fixtures we need """
import pytest

from goods import app as flask_app, db
from models import Goods


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="module", autouse=True)
def clean_db():
    print("clean goods table before test")
    Goods.query.delete()
    db.session.commit()
