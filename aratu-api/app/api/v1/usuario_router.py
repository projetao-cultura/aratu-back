from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_user, get_password_hash, create_access_token, verify_password
from app.models.models import Usuario as ModelUsuario
from app.schemas import UserResponse, UserResponseExpand, UsuarioCreate, UsuarioUpdate, UsuarioMini, Token, EventoResponse, EventoMini
from app.db.base import get_db
from app.services import usuario_services as service

usuario_router = APIRouter()

@usuario_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary='Criar um usuário')
async def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se o e-mail ou telefone já está cadastrado
    db_usuario = db.query(ModelUsuario).filter(ModelUsuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já está em uso")
    
    telefone = db.query(ModelUsuario).filter(ModelUsuario.telefone == usuario.telefone).first()
    if telefone:
        raise HTTPException(status_code=400, detail="Telefone já está em uso")
    
    hashed_password = get_password_hash(usuario.senha)
    
    # Cria um novo usuário
    novo_usuario = ModelUsuario(
        nome=usuario.nome, 
        email=usuario.email, 
        senha=hashed_password,
        telefone=usuario.telefone, 
        ativo=usuario.ativo,
        categorias_interesse=usuario.categorias_interesse
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return UserResponse.from_orm(novo_usuario)

@usuario_router.get("/{usuario_id}", response_model=UserResponse, summary='Listar um usuário')
async def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Busca o usuário por ID
    usuario = db.query(ModelUsuario).filter(ModelUsuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return UserResponse.from_orm(usuario)

@usuario_router.get("/{usuario_id}/expand", response_model=UserResponseExpand, summary='Buscar um Usuário expandindo Amigos e Eventos (Fui/Quero ir)')
async def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(ModelUsuario).filter(ModelUsuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    amigos = [UsuarioMini(id=amigo.id) for amigo in usuario.amigos]
    eventos_quero_ir = [
        EventoMini(id=evento.id, nome=evento.nome, data_hora=evento.data_hora, local=evento.local)  
        for evento in usuario.eventos_quero_ir
    ]
    eventos_fui = [
        EventoMini(id=evento.id, nome=evento.nome, data_hora=evento.data_hora, local=evento.local) 
        for evento in usuario.eventos_fui
    ]

    user_response = UserResponseExpand(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        biografia=usuario.biografia,
        telefone=usuario.telefone,
        foto_perfil=usuario.foto_perfil,
        amigos=amigos, 
        eventos_quero_ir=eventos_quero_ir,
        eventos_fui=eventos_fui,
        categorias_interesse=usuario.categorias_interesse
    )
    
    return user_response

@usuario_router.put('/{usuario_id}', response_model=UserResponse, summary='Atualizar um Usuário')
def update_user(
    user_id: int,
    user: UsuarioUpdate,
    session: Session = Depends(get_db),
    current_user: ModelUsuario = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    current_user.email = user.email
    current_user.senha = get_password_hash(user.senha)
    session.commit()
    session.refresh(current_user)

    return current_user

@usuario_router.get('/buscar/{nome}', response_model=list[UserResponse], summary='Buscar um Usuário por parte do nome')
def buscar_usuario_por_nome(nome: str, db: Session = Depends(get_db)):
    usuarios = db.query(ModelUsuario).filter(ModelUsuario.nome.ilike(f'%{nome}%')).all()
    return [UserResponse.from_orm(usuario) for usuario in usuarios]

@usuario_router.post('/selectedUsers', response_model=list[UserResponse], summary='Listar Usuários por uma lista de ids de usuário')
def listar_usuarios(ids: list[int], db: Session = Depends(get_db)):
    usuarios = db.query(ModelUsuario).filter(ModelUsuario.id.in_(ids)).all()
    return [UserResponse.from_orm(usuario) for usuario in usuarios]

@usuario_router.post('/token', response_model=Token, summary='Gerar um Token de Acesso')
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = db.query(ModelUsuario).filter(ModelUsuario.email == form_data.username).first()

    if not usuario:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': usuario.email})

    return {'access_token': access_token, 'token_type': 'bearer'}

@usuario_router.get("/eventos-de-interesse/{usuario_id}", response_model=List[EventoResponse], summary='Listar Eventos de Interesse do Usuário')
async def eventos_de_interesse_do_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        eventos_de_interesse = await service.get_eventos_interesse(db, usuario_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return eventos_de_interesse

@usuario_router.post("/{usuario_id}/amigos/{amigo_id}", status_code=status.HTTP_201_CREATED)
async def adicionar_amigo(usuario_id: int, amigo_id: int, db: Session = Depends(get_db)):
    service.adicionar_amigo(db, usuario_id, amigo_id)
    return {"mensagem": "Amigo adicionado com sucesso"}

@usuario_router.post("/{usuario_id}/amigos_lista_contatos", status_code=status.HTTP_201_CREATED, summary='Adicionar amigos por lista de contatos')
async def adicionar_amigos_endpoint(usuario_id: int, telefones: List[str], db: Session = Depends(get_db)):
    try:
        service.adicionar_amigos_por_telefone(db, usuario_id, telefones)
        return {"mensagem": "Amigos adicionados com sucesso"}
    except HTTPException as e:
        raise e

@usuario_router.post("/{usuario_id}/quero_ir/{evento_id}", status_code=status.HTTP_201_CREATED)
async def adicionar_evento_quero_ir(usuario_id: int, evento_id: int, db: Session = Depends(get_db)):
    service.adicionar_evento_quero_ir(db, usuario_id, evento_id)
    return {"mensagem": "Evento adicionado à lista de 'Quero Ir' com sucesso"}

@usuario_router.post("/{usuario_id}/fui/{evento_id}", status_code=status.HTTP_201_CREATED)
async def adicionar_evento_fui(usuario_id: int, evento_id: int, db: Session = Depends(get_db)):
    service.adicionar_evento_fui(db, usuario_id, evento_id)
    return {"mensagem": "Evento adicionado à lista de 'Fui' com sucesso"}
