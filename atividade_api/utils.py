from models import Pessoas, Usuarios


def insere_pessoa():
    pessoa = Pessoas(nome='Teste')
    pessoa.save()


def consulta_pessoas():
    pessoa = Pessoas.query.all()


def insere_usuario(login, senha, ativo=True):
    usuario = Usuarios(login=login, senha=senha, ativo=ativo)
    usuario.save()


def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)


if __name__ == '__main__':
    insere_usuario('gabriel', '123')
    insere_usuario('jefferson', '456', False)
    consulta_todos_usuarios()
