from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Enum
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

class ControleCarga(Base):
    __tablename__ = "controle_carga"
    
    id = Column(Integer, primary_key=True, index=True)
    fonte = Column(String)
    inic_exec = Column(String)
    fim_exec = Column(String)
    qtd_src_total = Column(Integer, default=0)
    qtd_sucesso = Column(Integer, default=0)
    status = Column(Enum('ERRO', 'EM_PROGRESSO', 'SUCESSO'))

    def __repr__(self):
        return f"<ControleCarga(id={self.id}, fonte='{self.fonte}', inic_exec='{self.inic_exec}', fim_exec='{self.fim_exec}', qtd_src_total={self.qtd_src_total}, qtd_sucesso={self.qtd_sucesso}, status='{self.status}')>"
