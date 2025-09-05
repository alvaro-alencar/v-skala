import os

class Config:
    """
    Guarda as configurações da nossa aplicação. 
    É como um quadro de avisos central para as configurações.
    """
    # Esta é uma "senha" para a aplicação, usada pelo Flask para manter
    # os dados da sessão do usuário seguros. Pense nela como a chave de
    # um cadeado digital.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-para-desenvolvimento'