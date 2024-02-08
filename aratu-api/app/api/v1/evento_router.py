from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.models.models import Evento as ModelEvento 
from app.schemas import Evento, EventoResponse
from app.db.base import get_db

evento_router = APIRouter()

@evento_router.post("/eventos/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
async def criar_evento(evento: Evento, db: Session = Depends(get_db)):
    # Cria um novo registro de evento no banco de dados
    novo_evento = ModelEvento(
        nome=evento.nome,
        descricao=evento.descricao,
        local=evento.local,
        data_hora=evento.data_hora,
        valor=evento.valor,
        foto_url=evento.foto_url,
        likes=evento.likes
    )
    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)

    evento_response = {
        "id": novo_evento.id,
        "nome": novo_evento.nome,
        "descricao": novo_evento.descricao,
        "local": novo_evento.local,
        "data_hora": novo_evento.data_hora,
        "valor": novo_evento.valor,
        "foto_url": novo_evento.foto_url,
        "likes": novo_evento.likes,
        "gostei_count": 0  # Adicione outros campos necessários aqui
    }

    return evento_response


@evento_router.get("/eventos/", response_model=list[EventoResponse])
async def listar_eventos(db: Session = Depends(get_db)):
    # Busca todos os eventos no banco de dados
    eventos = db.query(ModelEvento).all()
    return eventos
