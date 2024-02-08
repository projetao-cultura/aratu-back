from fastapi import FastAPI
from app.api.v1.usuario_router import usuario_router
from app.api.v1.evento_router import evento_router

app = FastAPI()

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(evento_router, prefix="/eventos", tags=["Eventos"])