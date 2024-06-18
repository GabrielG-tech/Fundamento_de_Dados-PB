from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Associação muitos para muitos
livro_autor = Table('livro_autor', Base.metadata,
    Column('id_livro', Integer, ForeignKey('livro.id_livro')),
    Column('id_autor', Integer, ForeignKey('autor.id_autor'))
)

class Livro(Base):
    """
    Classe que representa a tabela 'livro' no banco de dados.

    Atributos:
        id_livro (int): ID do livro.
        titulo (str): Título do livro.
        data_lancamento (date): Data de lançamento do livro.
        preco (float): Preço do livro.
        autores (list): Lista de autores associados ao livro.
    """
    __tablename__ = 'livro'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    data_lancamento = Column(Date, nullable=False)
    preco = Column(Float, nullable=False)
    autores = relationship('Autor', secondary=livro_autor, back_populates='livros')

class Autor(Base):
    """
    Classe que representa a tabela 'autor' no banco de dados.

    Atributos:
        id_autor (int): ID do autor.
        nome (str): Nome do autor.
        sobrenome (str): Sobrenome do autor.
        livros (list): Lista de livros associados ao autor.
    """
    __tablename__ = 'autor'
    id_autor = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    livros = relationship('Livro', secondary=livro_autor, back_populates='autores')

def conectar_bd():
    """
    Conecta ao banco de dados SQLite 'biblioteca.db' e retorna uma sessão.

    Returns:
        Session: Sessão do SQLAlchemy para interagir com o banco de dados.
    """
    engine = create_engine('sqlite:///biblioteca.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def desconectar_bd(session):
    """
    Fecha a sessão do banco de dados.

    Args:
        session (Session): Sessão do SQLAlchemy a ser fechada.
    """
    session.close()
