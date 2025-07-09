from fastapi import APIRouter, Depends, HTTPException
from app.banco import Equipamento, db
from pydantic import BaseModel
from app.depends import sessao
from sqlalchemy.orm import Session

equipamento_router = APIRouter(prefix="/equipamento", tags=["equipamento"])


class EquipamentoSchema(BaseModel):
    nome: str
    codigo_tag: str
    descricao: str
    unidade_id: int

    model_config = {
        "from_attributes": True
    }

@equipamento_router.get("/")
async def listar_equipamentos(session: Session = Depends(sessao)):
    equipamentos = session.query(Equipamento).all()
    return equipamentos

@equipamento_router.post("/")
async def criar_equipamentos(equipamento: EquipamentoSchema, session: Session = Depends(sessao)):
    try:
        equipamento_existente = session.query(Equipamento).filter(Equipamento.nome == equipamento.nome).first()

        if equipamento_existente:
            raise HTTPException(status_code=400, detail="Esse equipamento já existe")

        novo_equipamento = Equipamento(
            nome=equipamento.nome,
            codigo_tag=equipamento.codigo_tag,
            descricao=equipamento.descricao,
            unidade_id=equipamento.unidade_id,
        )

        session.add(novo_equipamento)
        session.commit()
        return {"mensagem": "Equipamento cadastrado com sucesso"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@equipamento_router.get("/{id}")
async def detalhar_equipamento(id: int, session: Session = Depends(sessao)):
    equipamento = session.query(Equipamento).filter(Equipamento.id == id).first()

    if not equipamento:
        raise HTTPException(status_code=404, detail="Esse equipamento não existe")

    return {
        "id": equipamento.id,
        "nome": equipamento.nome,
        "codigo_tag": equipamento.codigo_tag,
        "descricao": equipamento.descricao,
        "unidade_id": equipamento.unidade_id,
    }
