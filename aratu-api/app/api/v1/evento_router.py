from math import ceil
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from app.models.models import Evento as ModelEvento 
from app.schemas import Evento, EventoList, EventoResponse, pagination_params, Pagination
from app.db.base import get_db

from typing import List

evento_router = APIRouter()

@evento_router.post("/create/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
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

    return evento_response

@evento_router.post("/delete/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_evento(
    evento_id: int, 
    db: Session = Depends(get_db)
    ):
    # Deleta evento por ID
    evento = db.query(ModelEvento).filter(ModelEvento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    db.delete(evento)
    db.commit()
    
    return None

@evento_router.put('/update/{evento_id}', response_model=EventoResponse, status_code=status.HTTP_200_OK, summary='Atualizar um Evento')
async def update_event(
    evento_id: int,
    evento: Evento,
    db: Session = Depends(get_db)
):
    # Busca o evento por ID
    evento_db = db.query(ModelEvento).filter(ModelEvento.id == evento_id).first()
    if not evento_db:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    # Atualiza o evento
    evento_db.nome = evento.nome
    evento_db.descricao = evento.descricao
    evento_db.local = evento.local
    evento_db.data_hora = evento.data_hora
    evento_db.valor = evento.valor
    evento_db.foto_url = evento.foto_url
    db.commit()
    db.refresh(evento_db)

    return EventoResponse.from_orm(evento_db)


@evento_router.get("/list/allEvents", response_model=list[EventoResponse])
async def listar_eventos(db: Session = Depends(get_db)):
    eventos = db.query(ModelEvento).all()
    
    # Use from_orm para criar uma lista de EventoResponse a partir dos eventos
    eventos_response = [EventoResponse.from_orm(evento) for evento in eventos]
    
    return eventos_response


@evento_router.post("/list/selectedEvents", response_model=list[EventoResponse])
async def listar_eventos_selecionados(
    eventos_ids: List[int],
    db: Session = Depends(get_db)
):
    # Busca os eventos por uma lista de ID's
    eventos = db.query(ModelEvento).filter(ModelEvento.id.in_(eventos_ids)).all()
    
    # Use from_orm para criar uma lista de EventoResponse a partir dos eventos
    eventos_response = [EventoResponse.from_orm(evento) for evento in eventos]
    
    return eventos_response

@evento_router.get("/feed/", response_model=EventoList)
async def feed_eventos(
    db: Session = Depends(get_db),
    page: int = Query(ge=1, default=1, description="Número da página para a paginação, começando de 1"),
    perPage: int = Query(ge=1, le=100, default=10, description="Número de eventos por página"),
    order: str = Query(default="asc", description="Ordenação dos eventos, 'asc' para ascendente e 'desc' para descendente")
):
    # Calcular o offset baseado na página atual
    offset = (page - 1) * perPage

    # Construir a query com ordenação e paginação
    query = db.query(ModelEvento)
    if order == "asc":
        query = query.order_by(ModelEvento.data_hora.asc())
    else:
        query = query.order_by(ModelEvento.data_hora.desc())
    eventos = query.offset(offset).limit(perPage).all()

    # Criar a resposta dos eventos usando o esquema Pydantic
    eventos_response = [EventoResponse.from_orm(evento) for evento in eventos]

    # Calcular o total de páginas
    total_eventos = db.query(ModelEvento).count()
    total_pages = ceil(total_eventos / perPage)

    return EventoList(pages=total_pages, eventos=eventos_response)
