from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, get_password_hash, create_access_token, verify_password
from app.models.models import Usuario as ModelUsuario  
from app.schemas import UserResponse, UsuarioCreate, UsuarioUpdate, Token
from app.db.base import get_db

usuario_router = APIRouter()

@usuario_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se o e-mail já está cadastrado
    db_usuario = db.query(ModelUsuario).filter(ModelUsuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já está em uso")
    
    hashed_password = get_password_hash(usuario.senha)
    
    # Cria um novo usuário
    novo_usuario = ModelUsuario(nome=usuario.nome, email=usuario.email, senha=hashed_password, ativo=usuario.ativo)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return UserResponse.from_orm(novo_usuario)


@usuario_router.get("/{usuario_id}", response_model=UserResponse)
async def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Busca o usuário por ID
    usuario = db.query(ModelUsuario).filter(ModelUsuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return UserResponse.from_orm(usuario)

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

