from flask import Flask
import os

def create_app():
    # Get the base directory, which is one level up from this script
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Initialize the Flask app with custom template and static folder paths
    app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'), static_folder=os.path.join(basedir, 'static'))
    from .routes import main
    app.register_blueprint(main)
    app.secret_key = 'your_secret_key_here'
    return app


