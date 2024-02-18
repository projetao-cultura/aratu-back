from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY 
from sqlalchemy.orm import declarative_base, relationship

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
    banner = Column(String) 
    categoria = Column(ARRAY(String))
    local = Column(String)
    data_hora = Column(DateTime)
    valor = Column(Float, default=0.0)
    onde_comprar_ingressos = Column(String)
    
    avaliacoes = relationship("Avaliacao", back_populates="evento")

    def __repr__(self):
        return f"<Evento(nome='{self.nome}', descricao='{self.descricao}', local='{self.local}', data_hora='{self.data_hora}', valor={self.valor}, banner='{self.banner}')>"
    
class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    avaliacao = Column(Integer)
    
    evento = relationship("Evento", back_populates="avaliacoes")
    # Adicionaar a relação no modelo Usuario também, se necessário
    
    def __repr__(self):
        return f"<Avaliacao(evento_id={self.evento_id}, usuario_id={self.usuario_id}, avaliacao={self.avaliacao})>"

class ControleCarga(Base):
    __tablename__ = "controle_carga"
    
    id = Column(Integer, primary_key=True, index=True)
    fonte = Column(String)
    inic_exec = Column(DateTime)
    fim_exec = Column(DateTime)
    dt_inic = Column(DateTime)
    dt_fim = Column(DateTime)
    qtd_src_total = Column(Integer, default=0)
    qtd_sucesso = Column(Integer, default=0)
    status = Column(Enum('ERRO', 'EM_PROGRESSO', 'SUCESSO', name="tipo_categoria"))

    def __repr__(self):
        return f"<ControleCarga(id={self.id}, fonte='{self.fonte}', inic_exec='{self.inic_exec}', fim_exec='{self.fim_exec}', qtd_src_total={self.qtd_src_total}, qtd_sucesso={self.qtd_sucesso}, status='{self.status}')>"
