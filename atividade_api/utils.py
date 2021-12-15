from models import Pessoas


def insere_pessoa():
    pessoa = Pessoas(nome='Teste')
    pessoa.save()


def consulta_pessoas():
    pessoa = Pessoas.query.all()

