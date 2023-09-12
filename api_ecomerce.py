from flask import Flask, request, jsonify

app = Flask(__name__)

# Classe Produto


class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

# Classe Carrinho


class Carrinho:
    def __init__(self):
        self.items = []

    def adicionar_produto(self, produto):
        self.items.append(produto)

    def remover_produto(self, produto):
        if produto in self.items:
            self.items.remove(produto)

    def calcular_total(self):
        total = 0
        for produto in self.items:
            total += produto.preco
        return total

    def finalizar_compra(self):
        total = self.calcular_total()
        return total

# Classe Pedido


class Pedido:
    def __init__(self, produtos, total):
        self.produtos = produtos
        self.total = total


# Criação de uma instância de Carrinho
carrinho = Carrinho()

# Rota para adicionar um produto ao carrinho


@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    data = request.json
    nome = data['nome']
    preco = data['preco']
    estoque = data['estoque']

    produto = Produto(nome, preco, estoque)
    carrinho.adicionar_produto(produto)

    return "Produto adicionado ao carrinho com sucesso."

# Rota para remover um produto do carrinho


@app.route('/remover_produto', methods=['POST'])
def remover_produto():
    data = request.json
    nome = data['nome']

    for produto in carrinho.items:
        if produto.nome == nome:
            carrinho.remover_produto(produto)
            return "Produto removido do carrinho com sucesso."

    return "Produto não encontrado no carrinho."

# Rota para calcular o total do carrinho


@app.route('/calcular_total', methods=['GET'])
def calcular_total():
    total = carrinho.calcular_total()
    return jsonify({"total": total})

# Rota para finalizar a compra


@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    total = carrinho.finalizar_compra()
    produtos = [produto.nome for produto in carrinho.items]
    pedido = Pedido(produtos, total)
    carrinho.items = []  # Limpa o carrinho após a compra

    return jsonify({"pedido": pedido.__dict__, "mensagem": "Compra finalizada com sucesso."})


if __name__ == '__main__':
    app.run(debug=True)
