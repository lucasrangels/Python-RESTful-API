from flask_sqlalchemy import SQLAlchemy
from src.controller.request import RequestController

db = SQLAlchemy()
Request = RequestController()

from .PlanetModel import PlanetModel, PlanetSchema


