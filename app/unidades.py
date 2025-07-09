from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.banco import Unidade
from app.depends import sessao
from sqlalchemy.orm import Session

unidades_router = APIRouter(prefix="/unidade", tags=["unidade"])

class UnidadeSchema(BaseModel):
    nome: str
    tipo: str
    localidade: str

    class Config:
        from_attributes = True

@unidades_router.post("/")
async def criar_unidade(unidade: UnidadeSchema, session: Session = Depends(sessao)):
    unidade_existe = session.query(Unidade).filter(Unidade.nome == unidade.nome).first()

    if unidade_existe:
        raise HTTPException(status_code=400, detail="Essa unidade já existe")

    nova_unidade = Unidade(
        nome=unidade.nome,
        tipo=unidade.tipo,
        localidade=unidade.localidade,
    )

    session.add(nova_unidade)
    session.commit()
    session.refresh(nova_unidade)

    return {"mensagem": "Unidade criada com sucesso"}
    
@unidades_router.get("/")
async def listar_unidade(session: Session = Depends(sessao)):
    unidade = session.query(Unidade).all()
    return unidade

@unidades_router.get("/{id}")
async def detalhar_unidade(id: int, session: Session = Depends(sessao)):
    unidade = session.query(Unidade).filter(Unidade.id == id).first()

    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    return {
        "id": unidade.id,
        "nome": unidade.nome,
        "tipo": unidade.tipo,
        "localidade": unidade.localidade,
    }

@unidades_router.delete("/{id}")
async def deletar_unidade(id: int, session: Session = Depends(sessao)):
    unidades = session.query(Unidade).filter(Unidade.id == id).first()

    if not unidades:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    session.delete(unidades)
    session.commit()

    return {"mensagem": "Unidade deletada com sucesso"}
