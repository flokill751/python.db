from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from db import BancoDeDados

app = FastAPI()
db = BancoDeDados()

# Modelos para validação e tipagem dos dados recebidos/enviados

class Movimentacao(BaseModel):
    id: int
    tipo: str
    descricao: str
    valor: float
    data: str
    categoria: str

class MovimentacaoInput(BaseModel):
    tipo: str
    descricao: str
    valor: float
    data: str
    categoria_id: int

@app.get("/ping")
async def ping():
    return "Pong!"

@app.get("/movimentacoes", response_model=List[Movimentacao])
async def listar_movimentacoes():
    movimentacoes = db.listar_movimentacoes()
    resultado = []
    for mov in movimentacoes:
        resultado.append(Movimentacao(
            id=mov[0],
            tipo=mov[1],
            descricao=mov[2],
            valor=mov[3],
            data=mov[4],
            categoria=mov[5]
        ))
    return resultado

@app.post("/movimentacoes", status_code=201)
async def inserir_movimentacao(mov: MovimentacaoInput):
    try:
        db.inserir_movimentacao(
            mov.tipo,
            mov.descricao,
            mov.valor,
            mov.data,
            mov.categoria_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Movimentação inserida com sucesso!"}

@app.put("/movimentacoes/{id}")
async def atualizar_movimentacao(id: int, mov: MovimentacaoInput):
    try:
        db.atualizar_movimentacao(
            id,
            tipo=mov.tipo,
            descricao=mov.descricao,
            valor=mov.valor,
            data=mov.data,
            categoria_id=mov.categoria_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Movimentação atualizada com sucesso!"}


