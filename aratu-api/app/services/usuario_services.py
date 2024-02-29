from fastapi import HTTPException
from typing import List
from app.models.models import Usuario, Evento

async def get_eventos_interesse(session, usuario_id):
    # Primeiro, obtemos as categorias de interesse do usuário
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    categorias_interesse = usuario.categorias_interesse

    # Agora, filtramos os eventos que possuem interseção com as categorias de interesse
    eventos_de_interesse = session.query(Evento).filter(
        Evento.categoria.overlap(categorias_interesse)
    ).all()

    return eventos_de_interesse

def adicionar_amigo(session, usuario_id, amigo_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    amigo = session.query(Usuario).filter(Usuario.id == amigo_id).first()
    if usuario and amigo:
        usuario.amigos.append(amigo)  # Adiciona amigo à lista de amigos do usuário
        session.commit()

def adicionar_amigos_por_telefone(session, usuario_id: int, telefones: List[str]):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for telefone in telefones:
        amigo_potencial = session.query(Usuario).filter(Usuario.telefone == telefone).first()
        if amigo_potencial and amigo_potencial not in usuario.amigos:
            usuario.amigos.append(amigo_potencial)

    session.commit()

def adicionar_evento_quero_ir(session, usuario_id, evento_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    evento = session.query(Evento).filter(Evento.id == evento_id).first()
    if usuario and evento:
        usuario.eventos_quero_ir.append(evento)
        session.commit()

def adicionar_evento_fui(session, usuario_id, evento_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    evento = session.query(Evento).filter(Evento.id == evento_id).first()
    if usuario and evento:
        usuario.eventos_fui.append(evento)
        session.commit()

def remover_amigo(session, usuario_id, amigo_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    amigo = session.query(Usuario).filter(Usuario.id == amigo_id).first()
    if usuario and amigo:
        usuario.amigos.remove(amigo)
        session.commit()
