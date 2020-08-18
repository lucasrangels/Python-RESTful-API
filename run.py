import os

from src.app import create_app

if __name__ == '__main__':

  app = create_app('development')

  # Inicializador da Aplicação
  app.run()