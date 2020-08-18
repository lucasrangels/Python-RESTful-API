from flask import request, json, Response, Blueprint
from ..models.PlanetModel import PlanetModel, PlanetSchema

planet_api = Blueprint('planet_api', __name__)
planet_schema = PlanetSchema()


@planet_api.route('/', methods=['POST'])
def create():
    """
    Método para inserção de planetas
    """

    req_data = request.get_json()
    data = planet_schema.load(req_data)

    hasPlanet = PlanetModel.getPlanetbyName(data.get('nome'))
    if hasPlanet is not None:
        message = {'Erro': 'Planeta inserido já está cadastrado'}
        return custom_response(message, 400)

    planet = PlanetModel(data)
    response = planet.save()

    if response:
        message = {'Mensagem': 'Planeta cadastrado com sucesso!'}
    else:
        message = {'Erro': "Planeta inexistente no universo de Star Wars. Consulte o link a seguir para mais informações sobre os planetas existentes: 'https://pt.qwe.wiki/wiki/List_of_Star_Wars_planets_and_moons'"}

    return custom_response(message, 201)


@planet_api.route('/', methods=['PUT'])
def update():
    """
    Método para atualização de planetas já cadastrados no banco
    """
    req_data = request.get_json()
    data = planet_schema.load(req_data, partial=True)


    planet = PlanetModel.getPlanetbyName(data.get('nome'))
    if planet is None:
        message = {'Erro': 'Não foi possível atualizar informações do planeta pois o mesmo não está cadastrado.'}
        return custom_response(message, 400)

    planet.update(data)
    ser_planet = planet_schema.dump(planet)

    return custom_response(ser_planet, 200)


@planet_api.route('/', methods=['GET'])
def get_all():
    """
    Método para obter todas as entradas de planetas cadastradas no banco de dados
    """

    planets = PlanetModel.getAllPlanets()
    ser_planets = planet_schema.dump(planets, many=True)

    return custom_response(ser_planets, 200)


@planet_api.route('/<string:nome>', methods=['GET'])
def getByName(nome):
    """
    Método para obter um planeta específico a partir do nome
    """
    planet = PlanetModel.getPlanetbyName(nome)
    if planet is None:
        return custom_response({'Erro': 'Planeta não encontrado a partir do nome informado!'}, 404)


    ser_planet = planet_schema.dump(planet)

    return custom_response(ser_planet, 200)


@planet_api.route('/<int:id>', methods=['GET'])
def getByID(id):
    """
    Método para obter um planeta específico a partir de uma ID
    """
    planet = PlanetModel.getPlanetbyID(id)
    if planet is None:
        return custom_response({'Erro': 'Planeta não encontrado a partir do ID informado!'}, 404)

    ser_planet = planet_schema.dump(planet)

    return custom_response(ser_planet, 200)


@planet_api.route('/', methods=['DELETE'])
def delete():
  """
  Método para exclusão de planetas cadastrados no banco de dados
  """
  req_data = request.get_json()
  data = planet_schema.load(req_data)

  planet = PlanetModel.getPlanetbyName(data.get('nome'))

  if planet is None:
      message = {'Erro': 'Não foi possível excluir o planeta pois o mesmo não está cadastrado.'}
      return custom_response(message, 400)

  planet.delete()
  message = {'Mensagem': 'Planeta excluído com sucesso!'}

  return custom_response(message, 201)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )