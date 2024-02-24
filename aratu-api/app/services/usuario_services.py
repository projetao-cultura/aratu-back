from app.models.models import Usuario
from app.models.models import Evento

def adicionar_amigo(session, usuario_id, amigo_id):
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    amigo = session.query(Usuario).filter(Usuario.id == amigo_id).first()
    if usuario and amigo:
        usuario.amigos.append(amigo)  # Adiciona amigo à lista de amigos do usuário
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