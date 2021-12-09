from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/')
def pessoa():
    return {"nome": "Gabriel"}


@app.route('/somasimples/<int:primeiro_valor>/<int:segundo_valor>')
def soma_simples(primeiro_valor, segundo_valor):
    return jsonify(f'soma: {primeiro_valor + segundo_valor}')


@app.route('/soma/', methods=['POST'])
def soma():
    dados = json.loads(request.data)
    soma_valores = 0
    for valor in dados['valores']:
        soma_valores += int(valor)
    return jsonify(f'soma: {soma_valores}')


if __name__ == '__main__':
    app.run(debug=True)