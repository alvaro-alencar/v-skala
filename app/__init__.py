from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # AQUI ESTÁ A MUDANÇA
    from . import routes
    routes.init_app(app)
    
    return app