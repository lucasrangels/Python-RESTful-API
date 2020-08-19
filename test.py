import unittest
import json
from http import HTTPStatus
from flask_testing import TestCase
from src.app import create_app


class BaseTest(TestCase):

    def create_app(self):
        app = create_app('development')
        return app

    def testGetAllPlanets(self):
        self.client.delete("/api/v1/planetas/delete/all")
        response = self.client.get("/api/v1/planetas/")
        self.assertStatus(response, HTTPStatus.NO_CONTENT, message="Database não está vazio.")

    def testPostPlanet(self):
        self.client.delete("/api/v1/planetas/delete/all")
        data = [{
            "nome": "Tatooine",
            "clima": "Árido",
            "terreno": "Deserto"
        }, {
            "nome": "Alderaan",
            "clima": "Temperado",
            "terreno": "Montanha"
        }]

        for item in data:
            response = self.client.post("/api/v1/planetas/", json=item)
            self.assertStatus(response, HTTPStatus.CREATED, message="Cadastro de planetas falhou.")

    def testPutPlanet(self):
        data = {
            "nome": "Tatooine",
            "clima": "Temperado",
            "terreno": "Montanha"
        }
        response = self.client.put("/api/v1/planetas/", json=data)
        self.assertStatus(response, HTTPStatus.ACCEPTED, message="Atualização do cadastro de planetas falhou.")

    def testPutPlanetInvalid(self):
        data = {
            "nome": "PlanetaTESTE",
            "clima": "Temperado",
            "terreno": "Montanha"
        }
        response = self.client.put("/api/v1/planetas/", json=data)
        self.assertStatus(response, HTTPStatus.NO_CONTENT, message="Atualização de planeta com nome inválido falhou.")

    def testDeletePlanet(self):
        data = {
            "nome": "Tatooine",
            "clima": "Árido",
            "terreno": "Deserto"
        }
        response = self.client.delete("/api/v1/planetas/", json=data)
        self.assertStatus(response, HTTPStatus.ACCEPTED, message="Exclusão de planeta falhou.")

    def testDeleteInvalid(self):
        data = {
            "nome": "PlantaTeste",
            "clima": "TESTE",
            "terreno": "TESTE"
        }
        response = self.client.delete("/api/v1/planetas/", json=data)
        self.assertStatus(response, HTTPStatus.NO_CONTENT, message="Exclusão de planeta com nome inválido falhou.")

    def testDuplicateRow(self):
        data = {
            "nome": "Tatooine",
            "clima": "Árido",
            "terreno": "Deserto"
        }
        self.client.post("/api/v1/planetas/", json=data)
        response = self.client.post("/api/v1/planetas/", json=data)
        self.assertStatus(response, HTTPStatus.CONFLICT, message="Checar duplicidade no cadastro falhou.")

    def testGetbyName(self):
        data = {
            "nome": "Tatooine",
            "clima": "Árido",
            "terreno": "Deserto"
        }
        self.client.post("/api/v1/planetas/", json=data)
        response = self.client.get("/api/v1/planetas/Tatooine")
        self.assertStatus(response, HTTPStatus.OK, message="Busca de planetas por nome falhou.")

    def testGetbyNameInvalid(self):
        response = self.client.get("/api/v1/planetas/Planeta")
        self.assertStatus(response, HTTPStatus.NO_CONTENT, message="Busca de planeta com nome inválido falhou.")

    def testGetbyID(self):
        data = {
            "nome": "Tatooine",
            "clima": "Árido",
            "terreno": "Deserto"
        }
        self.client.post("/api/v1/planetas/", json=data)
        id = self.client.get("/api/v1/planetas/Tatooine")
        data = (id.data).decode("utf-8")
        planet = json.loads(data)
        response = self.client.get(f"/api/v1/planetas/{planet['id']}")
        self.assertStatus(response, HTTPStatus.OK, message="Busca de planetas por nome falhou.")

    def testGetbyIDInvalid(self):
        response = self.client.get("/api/v1/planetas/99999")
        self.assertStatus(response, HTTPStatus.NO_CONTENT, message="Busca de planeta com ID inválido falhou.")

def suite():

    suite = unittest.TestSuite()
    suite.addTest(BaseTest('testGetAllPlanets'))
    suite.addTest(BaseTest('testPostPlanet'))
    suite.addTest(BaseTest('testPutPlanet'))
    suite.addTest(BaseTest('testPutPlanetInvalid'))
    suite.addTest(BaseTest('testDeletePlanet'))
    suite.addTest(BaseTest('testDeleteInvalid'))
    suite.addTest(BaseTest('testDuplicateRow'))
    suite.addTest(BaseTest('testGetbyName'))
    suite.addTest(BaseTest('testGetbyNameInvalid'))
    suite.addTest(BaseTest('testGetbyID'))
    suite.addTest(BaseTest('testGetbyIDInvalid'))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())