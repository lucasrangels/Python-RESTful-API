import os

class Development(object):
    """
    Configuração de variáveis de ambiente - Desenvolvimento
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Production(object):
    """
    Configurações de variáveis de ambiente - Produção
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

app_config = {
    'development': Development,
    'production': Production,
}