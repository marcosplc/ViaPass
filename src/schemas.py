from decimal import Decimal

from pydantic import BaseModel, Field


class ValidarRequest(BaseModel):
    cartao_id: int


class ValidarResponse(BaseModel):
    liberado: bool
    motivo: str
    mensagem: str
    nome: str | None = None
    saldo_restante: float | None = None
    
class CartaoResponse(BaseModel):
    cartao_id: int
    nome: str
    saldo: float
    status: str


class RecargaRequest(BaseModel):
    valor: Decimal = Field(gt=0, max_digits=8, decimal_places=2)


class RecargaResponse(BaseModel):
    cartao_id: int
    valor_recarregado: float
    saldo_atual: float