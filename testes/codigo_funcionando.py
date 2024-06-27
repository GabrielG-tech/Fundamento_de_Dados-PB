from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
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

# Arredondar valores de altura e peso
df['Height'] = pd.to_numeric(df['Height'], errors='coerce').round(2) / 100  # Transforma em metros
df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce').round(1)

# Substituir NaN por None na coluna Height e Weight
df['Height'] = df['Height'].where(pd.notnull(df['Height']), None)
df['Weight'] = df['Weight'].where(pd.notnull(df['Weight']), None)

# Conexão com banco de dados SQLite
engine = create_engine(f'sqlite:///{DB_PATH}')
Base = declarative_base()
print('Banco criado')

# Definição das classes de modelo
class Atleta(Base):
    __tablename__ = 'Atleta'
    ID_Atleta = Column(Integer, primary_key=True)
    Name = Column(String)
    Sex = Column(String(1))
    # Age = Column(Integer)
    Height = Column(Float)
    Weight = Column(Float)

    participacoes = relationship('Participacao', back_populates='atleta')

class Pais(Base):
    __tablename__ = 'Pais'
    ID_Pais = Column(Integer, primary_key=True, autoincrement=True)
    NOC = Column(String(3))
    Team = Column(String)

class Jogo(Base):
    __tablename__ = 'Jogo'
    ID_Jogo = Column(Integer, primary_key=True, autoincrement=True)
    Games = Column(String)
    Year = Column(Integer)
    Season = Column(String)

    eventos = relationship('Evento', back_populates='jogo')

class Evento(Base):
    __tablename__ = 'Evento'
    ID_Evento = Column(Integer, primary_key=True, autoincrement=True)
    Event = Column(String)
    Sport = Column(String)
    City = Column(String)
    ID_Jogo = Column(Integer, ForeignKey('Jogo.ID_Jogo'))

    jogo = relationship('Jogo', back_populates='eventos')
    participacoes = relationship('Participacao', back_populates='evento')

class Participacao(Base):
    __tablename__ = 'Participacao'
    ID_Participacao = Column(Integer, primary_key=True, autoincrement=True)
    ID_Atleta = Column(Integer, ForeignKey('Atleta.ID_Atleta'))
    ID_Team = Column(Integer, ForeignKey('Pais.ID_Pais'))
    ID_Evento = Column(Integer, ForeignKey('Evento.ID_Evento'))
    Age = Column(Integer)
    Medal = Column(String)

    atleta = relationship('Atleta', back_populates='participacoes')
    evento = relationship('Evento', back_populates='participacoes')
    pais = relationship('Pais')

# Criar todas as tabelas no banco de dados
Base.metadata.create_all(engine)
print("Tabelas criadas")

# Criar uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()
print("Sessão iniciada")

# Inserir dados nas tabelas
for index, row in df.iterrows():
    print(f"Processando linha {index + 1}/{len(df)}")
    # Inserir atleta se não existir
    atleta_existente = session.query(Atleta).filter_by(ID_Atleta=row['ID']).first()
    if not atleta_existente:
        atleta = Atleta(
            ID_Atleta=row['ID'],
            Name=row['Name'],
            Sex=row['Sex'],
            # Age=row['Age'],
            Height=row['Height'],
            Weight=row['Weight']
        )
        session.add(atleta)

    # Inserir país se não existir
    pais_existente = session.query(Pais).filter_by(Team=row['Team']).first()
    if pais_existente==None:
        pais = Pais(
            NOC=row['NOC'],
            Team=row['Team']
        )
        session.add(pais)
        session.flush()  # Para obter o ID_Pais gerado automaticamente
        session.commit()
        
    _id_pais = session.query(Pais).filter_by(Team=row['Team']).first().ID_Pais
    
    # Inserir jogo se não existir
    jogo_existente = session.query(Jogo).filter_by(Games=row['Games'], Year=row['Year'], Season=row['Season']).first()
    if not jogo_existente:
        jogo = Jogo(
            Games=row['Games'],
            Year=row['Year'],
            Season=row['Season']
        )
        session.add(jogo)
        session.flush()  # Para obter o ID_Jogo gerado automaticamente
    
    _id_jogo = session.query(Jogo).filter_by(Games=row['Games'], Year=row['Year'], Season=row['Season']).first().ID_Jogo

    # Inserir evento se não existir
    evento_existente = session.query(Evento).filter_by(Event=row['Event'], Sport=row['Sport'], City=row['City'], ID_Jogo=_id_jogo).first()
    if not evento_existente:
        evento = Evento(
            Event=row['Event'],
            Sport=row['Sport'],
            City=row['City'],
            ID_Jogo=_id_jogo
        )
        session.add(evento)
        session.flush()  # Para obter o ID_Evento gerado automaticamente
    
    _id_evento = session.query(Evento).filter_by(Event=row['Event'], Sport=row['Sport'], City=row['City'], ID_Jogo=_id_jogo).first().ID_Evento

    # Inserir participação
    participacao = Participacao(
        ID_Atleta=row['ID'],
        ID_Team=_id_pais,
        ID_Evento=_id_evento,
        Age=row['Age'],
        Medal=row['Medal']
    )
    session.add(participacao)
    

# Commitar todas as mudanças no final
session.commit()
print("Commit realizado")

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

df_medalhas_paises = medalhas_por_pais()
df_participacoes_atletas = participacoes_por_atleta()

# Salvar resultados como JSON
df_medalhas_paises.to_json(f'{PATH}Arquivos_json\\medalhas_paises.json', orient='records', indent=4)
df_participacoes_atletas.to_json(f'{PATH}Arquivos_json\\participacoes_atletas.json', orient='records', indent=4)

session.close()