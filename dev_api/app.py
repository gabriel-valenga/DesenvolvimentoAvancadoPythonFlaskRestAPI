from flask import Flask, jsonify, request
import json

app = Flask(__name__)

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


@app.route('/dev/<int:id>/', methods=['GET'])
def buscar_dev_por_id(id):
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
    return jsonify(response)


@app.route('/dev/<int:id>/', methods=['PUT'])
def atualizar_dev(id):
    """
    Atualiza o desenvolvedor do id informado.
    :param id: int
    :return: JSON
    """
    dados = json.loads(request.data)
    dev = json.loads(buscar_dev_por_id(id).data)
    if dev:
        desenvolvedores[dev[0][0]['list_index']] = dados
        response = dados
    else:
        response = {'status': 'não encontrado',
                    'mensagem': f'Desenvolvedor do id {id} não existe'}
    return jsonify(response)


@app.route('/dev/<int:id>/', methods=['DELETE'])
def apagar_dev(id):
    """
    Apaga o desenvolvedor do id informado.
    :param id: int
    :return: JSON
    """
    dev = json.loads(buscar_dev_por_id(id).data)
    if dev:
        desenvolvedores.pop(dev[0][0]['list_index'])
        return jsonify({'status': 'sucesso', 'mensagem': 'Registro excluído'})
    else:
        return jsonify({'status': 'não encontrado',
                        'mensagem': f'Desenvolvedor do id {id} não encontrado.'})


@app.route('/dev/', methods=['GET'])
def lista_desenvolvedores():
    """
    Lista todos os desenvolvedores.
    :return: JSON
    """
    return jsonify(desenvolvedores)


@app.route('/dev/', methods=['POST'])
def adicionar_dev():
    """
    Adiciona o desenvolvedor enviado na lista de desenvolvedores.
    :return: JSON
    """
    dados = json.loads(request.data)
    dados['id'] = incrementa_id_auto()
    desenvolvedores.append(dados)
    return jsonify(desenvolvedores[-1])


if __name__ == '__main__':
    app.run(debug=True)
