from flask import Flask, jsonify, request
import json

app = Flask(__name__)

id_auto = 0
tarefas = []


def incrementa_id_auto():
    """
    Funcao que incrementa o id automatico da lista
    :return: int
    """
    global id_auto
    id_auto += 1
    return id_auto


@app.route('/tarefas/', methods=['GET'])
def listar_todas_tarefas():
    """
    Lista todas as tarefas da lista
    :return: JSON
    """
    return jsonify(tarefas)


@app.route('/tarefas/', methods=['POST'])
def adicionar_tarefa():
    """
    Adiciona a tarefa enviada no body na lista de tarefas
    :return: JSON (Retorna a tarefa passada no body)
    """
    dados = json.loads(request.data)
    dados['id'] = incrementa_id_auto()
    tarefas.append(dados)
    return jsonify(tarefas[-1])


@app.route('/tarefas/<int:id>/', methods=['GET'])
def buscar_tarefa_por_id(id):
    """
    Retorna a tarefa do id passado por parametro
    :param id: int
    :return: JSON
    """
    tarefa_encontrada = [({'list_index': index}, tarefa) for index, tarefa in enumerate(tarefas) if tarefa['id'] == id]
    return jsonify(tarefa_encontrada)


@app.route('/tarefas/<int:id>/', methods=['PUT'])
def alterar_status_tarefa(id):
    """
    Funcao para alterar apenas o status de uma tarefa
    :param id: int
    :return: JSON
    """
    tarefa = json.loads(buscar_tarefa_por_id(id).data)
    if tarefa:
        dados = json.loads(request.data)
        index = tarefa[0][0]['list_index']
        tarefas[index]['status'] = dados['status']
        response = tarefas[index]
    else:
        response = {'status': 'não encontrado',
                    'mensagem': f'Tarefa do id {id} não existe'}
    return jsonify(response)


@app.route('/tarefas/<int:id>/', methods=['DELETE'])
def excluir_tarefa(id):
    """
    Exclui a tarefa do id informado por parametro
    :param id: int
    :return: JSON
    """
    tarefa = json.loads(buscar_tarefa_por_id(id).data)
    if tarefa:
        tarefas.pop(tarefa[0][0]['list_index'])
        return jsonify({'status': 'sucesso', 'mensagem': 'Registro excluído'})
    else:
        return jsonify({'status': 'não encontrado',
                        'mensagem': f'Tarefa do id {id} não encontrada.'})


if __name__ == '__main__':
    app.run(debug=True)