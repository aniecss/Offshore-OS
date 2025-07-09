from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from app.banco import Servico, Usuario, db
from app.depends import sessao
from sqlalchemy.orm import Session

servico_router = APIRouter(prefix="/servico", tags=["servico"])

class ServicoSchema(BaseModel):
    usuario_id: int
    descricao: str
    data_abertura: datetime
    status: str
    unidade_id: int
    equipamento_id: int

    model_config = {
        "from_attributes": True
    }

class ServicoUpdateSchema(BaseModel):
    status: str

# Listar todos os serviços
@servico_router.get("/")
async def listar_servicos(session: Session = Depends(sessao)):
    return session.query(Servico).all()


@servico_router.post("/")
async def criar_servicos(servico: ServicoSchema, session: Session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == servico.usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não existe")

    novo_servico = Servico(
        usuario_id=servico.usuario_id,
        descricao=servico.descricao,
        data_abertura=servico.data_abertura,
        status=servico.status,
        unidade_id=servico.unidade_id,
        equipamento_id=servico.equipamento_id,
    )
    session.add(novo_servico)
    session.commit()
    session.refresh(novo_servico)

    return {"mensagem": "Serviço criado com sucesso"}

# Detalhar um serviço específico
@servico_router.get("/{id}")
async def detalhar_servico(id: int, session: Session = Depends(sessao)):
    servico = session.get(Servico, id)

    if not servico:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    return servico

# Atualizar status de um serviço
@servico_router.put("/{id}")
async def atualizar_servico(id: int, dados: ServicoUpdateSchema, session: Session = Depends(sessao)):
    servico = session.get(Servico, id)

    if not servico:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")

    servico.status = dados.status
    session.commit()
    session.refresh(servico)
    return servico

# Cancelar (deletar) um serviço
@servico_router.delete("/{id}")
async def cancelar_servico(id: int, session: Session = Depends(sessao)):
    servico = session.get(Servico, id)

    if not servico:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")

    session.delete(servico)
    session.commit()

    return {"ok": True, "mensagem": "Ordem de serviço cancelada com sucesso"}
