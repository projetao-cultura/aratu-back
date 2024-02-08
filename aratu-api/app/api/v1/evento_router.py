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
        likes=0
    )
    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)

    evento_response = EventoResponse.from_orm(novo_evento)
    # Adicione campos adicionais se necessário
    evento_response.gostei_count = 0

    return evento_response


@evento_router.get("/eventos/", response_model=list[EventoResponse])
async def listar_eventos(db: Session = Depends(get_db)):
    eventos = db.query(ModelEvento).all()
    
    # Use from_orm para criar uma lista de EventoResponse a partir dos eventos
    eventos_response = [EventoResponse.from_orm(evento) for evento in eventos]
    
    return eventos_response
