from flask import Flask, request
from flask_restful import Resource, Api
import json
from habilidades import Habilidades, ListaHabilidades

app = Flask(__name__)
api = Api(app)


id_auto = 0


def incrementa_id_auto():
    global id_auto
    id_auto += 1
    return id_auto


desenvolvedores = [
    {'id': incrementa_id_auto(),
     'nome': 'José',
     'habilidades': ['Python', 'Flask']
     },
    {'id': incrementa_id_auto(),
     'nome': 'Carlos',
     'habilidades': ['Python', 'Django']
     }
]


class Desenvolvedor(Resource):
    def get(self, id):
        """
        Retorna um desenvolvedor buscando pelo id.
        :param id: int
        :return: JSON
        """
        try:
            response = [({'list_index': index}, dev) for index, dev in enumerate(desenvolvedores) if dev['id'] == id]
        except Exception:
            mensagem = 'Erro desconhecido, procure o administrador da API'
            response = {'status': 'erro', 'mensagem': mensagem}
        return response

    def put(self, id):
        """
        Atualiza o desenvolvedor do id informado.
        :param id: int
        :return: JSON
        """
        dados = json.loads(request.data)
        dev = self.get(id)
        if dev:
            if verifica_habilidades_dev(dados['habilidades']):
                desenvolvedores[dev[0][0]['list_index']] = dados
                response = dados
            else:
                response = {'status': 'não permitido',
                            'mensagem': 'habilidade não está na lista de habilidades'}
        else:
            response = {'status': 'não encontrado',
                        'mensagem': f'Desenvolvedor do id {id} não existe'}
        return response

    def delete(self, id):
        """
            Apaga o desenvolvedor do id informado.
            :param id: int
            :return: JSON
            """
        dev = self.get(id)
        if dev:
            desenvolvedores.pop(dev[0][0]['list_index'])
            return {'status': 'sucesso', 'mensagem': 'Registro excluído'}
        else:
            return {'status': 'não encontrado',
                    'mensagem': f'Desenvolvedor do id {id} não encontrado.'}


class ListaDesenvolvedores(Resource):
    def get(self):
        """
        Lista todos os desenvolvedores.
        :return: JSON
        """
        return desenvolvedores

    def post(self):
        """
        Adiciona o desenvolvedor enviado na lista de desenvolvedores.
        :return: JSON
        """
        dados = json.loads(request.data)
        if verifica_habilidades_dev(dados['habilidades']):
            dados['id'] = incrementa_id_auto()
            desenvolvedores.append(dados)
            return desenvolvedores[-1]
        else:
            return {'status': 'não permitido',
                    'mensagem': 'habilidade não está na lista de habilidades'}


def verifica_habilidades_dev(habilidades_dev):
    """
    Verifica se as habilidades passadas no JSON estão na lista de habilidades.
    :param habilidades: list()
    :return: bool
    """
    lista_habilidades = ListaHabilidades()
    habilidades = lista_habilidades.get()
    for habilidade in habilidades_dev:
        if habilidade not in habilidades:
            return False
    return True


api.add_resource(Desenvolvedor, '/dev/<int:id>/')
api.add_resource(ListaDesenvolvedores, '/dev/')
api.add_resource(Habilidades, '/habilidades/<int:index>/')
api.add_resource(ListaHabilidades, '/habilidades/')

if __name__ == '__main__':
    app.run(debug=True)