
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Categoria:
    id: Optional[int]
    nome: str
    tipo: str  # 'receita' ou 'despesa'

@dataclass
class Transacao:
    id: Optional[int]
    descricao: str
    valor: float
    data: datetime
    categoria_id: int
    categoria_nome: Optional[str] = None

# TODO: Adicionar validações e métodos auxiliares
