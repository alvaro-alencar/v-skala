from flask import Flask
from config import Config

def create_app(config_class=Config):
    """
    Application Factory: cria e configura a instância da aplicação Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Importa nosso blueprint do arquivo de rotas
    from .routes import main as main_blueprint
    
    # Registra o blueprint na aplicação.
    # Neste momento, o Flask aprende sobre todas as rotas definidas no blueprint.
    app.register_blueprint(main_blueprint)
    
    # Retorna a aplicação configurada e pronta para rodar
    return app