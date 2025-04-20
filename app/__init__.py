from flask import Flask
from app.routes.drinks import drinks_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(drinks_bp)
    return app
