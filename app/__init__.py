from flask import Flask
from .db import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_mapping (
        DATABASE="app/e-learning_project_dk.db"
    )

    init_app(app)
    return app