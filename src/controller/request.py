# !/usr/bin/env python
# -*- coding: cp1252 -*-

import json
import requests

class RequestController():
    """
    Classe para centralização de Requests
    """

    def GetRequest(self, entrada: str):
        try:
            entrada_json = json.loads(entrada)
            url = str(entrada_json["url"])
            body = str(entrada_json["body"])

            if "\\u" in body:
                body = body.encode("latin1").decode("utf-8")

            header = dict(entrada_json["header"])

            x = requests.get(url, data=body, headers=header)
            resultado = json.loads(x.text)

            if x.status_code == 200:
                if resultado["results"] != []:
                    retorno = resultado
                else:
                    retorno = {'Erro': str('Planeta não encontrado!')}
            else:
                retorno = {'Erro': str('Erro ao consultar API Star Wars.')}
        except Exception as e:
            retorno = {'Erro': str(str(e))}
        finally:
            return retorno


    def getPlanetAppearances(self, name):
        """
        Obtém o número de aparições de um determinado planeta a partir de seu nome.
        Também verica se o mesmo existe no database de planetas fornecido pela API https://swapi.dev/
        """
        entrada = dict()
        entrada["url"] = f'https://swapi.dev/api/planets/?search={name}'
        entrada["header"] = {"Content-Type": "application/json"}
        entrada["body"] = ''

        raw_input = self.GetRequest(json.dumps(entrada))

        try:
            appearances = len(raw_input["results"][0]["films"])
        except KeyError:
            appearances = 0
        finally:
            return appearances