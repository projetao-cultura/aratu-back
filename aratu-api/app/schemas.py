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
    usuarios_que_querem_ir: List[int] = Field(default_factory=list, description="Lista de IDs de usuários que querem ir ao evento")
    usuarios_que_foram: List[int] = Field(default_factory=list, description="Lista de IDs de usuários que foram ao evento")
    usuarios_que_avaliaram: List[int] = Field(default_factory=list, description="Lista de IDs de usuários que avaliaram o evento")

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

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    biografia: Optional[str] = None
    telefone: str
    ativo: Optional[bool] = True
    foto_perfil: Optional[HttpUrl] = None

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

    @validator("senha")
    def senha_nao_nula(cls, v: str) -> str:
        if v is None:
            raise ValueError("Senha não pode ser nula")
        return v

class Usuario(UsuarioBase):
    id: Optional[int] = Field(None, description="ID do usuário, gerado automaticamente")
    ativo: bool = True
    amigos: List[int] = Field(default_factory=list, description="Lista de IDs de amigos do usuario")
    eventos_quero_ir: List[int] = Field(default_factory=list, description="Lista de IDs de eventos que o usuario quer ir")
    eventos_fui: List[int] = Field(default_factory=list, description="Lista de IDs de eventos que o usuario foi")

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    eventos_quero_ir: List[EventoMini] = []
    eventos_fui: List[EventoMini] = []

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
    biografia: Optional[str] = None
    telefone: Optional[str] = None
    foto_perfil: Optional[HttpUrl] = None

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
