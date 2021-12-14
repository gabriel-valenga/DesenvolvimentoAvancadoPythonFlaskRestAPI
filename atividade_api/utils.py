from models import Pessoas


def insere_pessoa():
    pessoa = Pessoas(nome)
    pessoa.save()


def consulta_pessoas():
    pessoa = Pessoas.query.all()



def altera_pessoa():
