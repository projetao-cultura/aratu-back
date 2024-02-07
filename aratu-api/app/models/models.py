from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', email='{self.email}', ativo={self.ativo})>"

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    local = Column(String)
    data_hora = Column(DateTime)
    valor = Column(Float)
    foto_url = Column(String)
    likes = Column(Integer, default=0)

    def __repr__(self):
        return f"<Evento(nome='{self.nome}', descricao='{self.descricao}', local='{self.local}', data_hora='{self.data_hora}', valor={self.valor}, foto_url='{self.foto_url}', likes={self.likes})>"
