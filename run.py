# Importamos a função que vai criar nossa aplicação (faremos ela no próximo passo)
from app import create_app

# Chamamos a função para construir nossa aplicação.
app = create_app()

# Esta linha é um padrão em Python. É como perguntar:
# "Este script foi executado diretamente pelo usuário (ex: python run.py)?"
if __name__ == '__main__':
    # Se a resposta for sim, então ligue o servidor.
    # debug=True é um modo especial para desenvolvimento que reinicia o
    # servidor automaticamente quando salvamos uma alteração no código.
    app.run(debug=True)