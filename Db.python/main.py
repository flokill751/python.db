from fastapi import FastAPI
from db import BancoDeDados

app = FastAPI()

@app.get("/ping")
async def ping():
    return "Pong!"

def inicializar_dados():
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

    db.fechar()

if __name__ == "__main__":
    inicializar_dados()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
