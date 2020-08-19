import datetime
from . import db,Request
from marshmallow import fields, Schema



class PlanetModel(db.Model):
    """
    Classe modelo para tipagem de planetas
    """

    # Nome da Tabela
    __tablename__ = 'planetas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), unique=True, nullable=False)
    clima = db.Column(db.String(128), nullable=False)
    terreno = db.Column(db.String(128), nullable=False)
    quantidade_aparicoes = db.Column(db.Integer)
    data_criacao = db.Column(db.DateTime)
    data_modificacao = db.Column(db.DateTime)


    def __init__(self, data):
        """
        Construtor da classe planetas
        """
        self.nome = data.get('nome')
        self.clima = data.get('clima')
        self.terreno = data.get('terreno')
        self.quantidade_aparicoes = data.get('quantidade_aparicoes')
        self.data_criacao = datetime.datetime.utcnow()
        self.data_modificacao = datetime.datetime.utcnow()

    def save(self):
        """
        Método para realizar inserções no banco de dados
        """
        self.quantidade_aparicoes = Request.getPlanetAppearances(self.nome)
        if self.quantidade_aparicoes == 0:
            return False
        else:
            db.session.add(self)
            db.session.commit()
            return True

    def update(self, data):
        """
        Método para realizar alterações no banco de dados
        """
        for key, item in data.items():
            setattr(self, key, item)
        self.data_modificacao = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        """
        Método para excluir entradas no banco de dados.
        """
        db.session.delete(self)
        db.session.commit()

    def cleanDB(self):
        """
        Método para excluir todas entradas no banco de dados.
        """
        db.session.query(PlanetModel).delete()
        db.session.commit()


    @staticmethod
    def getAllPlanets():
        """
        Método destinado para buscar todos os planetas cadastrados
        """
        return PlanetModel.query.all()

    @staticmethod
    def getPlanetbyID(id):
        """
        Método para buscar um planeta cadastrado a partir de seu ID
        """
        return PlanetModel.query.get(id)

    @staticmethod
    def getPlanetbyName(nome):
        """
        Método para buscar um planeta cadastrado a partir de seu nome
        """
        return PlanetModel.query.filter_by(nome=nome).first()

    def __repr(self):
        return '<id {}>'.format(self.id)


class PlanetSchema(Schema):
  """
  Schema para classe 'Planets'
  """
  id = fields.Int(dump_only=True)
  nome = fields.Str(required=True)
  clima = fields.Str(required=True)
  terreno = fields.Str(required=True)
  quantidade_aparicoes = fields.Int(dump_only=True)
  data_criacao = fields.DateTime(dump_only=True)
  data_modificacao = fields.DateTime(dump_only=True)