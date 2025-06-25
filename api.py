
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from db import DatabaseManager
from models import Categoria, Transacao

app = FastAPI(
    title="API de Finanças Pessoais", 
    version="1.0.0",
    description="API REST para gerenciamento de finanças pessoais"
)
db = DatabaseManager()

# Modelos Pydantic para API
class CategoriaCreate(BaseModel):
    nome: str
    tipo: str
    
    class Config:
        schema_extra = {
            "example": {
                "nome": "Alimentação",
                "tipo": "despesa"
            }
        }

class CategoriaUpdate(BaseModel):
    nome: str
    tipo: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    tipo: str

class TransacaoCreate(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria_id: int
    
    class Config:
        schema_extra = {
            "example": {
                "descricao": "Supermercado",
                "valor": -150.50,
                "data": "2024-01-15",
                "categoria_id": 1
            }
        }

class TransacaoUpdate(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria_id: int

class TransacaoResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    data: date
    categoria_id: int
    categoria_nome: Optional[str] = None

class ResumoFinanceiro(BaseModel):
    saldo_total: float
    total_receitas: float
    total_despesas: float
    total_transacoes: int
    total_categorias: int

# Endpoints principais
@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "API de Finanças Pessoais",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "categorias": "/categorias",
            "transacoes": "/transacoes",
            "resumo": "/resumo"
        }
    }

@app.get("/resumo", response_model=ResumoFinanceiro, tags=["Resumo"])
async def get_resumo_financeiro():
    """Retorna um resumo financeiro geral"""
    try:
        saldo_total = db.get_saldo_total()
        total_receitas = db.get_total_receitas()
        total_despesas = db.get_total_despesas()
        total_transacoes = len(db.get_transacoes())
        total_categorias = len(db.get_categorias())
        
        return ResumoFinanceiro(
            saldo_total=saldo_total,
            total_receitas=total_receitas,
            total_despesas=total_despesas,
            total_transacoes=total_transacoes,
            total_categorias=total_categorias
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Categorias
@app.get("/categorias", response_model=List[CategoriaResponse], tags=["Categorias"])
async def get_categorias():
    """Lista todas as categorias"""
    try:
        categorias = db.get_categorias()
        return [CategoriaResponse(id=c.id, nome=c.nome, tipo=c.tipo) for c in categorias]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorias"])
async def get_categoria(categoria_id: int):
    """Retorna uma categoria específica"""
    try:
        categoria = db.get_categoria_by_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return CategoriaResponse(id=categoria.id, nome=categoria.nome, tipo=categoria.tipo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/categorias", response_model=CategoriaResponse, tags=["Categorias"])
async def create_categoria(categoria: CategoriaCreate):
    """Cria uma nova categoria"""
    try:
        if categoria.tipo not in ['receita', 'despesa']:
            raise HTTPException(status_code=400, detail="Tipo deve ser 'receita' ou 'despesa'")
        
        categoria_id = db.create_categoria(categoria.nome, categoria.tipo)
        return CategoriaResponse(id=categoria_id, nome=categoria.nome, tipo=categoria.tipo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorias"])
async def update_categoria(categoria_id: int, categoria: CategoriaUpdate):
    """Atualiza uma categoria existente"""
    try:
        if categoria.tipo not in ['receita', 'despesa']:
            raise HTTPException(status_code=400, detail="Tipo deve ser 'receita' ou 'despesa'")
        
        success = db.update_categoria(categoria_id, categoria.nome, categoria.tipo)
        if not success:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        return CategoriaResponse(id=categoria_id, nome=categoria.nome, tipo=categoria.tipo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/categorias/{categoria_id}", tags=["Categorias"])
async def delete_categoria(categoria_id: int):
    """Exclui uma categoria"""
    try:
        success = db.delete_categoria(categoria_id)
        if not success:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return {"message": "Categoria excluída com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Transações
@app.get("/transacoes", response_model=List[TransacaoResponse], tags=["Transações"])
async def get_transacoes():
    """Lista todas as transações"""
    try:
        transacoes = db.get_transacoes()
        return [
            TransacaoResponse(
                id=t.id,
                descricao=t.descricao,
                valor=t.valor,
                data=t.data.date() if isinstance(t.data, datetime) else t.data,
                categoria_id=t.categoria_id,
                categoria_nome=t.categoria_nome
            ) for t in transacoes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transacoes/{transacao_id}", response_model=TransacaoResponse, tags=["Transações"])
async def get_transacao(transacao_id: int):
    """Retorna uma transação específica"""
    try:
        transacao = db.get_transacao_by_id(transacao_id)
        if not transacao:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        return TransacaoResponse(
            id=transacao.id,
            descricao=transacao.descricao,
            valor=transacao.valor,
            data=transacao.data.date() if isinstance(transacao.data, datetime) else transacao.data,
            categoria_id=transacao.categoria_id,
            categoria_nome=transacao.categoria_nome
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transacoes", response_model=TransacaoResponse, tags=["Transações"])
async def create_transacao(transacao: TransacaoCreate):
    """Cria uma nova transação"""
    try:
        # Verificar se a categoria existe
        categoria = db.get_categoria_by_id(transacao.categoria_id)
        if not categoria:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")
        
        data_str = transacao.data.strftime('%Y-%m-%d')
        transacao_id = db.create_transacao(
            transacao.descricao,
            transacao.valor,
            data_str,
            transacao.categoria_id
        )
        
        return TransacaoResponse(
            id=transacao_id,
            descricao=transacao.descricao,
            valor=transacao.valor,
            data=transacao.data,
            categoria_id=transacao.categoria_id,
            categoria_nome=categoria.nome
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/transacoes/{transacao_id}", response_model=TransacaoResponse, tags=["Transações"])
async def update_transacao(transacao_id: int, transacao: TransacaoUpdate):
    """Atualiza uma transação existente"""
    try:
        # Verificar se a categoria existe
        categoria = db.get_categoria_by_id(transacao.categoria_id)
        if not categoria:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")
        
        data_str = transacao.data.strftime('%Y-%m-%d')
        success = db.update_transacao(
            transacao_id,
            transacao.descricao,
            transacao.valor,
            data_str,
            transacao.categoria_id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        return TransacaoResponse(
            id=transacao_id,
            descricao=transacao.descricao,
            valor=transacao.valor,
            data=transacao.data,
            categoria_id=transacao.categoria_id,
            categoria_nome=categoria.nome
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/transacoes/{transacao_id}", tags=["Transações"])
async def delete_transacao(transacao_id: int):
    """Exclui uma transação"""
    try:
        success = db.delete_transacao(transacao_id)
        if not success:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        return {"message": "Transação excluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categorias/{categoria_id}/transacoes", response_model=List[TransacaoResponse], tags=["Transações"])
async def get_transacoes_by_categoria(categoria_id: int):
    """Lista transações de uma categoria específica"""
    try:
        # Verificar se a categoria existe
        categoria = db.get_categoria_by_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        transacoes = db.get_transacoes_by_categoria(categoria_id)
        return [
            TransacaoResponse(
                id=t.id,
                descricao=t.descricao,
                valor=t.valor,
                data=t.data.date() if isinstance(t.data, datetime) else t.data,
                categoria_id=t.categoria_id,
                categoria_nome=t.categoria_nome
            ) for t in transacoes
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
