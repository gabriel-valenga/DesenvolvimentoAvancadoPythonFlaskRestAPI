from flask_restful import Resource
from flask import request
import json

lista_habilidades = ['Python', 'Django', 'Flask']


class Habilidades(Resource):

    def put(self, index):
        try:
            habilidade = json.loads(request.data)
            lista_habilidades[index] = habilidade['habilidade']
            return habilidade
        except IndexError:
            return 'Erro ao acessar o indice informado'
        except Exception as e:
            return f'Erro desconhecido: {str(e)}'

    def delete(self, index):
        try:
            lista_habilidades.pop(index)
            return {'status': 'sucesso', 'mensagem': 'registro excluido com sucesso'}
        except IndexError:
            return 'Erro ao acessar o indice informado'
        except Exception as e:
            return f'Erro desconhecido: {str(e)}'


class ListaHabilidades(Resource):
    def get(self):
        return lista_habilidades

    def post(self):
        habilidade = request.data
        lista_habilidades.append(habilidade)
        return habilidade
