from fastapi import HTTPException
from typing import List
from app.models.models import Usuario, Evento, Avaliacao
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound

async def get_eventos_interesse(session, usuario_id):
    # Primeiro, obtemos as categorias de interesse do usuário
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    categorias_interesse = usuario.categorias_interesse

    # Agora, filtramos os eventos que possuem interseção com as categorias de interesse
    eventos_de_interesse = session.query(Evento).filter(
        Evento.categoria.overlap(categorias_interesse)
    ).limit(15).all()

    return eventos_de_interesse

def adicionar_amigo(session, usuario_id, amigo_id):
    if usuario_id == amigo_id:
        raise HTTPException(status_code=400, detail="Não é possível adicionar a si mesmo como amigo.")
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    amigo = session.query(Usuario).filter(Usuario.id == amigo_id).first()

    if not usuario or not amigo:
        raise HTTPException(status_code=404, detail="Usuário ou amigo não encontrado.")
    
    if amigo in usuario.amigos:
        raise HTTPException(status_code=400, detail="Este amigo já foi adicionado.")
    
    usuario.amigos.append(amigo)  # Adiciona amigo à lista de amigos do usuário
    session.commit()

def remover_amigo(session, usuario_id, amigo_id):
    if usuario_id == amigo_id:
        raise HTTPException(status_code=400, detail="Não é possível remover a si mesmo da lista de amigos.")
    
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    amigo = session.query(Usuario).filter(Usuario.id == amigo_id).first()

    if not usuario or not amigo:
        raise HTTPException(status_code=404, detail="Usuário ou amigo não encontrado.")
    
    if amigo not in usuario.amigos:
        raise HTTPException(status_code=404, detail="Este amigo não está na sua lista de amigos.")
    
    usuario.amigos.remove(amigo)  # Remove o amigo da lista de amigos do usuário
    session.commit()

def adicionar_amigos_por_telefone(session, usuario_id: int, telefones: List[str]):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for telefone in telefones:
        try:
            amigo_potencial = session.query(Usuario).filter(Usuario.telefone == telefone).one()
            if amigo_potencial not in usuario.amigos:
                usuario.amigos.append(amigo_potencial)
            else:
                pass
        except NoResultFound:
            pass

    session.commit()

def adicionar_evento_quero_ir(session, usuario_id, evento_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    evento = session.query(Evento).filter(Evento.id == evento_id).first()
    
    if not usuario or not evento:
        raise HTTPException(status_code=404, detail="Usuário ou evento não encontrado.")

    if evento in usuario.eventos_quero_ir:
        raise HTTPException(status_code=400, detail="Evento já está na lista de 'Quero Ir'.")

    usuario.eventos_quero_ir.append(evento)
    session.commit()

def adicionar_evento_fui(session, usuario_id, evento_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    evento = session.query(Evento).filter(Evento.id == evento_id).first()
    
    if not usuario or not evento:
        raise HTTPException(status_code=404, detail="Usuário ou evento não encontrado.")

    if evento in usuario.eventos_fui:
        raise HTTPException(status_code=400, detail="Evento já está na lista de 'Fui'.")

    usuario.eventos_fui.append(evento)
    session.commit()

def remover_evento_quero_ir(session, usuario_id, evento_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    evento = session.query(Evento).filter(Evento.id == evento_id).first()
    
    if not usuario or not evento:
        raise HTTPException(status_code=404, detail="Usuário ou evento não encontrado.")

    if evento not in usuario.eventos_quero_ir:
        raise HTTPException(status_code=400, detail="Evento não está na lista de 'Quero Ir'.")

    usuario.eventos_quero_ir.remove(evento)
    session.commit()

def remover_evento_fui(session, usuario_id, evento_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    evento = session.query(Evento).filter(Evento.id == evento_id).first()
    
    if not usuario or not evento:
        raise HTTPException(status_code=404, detail="Usuário ou evento não encontrado.")

    if evento not in usuario.eventos_fui:
        raise HTTPException(status_code=400, detail="Evento não está na lista de 'Fui'.")

    usuario.eventos_fui.remove(evento)
    session.commit()

def buscar_usuario_com_eventos_e_medias(session, usuario_id: int):
    # Substitua ModelEvento, ModelAvaliacao, etc., pelos nomes reais dos seus modelos
    eventos_quero_ir = session.query(
        Evento.id,
        Evento.nome,
        Evento.data_hora,
        Evento.local,
        Evento.banner,
        func.coalesce(func.round(func.avg(Avaliacao.avaliacao), 1), 0).label("media_avaliacao")
    ).outerjoin(Avaliacao).filter(Evento.usuarios_que_querem_ir.any(id=usuario_id)).group_by(Evento.id).all()

    eventos_fui = session.query(
        Evento.id,
        Evento.nome,
        Evento.data_hora,
        Evento.local,
        Evento.banner,
        func.coalesce(func.round(func.avg(Avaliacao.avaliacao), 1), 0).label("media_avaliacao")
    ).outerjoin(Avaliacao).filter(Evento.usuarios_que_foram.any(id=usuario_id)).group_by(Evento.id).all()

    return eventos_quero_ir, eventos_fui