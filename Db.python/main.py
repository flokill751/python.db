from db import BancoDeDados

def main():
    db = BancoDeDados()


    if not db.listar_categorias():
        db.inserir_categoria("Salário")

    categoria_id = db.listar_categorias()[0][0]

  
    db.inserir_movimentacao(
        tipo="Receita",
        descricao="Pagamento mensal",
        valor=3000.00,
        data="2025-06-16",
        categoria_id=categoria_id
    )

    print("Movimentações:")
    for mov in db.listar_movimentacoes():
        print(mov)

    db.fechar()

if __name__ == "__main__":
    main()
