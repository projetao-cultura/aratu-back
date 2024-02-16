from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.api.v1.usuario_router import usuario_router
from app.api.v1.evento_router import evento_router

app = FastAPI(title="Aratu API", version="0.1")

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(evento_router, prefix="/eventos", tags=["Eventos"])

@app.get("/")
def root():
    return RedirectResponse(url="/docs")