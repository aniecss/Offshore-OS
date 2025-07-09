from fastapi import FastAPI
from app.usuarios import usuarios_router
from app.unidades import unidades_router
from app.servico import servico_router
from app.equipamento import equipamento_router

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(unidades_router)
app.include_router(servico_router)
app.include_router(equipamento_router)