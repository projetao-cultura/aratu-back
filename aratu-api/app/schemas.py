from fastapi.params import Query
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import Optional, List
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
    banner: Optional[HttpUrl] = None
    categoria: List[str] = []
    avaliacao: Optional[float] = None
    local: str
    data_hora: datetime
    valor: Optional[float] = Field(0.0, description="Valor do ingresso para o evento, gratuito por padrão.")
    onde_comprar_ingressos: Optional[HttpUrl] = None
    usuarios_que_querem_ir: List[int] = Field(default_factory=list, description="Lista de IDs de usuários que querem ir ao evento")
    usuarios_que_foram: List[int] = Field(default_factory=list, description="Lista de IDs de usuários que foram ao evento")
    usuarios_que_avaliaram: List[int] = Field(default_factory=list, description="Lista de IDs de usuários que avaliaram o evento")

    class Config:
        orm_mode = True


class AvaliacaoEvento(BaseModel):
    evento_id: int
    usuario_id: int 
    avaliacao: int  

    @validator('evento_id')
    def evento_deve_existir(cls, v, values):
        if v not in values['evento_id']:
            raise ValueError("Evento não existe")
        return v
    
    @validator('usuario_id')
    def usuario_deve_existir(cls, v, values):
        if v not in values['usuario_id']:
            raise ValueError("Usuário não existe")
        return v

    @validator('avaliacao')
    def avaliacao_deve_ser_valida(cls, v):
        if v < 1 or v > 5:
            raise ValueError("A avaliação deve ser entre 1 e 5")
        return v

class EventoResponse(Evento):
    pass

class EventoList(BaseModel):
    pages: int  
    eventos: list[EventoResponse]

class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

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
