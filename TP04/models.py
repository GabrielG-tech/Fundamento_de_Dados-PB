from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Associação muitos para muitos
livro_autor = Table('livro_autor', Base.metadata,
    Column('id_livro', Integer, ForeignKey('livro.id_livro')),
    Column('id_autor', Integer, ForeignKey('autor.id_autor'))
)

class Livro(Base):
    __tablename__ = 'livro'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    data_lancamento = Column(Date, nullable=False)
    preco = Column(Float, nullable=False)
    autores = relationship('Autor', secondary=livro_autor, back_populates='livros')

class Autor(Base):
    __tablename__ = 'autor'
    id_autor = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    livros = relationship('Livro', secondary=livro_autor, back_populates='autores')

def conectar_bd():
    engine = create_engine('sqlite:///biblioteca.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def desconectar_bd(session):
    session.close()
