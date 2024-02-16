from fastapi.params import Query
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    id: Optional[int] = Field(None, description="ID do usuário, gerado automaticamente")
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True

    @validator("senha")
    def senha_nao_nula(cls, v: str) -> str:
        if v is None:
            raise ValueError("Senha não pode ser nula")
        return v
    
    @validator("email")
    def email_valido(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("E-mail inválido")
        return v

class Evento(BaseModel):
    id: Optional[int] = Field(None, description="ID do evento, gerado automaticamente")
    nome: str
    descricao: str
    local: str
    data_hora: datetime
    valor: Optional[float] = 0.0  # Pode ser gratuito, por isso é opcional e por padrão 0.0
    foto_url: Optional[HttpUrl] = None  # URL para a foto do evento
    likes: int = 0

    class Config:
        orm_mode = True


class EventoLike(BaseModel):
    evento_id: int
    usuario_email: EmailStr
    gostei: bool

class EventoResponse(Evento):
    pass

class EventoList(BaseModel):
    pages: int  
    eventos: list[EventoResponse]
 
class Pagination(BaseModel):
    perPage: int
    page: int
    order: str = "asc" 

def pagination_params(
        page: int = Query(ge=1, required=False, default=1, le=500000), 
        perPage: int = Query(ge=1, le=100, required=False, default=10), 
        order: str = Query(default="asc")
        ):
        return Pagination(perPage=perPage, page=page, order=order)

class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Para atualizações de eventos ou usuários, permitindo alterar somente os campos específicos
class EventoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    local: Optional[str] = None
    data_hora: Optional[datetime] = None
    valor: Optional[float] = None
    foto_url: Optional[HttpUrl] = None

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[bool] = None
