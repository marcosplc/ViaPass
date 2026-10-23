from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cartao, Recarga
from ..schemas import CartaoResponse, RecargaRequest, RecargaResponse

router = APIRouter(prefix="/cartoes", tags=["cartoes"])


@router.get("/{cartao_id}", response_model=CartaoResponse)
def consultar(cartao_id: int, db: Session = Depends(get_db)):
    cartao = db.get(Cartao, cartao_id)
    if cartao is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    return CartaoResponse(
        cartao_id=cartao.id,
        nome=cartao.usuario.nome,
        saldo=float(cartao.saldo),
        status=cartao.status,
    )


@router.post("/{cartao_id}/recarga", response_model=RecargaResponse)
def recarregar(cartao_id: int, dados: RecargaRequest, db: Session = Depends(get_db)):
    cartao = db.execute(
        select(Cartao).where(Cartao.id == cartao_id).with_for_update()
    ).scalar_one_or_none()
    if cartao is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    cartao.saldo += dados.valor
    db.add(Recarga(cartao_id=cartao.id, valor=dados.valor))
    db.commit()

    return RecargaResponse(
        cartao_id=cartao.id,
        valor_recarregado=float(dados.valor),
        saldo_atual=float(cartao.saldo),
    )