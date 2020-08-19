from flask import request, json, Response, Blueprint
from ..models.PlanetModel import PlanetModel, PlanetSchema
from http import HTTPStatus

planet_api = Blueprint('planet_api', __name__)
planet_schema = PlanetSchema()


@planet_api.route('/', methods=['POST'])
def create():
    """
    Método para inserção de planetas
    """

    req_data = request.get_json()

    if type(req_data) == list:
        for item in req_data:
            data = planet_schema.load(item)
            hasPlanet = PlanetModel.getPlanetbyName(data.get('nome'))

            if hasPlanet is not None:
                message = {'Erro': 'Planeta inserido já está cadastrado'}
                return custom_response(message, HTTPStatus.CONFLICT)


            planet = PlanetModel(data)
            response = planet.save()
            if not response:
                return custom_response({
                    'Erro': "Planeta inexistente no universo de Star Wars. Consulte o link a seguir para mais informações sobre os planetas existentes: 'https://pt.qwe.wiki/wiki/List_of_Star_Wars_planets_and_moons'"}, HTTPStatus.CONFLICT)
    else:
        data = planet_schema.load(req_data)

        hasPlanet = PlanetModel.getPlanetbyName(data.get('nome'))
        if hasPlanet is not None:
            message = {'Erro': 'Planeta inserido já está cadastrado'}
            return custom_response(message, HTTPStatus.CONFLICT)

        planet = PlanetModel(data)
        response = planet.save()

        if not response:
            return custom_response({
                'Erro': "Planeta inexistente no universo de Star Wars. Consulte o link a seguir para mais informações sobre os planetas existentes: 'https://pt.qwe.wiki/wiki/List_of_Star_Wars_planets_and_moons'"}, HTTPStatus.CONFLICT)

    message = {'Mensagem': 'Planetas cadastrado com sucesso!'}

    return custom_response(message, HTTPStatus.CREATED)


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
        return custom_response(message, HTTPStatus.NO_CONTENT)

    planet.update(data)
    ser_planet = planet_schema.dump(planet)

    return custom_response(ser_planet, HTTPStatus.ACCEPTED)


@planet_api.route('/', methods=['GET'])
def get_all():
    """
    Método para obter todas as entradas de planetas cadastradas no banco de dados
    """

    planets = PlanetModel.getAllPlanets()
    ser_planets = planet_schema.dump(planets, many=True)

    if ser_planets == []:
        return custom_response("{'Mensagem': 'Não há planetas cadastrados.'}", HTTPStatus.NO_CONTENT)
    else:
        return custom_response(ser_planets, HTTPStatus.OK)


@planet_api.route('/<string:nome>', methods=['GET'])
def getByName(nome):
    """
    Método para obter um planeta específico a partir do nome
    """
    planet = PlanetModel.getPlanetbyName(nome)
    if planet is None:
        return custom_response({'Erro': 'Planeta não encontrado a partir do nome informado!'}, HTTPStatus.NO_CONTENT)


    ser_planet = planet_schema.dump(planet)

    return custom_response(ser_planet, HTTPStatus.OK)


@planet_api.route('/<int:id>', methods=['GET'])
def getByID(id):
    """
    Método para obter um planeta específico a partir de uma ID
    """
    planet = PlanetModel.getPlanetbyID(id)
    if planet is None:
        return custom_response({'Erro': 'Planeta não encontrado a partir do ID informado!'}, HTTPStatus.NO_CONTENT)

    ser_planet = planet_schema.dump(planet)

    return custom_response(ser_planet, HTTPStatus.OK)


@planet_api.route('/', methods=['DELETE'])
def delete():
  """
  Método para exclusão de planetas cadastrados no banco de dados
  """
  req_data = request.get_json()

  if type(req_data) == list:
    for item in req_data:
        data = planet_schema.load(item)
        planet = PlanetModel.getPlanetbyName(data.get('nome'))
        if planet is None:
            message = {'Erro': 'Não foi possível excluir o planeta pois o mesmo não está cadastrado.'}
            return custom_response(message, HTTPStatus.NO_CONTENT)
        planet.delete()
  else:
      data = planet_schema.load(req_data)

      planet = PlanetModel.getPlanetbyName(data.get('nome'))

      if planet is None:
          message = {'Erro': 'Não foi possível excluir o planeta pois o mesmo não está cadastrado.'}
          return custom_response(message, HTTPStatus.NO_CONTENT)

      planet.delete()

  message = {'Mensagem': 'Planeta(s) excluído(s) com sucesso!'}

  return custom_response(message, HTTPStatus.ACCEPTED)

@planet_api.route('/delete/all', methods=['DELETE'])
def deleteAll():
  """
  Método debug para exclusão
  """
  planet = PlanetModel({})
  planet.cleanDB()

  return custom_response({"Debug": "Limpeza de DB concluída"}, HTTPStatus.ACCEPTED)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )