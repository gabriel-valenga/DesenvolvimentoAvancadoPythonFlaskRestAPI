from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, StatusAtividade, Usuarios
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha, ativo=True).first()


class Pessoa(Resource):
    def get(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        if pessoa:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        else:
            response = {'status': 'Erro',
                        'mensagem': 'Pessoa não encontrada'}
        return response

    @auth.login_required
    def put(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        dados = request.json
        if pessoa:
            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
        else:
            response = {'status': 'Erro',
                        'mensagem': 'Pessoa não encontrada'}
        return response

    @auth.login_required
    def delete(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        if pessoa:
            pessoa.delete()
            response = {'status': 'Sucesso',
                        'mensagem': f'Pessoa do id {id} excluída com sucesso.'}
        else:
            response = {'status': 'Erro',
                        'mensagem': 'Pessoa não encontrada'}
        return response


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': pessoa.id,
                     'nome': pessoa.nome,
                     'idade': pessoa.idade} for pessoa in pessoas]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response


class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': atividade.id,
                     'nome': atividade.nome,
                     'pessoa': atividade.pessoa.nome,
                     'status': atividade.status} for atividade in atividades]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()
        if pessoa:
            atividade = Atividades(nome=dados['nome'],
                                   pessoa=pessoa)
            if 'status' in dados:
                if StatusAtividade.validar_status(dados['status']):
                    atividade.status = dados['status']
                else:
                    return {'status': 'Erro',
                            'mensagem': f'Status {dados["status"]} não permitido. '
                                        'Status deve ser pendente ou concluído.'}
            atividade.save()
            response = {
                'id': atividade.id,
                'nome': atividade.nome,
                'pessoa': atividade.pessoa.nome,
                'status': atividade.status
            }
        else:
            response = {'status': 'Erro',
                        'mensagem': 'Pessoa não encontrada'}

        return response


class ListaAtividadesPorNomePessoa(Resource):
    def get(self, nome_pessoa):
        pessoa = Pessoas.query.filter_by(nome=nome_pessoa).first()
        if pessoa:
            atividades = Atividades.query.filter_by(pessoa_id=pessoa.id)
            response = [{'id': atividade.id, 'nome': atividade.nome,
                         'pessoa': atividade.pessoa.nome, 'status': atividade.status}
                        for atividade in atividades]
        else:
            response = {'status': 'Erro',
                        'mensagem': f'pessoa_id {id} não existe.'}
        return response


class Atividade(Resource):
    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        if atividade:
            response = {'id': atividade.id,
                        'nome': atividade.nome,
                        'pessoa': atividade.pessoa.nome,
                        'status': atividade.status}
        else:
            response = {'status': 'Erro',
                        'mensagem': 'Atividade não encontrada'}
        return response

    @auth.login_required
    def put(self, id):
        dados = request.json
        atividade = Atividades.query.filter_by(id=id).first()
        if atividade:
            if dados['status']:
                if StatusAtividade.validar_status(dados['status']):
                    atividade.status = dados['status']
                else:
                    return {'status': 'Erro',
                            'mensagem': f'Status {dados["status"]} não permitido. '
                                        'Status deve ser pendente ou concluído.'}
            atividade.save()
            response = {'id': atividade.id,
                        'nome': atividade.nome,
                        'pessoa': atividade.pessoa.nome,
                        'status': atividade.status}
        else:
            response = {'status': 'Erro',
                        'mensagem': 'Atividade não encontrada'}
        return response


api.add_resource(Pessoa, '/pessoas/<int:id>/')
api.add_resource(ListaPessoas, '/pessoas/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(Atividade, '/atividades/<int:id>/')
api.add_resource(ListaAtividadesPorNomePessoa, '/atividades/pessoa/<string:nome_pessoa>/')

if __name__ == '__main__':
    app.run(debug=True)
