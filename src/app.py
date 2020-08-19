from flask import Flask

from .models import db
from .config import app_config
from .views.PlanetView import planet_api as planet_blueprint


def create_app(env_name):
    """
    Método para criação da aplicação
    """

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    db.init_app(app)

    app.register_blueprint(planet_blueprint, url_prefix='/api/v1/planetas')

    @app.route('/', methods=['GET'])
    def index():
        """
        Endpoint
        """

    return app