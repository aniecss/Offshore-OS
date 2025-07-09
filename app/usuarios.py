from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.banco import Usuario
from app.depends import sessao
from sqlalchemy.orm import Session

usuarios_router = APIRouter(prefix="/usuario", tags=["usuario"])

class UsuarioSchema(BaseModel):
    nome: str
    cpf: int
    cargo: str
    email: str
    senha: str

    model_config = {
        "from_attributes": True
    }

@usuarios_router.post("/")
async def criar_usuario(usuario: UsuarioSchema, session: Session = Depends(sessao)):
    usuario_existe = session.query(Usuario).filter(Usuario.cpf == usuario.cpf).first()

    if usuario_existe:
        raise HTTPException(status_code=409, detail="Usuário já existe")

    novo_usuario = Usuario(
        nome=usuario.nome,
        cpf=usuario.cpf,
        cargo=usuario.cargo,
        email=usuario.email,
        senha=usuario.senha,
    )

    session.add(novo_usuario)
    session.commit()

    return {"mensagem": "Usuário cadastrado com sucesso"}

@usuarios_router.get("/")
async def listar_usuario(session: Session = Depends(sessao)):
    usuarios = session.query(Usuario).all()
    return usuarios

@usuarios_router.get("/{id}")
async def detalhar_usuario(id: int, session: Session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "cpf": usuario.cpf,
        "cargo": usuario.cargo,
    }

@usuarios_router.delete("/{id}")
async def deletar_usuario(id: int, session: Session = Depends(sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    session.delete(usuario)
    session.commit()

    return {"mensagem": "Usuário deletado com sucesso"}
