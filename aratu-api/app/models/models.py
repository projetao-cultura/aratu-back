from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Enum, ForeignKey, Text, Table
from sqlalchemy.dialects.postgresql import ARRAY 
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabela de associação para a relação many-to-many de amigos
amigos_association = Table('amigos', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('amigo_id', Integer, ForeignKey('usuarios.id'), primary_key=True)
)

# Tabela de associação para a relação many-to-many de eventos e usuarios (quero ir/fui)
usuarios_eventos_querem_ir = Table('usuarios_eventos_querem_ir', Base.metadata,
    Column('usuario_id', ForeignKey('usuarios.id'), primary_key=True),
    Column('evento_id', ForeignKey('eventos.id'), primary_key=True)
)

usuarios_eventos_foram = Table('usuarios_eventos_foram', Base.metadata,
    Column('usuario_id', ForeignKey('usuarios.id'), primary_key=True),
    Column('evento_id', ForeignKey('eventos.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)
    biografia = Column(Text)
    categorias_interesse = Column(ARRAY(String))
    telefone = Column(String, unique=True)
    foto_perfil = Column(String)
    
    amigos = relationship("Usuario",
                          secondary=amigos_association,
                          primaryjoin=id==amigos_association.c.usuario_id,
                          secondaryjoin=id==amigos_association.c.amigo_id,
                          backref="usuarios")
    
    eventos_quero_ir = relationship("Evento", secondary="usuarios_eventos_querem_ir", back_populates="usuarios_que_querem_ir")
    eventos_fui = relationship("Evento", secondary="usuarios_eventos_foram", back_populates="usuarios_que_foram")
    
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
    endereco = Column(String)
    data_hora = Column(DateTime)
    data_fim = Column(DateTime)
    valor = Column(Float, default=0.0)
    onde_comprar_ingressos = Column(String)
    id_sistema_origem = Column(Integer)
    fonte = Column(String)
    organizador = Column(String)
    gratis = Column(Boolean)
    atualizado_em = Column(DateTime)
    
    usuarios_que_querem_ir = relationship("Usuario", secondary=usuarios_eventos_querem_ir, back_populates="eventos_quero_ir")
    usuarios_que_foram = relationship("Usuario", secondary=usuarios_eventos_foram, back_populates="eventos_fui")
    avaliacoes = relationship("Avaliacao", back_populates="evento")

    def __repr__(self):
        return f"<Evento(nome='{self.nome}', descricao='{self.descricao}', local='{self.local}', data_hora='{self.data_hora}', data_fim='{self.data_fim}', valor={self.valor}, onde_comprar_ingressos='{self.onde_comprar_ingressos}', id_sistema_origem={self.id_sistema_origem}, fonte='{self.fonte}', organizador='{self.organizador}', gratis={self.gratis})>"
    
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
