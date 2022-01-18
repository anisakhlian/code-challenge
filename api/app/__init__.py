import os
from flask import Flask, request, g
from models import db_session

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# Initialize Flask App
app = Flask(__name__)

from .documents import documents_mod
app.register_blueprint(documents_mod, url_prefix="/v1/documents")


@app.teardown_appcontext
def shutdown_session(exception=None):
    if not os.environ.get('UNITTEST'):
        db_session.remove()
