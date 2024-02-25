from app.models.models import Usuario
from app.models.models import Evento

async def get_eventos_interesse(session, usuario_id):
    # Primeiro, obtemos as categorias de interesse do usuário
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    categorias_interesse = usuario.categorias_interesse

    # Agora, filtramos os eventos que possuem interseção com as categorias de interesse
    eventos_de_interesse = session.query(Evento).filter(
        Evento.categoria.overlap(categorias_interesse)
    ).all()

    return eventos_de_interesse