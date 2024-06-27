from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import pandas as pd

PATH = 'AT\\'
CSV_NAME = 'olimpiadas.csv'
CSV_PATH = f'{PATH}{CSV_NAME}'
DB_NAME = 'olimpiadas'
DB_PATH = f'{PATH}{DB_NAME}.db'

# Carregar dados do CSV
df = pd.read_csv(CSV_PATH)

# Substituir os valores 'NA' de Medal para 'No Medal'
df['Medal'] = df['Medal'].fillna('No Medal')

# Substituir os valores 'NA' de Height e Weight pela média
mean_height = df[df['Height'].notna()]['Height'].round().mean()
mean_weight = df[df['Weight'].notna()]['Weight'].round().mean()

df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')

df['Height'] = df['Height'].fillna(mean_height)
df['Weight'] = df['Weight'].fillna(mean_weight)

df['Height'] = df['Height'].round().astype(int) / 100
df['Weight'] = df['Weight'].round(1).astype(int)

# Conexão com banco de dados SQLite
engine = create_engine(f'sqlite:///{DB_PATH}')
Base = declarative_base()

# Definição das classes de modelo
class Atleta(Base):
    __tablename__ = 'Atletas'
    ID_Atleta = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Sex = Column(String(1))
    Age = Column(Integer)
    Height = Column(Float)
    Weight = Column(Float)

    participacoes = relationship('Participacao', back_populates='atleta')

class Pais(Base):
    __tablename__ = 'Paises'
    ID_Pais = Column(Integer, primary_key=True, autoincrement=True)
    NOC = Column(String(3))
    Team = Column(String)

class Jogo(Base):
    __tablename__ = 'Jogos'
    ID_Game = Column(Integer, primary_key=True, autoincrement=True)
    Games = Column(String)
    Year = Column(Integer)
    Season = Column(String)

    eventos = relationship('Evento', back_populates='jogo')

class Evento(Base):
    __tablename__ = 'Eventos'
    ID_Evento = Column(Integer, primary_key=True, autoincrement=True)
    Event = Column(String)
    Sport = Column(String)
    City = Column(String)
    ID_Game = Column(Integer, ForeignKey('Jogos.ID_Game'))

    jogo = relationship('Jogo', back_populates='eventos')
    participacoes = relationship('Participacao', back_populates='evento')

class Participacao(Base):
    __tablename__ = 'Participacoes'
    ID_Participacoes = Column(Integer, primary_key=True, autoincrement=True)
    ID_Atleta = Column(Integer, ForeignKey('Atletas.ID_Atleta'))
    ID_Team = Column(Integer, ForeignKey('Paises.ID_Pais'))
    ID_Evento = Column(Integer, ForeignKey('Eventos.ID_Evento'))
    Medal = Column(String)

    atleta = relationship('Atleta', back_populates='participacoes')
    evento = relationship('Evento', back_populates='participacoes')
    pais = relationship('Pais')

# Criar todas as tabelas no banco de dados
Base.metadata.create_all(engine)

# Criar uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Preparando os objetos para inserção
atletas_objs = []
paises_objs = []
jogos_objs = []
eventos_objs = []
participacoes_objs = []

# Inserir dados nas tabelas
for index, row in df.iterrows():
    # Atletas
    atleta = Atleta(
        Name=row['Name'],
        Sex=row['Sex'],
        Age=row['Age'],
        Height=row['Height'],
        Weight=row['Weight']
    )
    atletas_objs.append(atleta)

    # Paises
    pais = Pais(
        NOC=row['NOC'],
        Team=row['Team']
    )
    paises_objs.append(pais)

    # Jogos
    jogo = Jogo(
        Games=row['Games'],
        Year=row['Year'],
        Season=row['Season']
    )
    jogos_objs.append(jogo)

    # Eventos
    evento = Evento(
        Event=row['Event'],
        Sport=row['Sport'],
        City=row['City'],
        jogo=jogo
    )
    eventos_objs.append(evento)

    # Participacoes
    participacao = Participacao(
        Medal=row['Medal'],
        atleta=atleta,
        pais=pais,
        evento=evento
    )
    participacoes_objs.append(participacao)

# Adicionar objetos à sessão e commit para o banco de dados
session.add_all(atletas_objs)
session.add_all(paises_objs)
session.add_all(jogos_objs)
session.add_all(eventos_objs)
session.add_all(participacoes_objs)
session.commit()

# Exemplo de consultas
def medalhas_por_pais():
    query = text("""
    SELECT
        P.NOC AS noc,
        SUM(CASE WHEN M.Medal = 'Gold' THEN 1 ELSE 0 END) AS Ouro,
        SUM(CASE WHEN M.Medal = 'Silver' THEN 1 ELSE 0 END) AS Prata,
        SUM(CASE WHEN M.Medal = 'Bronze' THEN 1 ELSE 0 END) AS Bronze,
        COUNT(M.Medal) AS Total_Medalhas
    FROM Paises P
    JOIN Participacoes M ON P.ID_Pais = M.ID_Team
    WHERE M.Medal != 'No Medal'
    GROUP BY P.NOC
    ORDER BY P.NOC;
    """)
    df_medalhas_paises = pd.read_sql(query, engine)
    return df_medalhas_paises

def participacoes_por_atleta():
    query = text("""
    SELECT A.Name, COUNT(P.ID_Participacoes) AS Total_Participacoes
    FROM Atletas A
    JOIN Participacoes P ON A.ID_Atleta = P.ID_Atleta
    GROUP BY A.Name
    ORDER BY Total_Participacoes DESC;
    """)
    df_participacoes_atletas = pd.read_sql(query, engine)
    return df_participacoes_atletas

# Exemplo de uso das funções
df_medalhas_paises = medalhas_por_pais()
df_participacoes_atletas = participacoes_por_atleta()

# # Salvar resultados como JSON
df_medalhas_paises.to_json(f'{PATH}medalhas_paises.json', orient='records', indent=4)
df_participacoes_atletas.to_json(f'{PATH}participacoes_atletas.json', orient='records', indent=4)

# Fechar a sessão após o uso
session.close()
