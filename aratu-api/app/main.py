from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.api.v1.usuario_router import usuario_router
from app.api.v1.evento_router import evento_router

tags_metadata = [
    {
        "name": "CRUD Usuario",
        "description": ""
    },
    {
        "name": "CRUD Evento",
        "description": ""
    },
    {
        "name": "Autenticação",
        "description": ""
    },
    {
        "name": "Feed",
        "description": "Endpoints para gerenciar e exibir os carrosseis do feed de eventos."
    },
    {
        "name": "Ações do Usuário",
        "description": "Ações específicas que os usuários podem realizar, como avaliar eventos, adicionar amigos e expressar interesse em participar de eventos."
    },
    {
        "name": "Busca",
        "description": ""
    },
    {
        "name": "Carregar Eventos",
        "description": "Endpoints para carregar e sincronizar eventos a partir de fontes externas."
    },
]

app = FastAPI(title="Aratu API", version="0.1", openapi_tags=tags_metadata, description="API para o aplicativo Aratu", redoc_url=None, docs_url="/")

app.include_router(usuario_router, prefix="/usuarios")
app.include_router(evento_router, prefix="/eventos")