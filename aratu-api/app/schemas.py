from enum import Enum
from fastapi.params import Query
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import Optional, List
from datetime import datetime

class Evento(BaseModel):
    id: Optional[int] = Field(None, description="ID do evento, gerado automaticamente")
    nome: str
    descricao: str
    banner: Optional[HttpUrl] = None
    categoria: List[str] = []
    avaliacao: Optional[float] = None
    local: str
    endereco: str
    data_hora: datetime
    data_fim: datetime
    id_sistema_origem: Optional[int] = Field(None, description="ID do evento no sistema de origem")
    fonte: str
    organizador: str
    gratis: bool
    atualizado_em: datetime
    valor: Optional[float] = Field(0.0, description="Valor do ingresso para o evento, gratuito por padrão.")
    onde_comprar_ingressos: Optional[HttpUrl] = None

    class Config:
        orm_mode = True

# Schema de Evento simplificado pra ser retornado nas listas do usuário (quero ir/fui)
class EventoMini(BaseModel):
    id: int
    nome: str
    data_hora: datetime
    local: str

    class Config:
        orm_mode = True

class AvaliacaoEvento(BaseModel):
    evento_id: int
    usuario_id: int 
    avaliacao: int  # De 1 a 5

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

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    biografia: Optional[str] = None
    telefone: str
    ativo: Optional[bool] = True
    foto_perfil: Optional[HttpUrl] = "https://i.imgur.com/JUf7jx3.jpeg"

    @validator('telefone', pre=True, always=True)
    def validar_telefone(cls, v):
        # Implemente a lógica de validação do telefone aqui
        return v
    
    @validator("email")
    def email_valido(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("E-mail inválido")
        return v

class UsuarioCreate(UsuarioBase):
    senha: str
    categorias_interesse: Optional[List[str]] = []
    lista_contatos: Optional[List[str]] = []

    @validator("senha")
    def senha_nao_nula(cls, v: str) -> str:
        if v is None:
            raise ValueError("Senha não pode ser nula")
        return v
    
class UsuarioMini(BaseModel):
    id: int

class Usuario(UsuarioBase):
    id: Optional[int] = Field(None, description="ID do usuário, gerado automaticamente")
    ativo: bool = True
    categorias_interesse: Optional[List[str]] = []
    amigos: List[UsuarioMini] = Field(default_factory=list, description="Lista de amigos do usuario")
    eventos_quero_ir: List[EventoMini] = Field(default_factory=list, description="Lista de eventos que o usuario quer ir")
    eventos_fui: List[EventoMini] = Field(default_factory=list, description="Lista de eventos que o usuario foi")

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str
    biografia: Optional[str] = None
    foto_perfil: Optional[HttpUrl] = None
    categorias_interesse: Optional[List[str]] = []

    class Config:
        orm_mode = True

class UserResponseExpand(UserResponse):
    amigos: List[UsuarioMini] = Field(default_factory=list, description="Lista de amigos do usuario")
    eventos_quero_ir: List[EventoMini] = Field(default_factory=list, description="Lista de eventos que o usuario quer ir")
    eventos_fui: List[EventoMini] = Field(default_factory=list, description="Lista de eventos que o usuario foi")
    avaliacoes: List[AvaliacaoEvento] = Field(default_factory=list, description="Lista de eventos que o usuario avaliou")

class EventoResponseExpand(EventoResponse):
    usuarios_que_querem_ir: List[UsuarioMini] = Field(default_factory=list, description="Lista de usuários que querem ir ao evento")
    usuarios_que_foram: List[UsuarioMini] = Field(default_factory=list, description="Lista de usuários que foram ao evento")
    avaliacoes: List[AvaliacaoEvento] = Field(default_factory=list, description="Lista de usuários que avaliaram o evento")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
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
    biografia: Optional[str] = None
    telefone: Optional[str] = None
    foto_perfil: Optional[HttpUrl] = None
    categorias_interesse: Optional[List[str]] = None

class ControleCargaStatus(str, Enum):
    ERRO = 'ERRO'
    EM_PROGRESSO = 'EM_PROGRESSO'
    SUCESSO = 'SUCESSO'

class ControleCarga(BaseModel):
    id: Optional[int] = Field(None, description="ID do controle de carga, gerado automaticamente")
    fonte: str
    inic_exec: datetime
    fim_exec: datetime
    dt_inic: datetime
    dt_fim: datetime
    qtd_src_total: int
    qtd_sucesso: int
    status: ControleCargaStatus
