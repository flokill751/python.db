from flask import Flask, request, jsonify
from db import BancoDeDados

app = Flask(__name__)
db = BancoDeDados()

@app.route('/ping')
def ping():
    return 'Pong!', 200

@app.route('/movimentacoes', methods=['GET'])
def listar_movimentacoes():
    movimentacoes = db.listar_movimentacoes()
    resultado = []

    for mov in movimentacoes:
        resultado.append({
            'id': mov[0],
            'tipo': mov[1],
            'descricao': mov[2],
            'valor': mov[3],
            'data': mov[4],
            'categoria': mov[5]
        })

    return jsonify(resultado), 200

@app.route('/movimentacoes', methods=['POST'])
def inserir_movimentacao():
    data = request.json
    tipo = data.get('tipo')
    descricao = data.get('descricao')
    valor = data.get('valor')
    data_mov = data.get('data')
    categoria_id = data.get('categoria_id')

    db.inserir_movimentacao(tipo, descricao, valor, data_mov, categoria_id)
    return jsonify({'message': 'Movimentação inserida com sucesso!'}), 201

@app.route('/movimentacoes/<int:id>', methods=['PUT'])
def atualizar_movimentacao(id):
    data = request.get_json()
    db.atualizar_movimentacao(
        id,
        tipo=data['tipo'],
        descricao=data['descricao'],
        valor=data['valor'],
        data=data['data'],
        categoria_id=data['categoria_id'],
    )
    return jsonify({'message': 'Movimentação atualizada com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
