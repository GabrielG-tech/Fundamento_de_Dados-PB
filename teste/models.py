from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Atleta(Base):
    __tablename__ = 'atletas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    sexo = Column(String)
    altura = Column(Float)
    peso = Column(Float)
    pais_id = Column(Integer, ForeignKey('paises.id'))

    pais = relationship("Pais", back_populates="atletas")

class Pais(Base):
    __tablename__ = 'paises'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    atletas = relationship("Atleta", back_populates="pais")

class Evento(Base):
    __tablename__ = 'eventos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    esporte_id = Column(Integer, ForeignKey('esportes.id'))
    jogos_id = Column(Integer, ForeignKey('jogos.id'))

    esporte = relationship("Esporte", back_populates="eventos")
    jogos = relationship("Jogos", back_populates="eventos")

class Esporte(Base):
    __tablename__ = 'esportes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    eventos = relationship("Evento", back_populates="esporte")

class Jogos(Base):
    __tablename__ = 'jogos'
    id = Column(Integer, primary_key=True)
    ano = Column(Integer)
    temporada = Column(String)
    cidade = Column(String)

    eventos = relationship("Evento", back_populates="jogos")

class Participacao(Base):
    __tablename__ = 'participacoes'
    id_atleta = Column(Integer, ForeignKey('atletas.id'), primary_key=True)
    id_evento = Column(Integer, ForeignKey('eventos.id'), primary_key=True)
    id_jogos = Column(Integer, ForeignKey('jogos.id'))
    medalha = Column(String)

    atleta = relationship("Atleta")
    evento = relationship("Evento")

class Medalha(Base):
    __tablename__ = 'medalhas'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
