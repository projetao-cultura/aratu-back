from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models.models import Usuario as ModelUsuario  
from app.schemas import Usuario, UserResponse  
from app.db.base import get_db

usuario_router = APIRouter()

@usuario_router.post("/create/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    # Verifica se o e-mail já está cadastrado
    db_usuario = db.query(ModelUsuario).filter(ModelUsuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já está em uso")
    
    # Cria um novo usuário
    novo_usuario = ModelUsuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha, ativo=usuario.ativo)
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

