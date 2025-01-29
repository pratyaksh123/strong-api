from flask import Flask
from .routes import api  # Import blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)  # Register routes
    return app
