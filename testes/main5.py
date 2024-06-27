from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, Float, ForeignKey, text
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

# Substituir os valores 'NA' de Age para '-'
df['Age'] = df['Age'].fillna('-')

# Substituir os valores 'NA' de Height e Weight por "Não definido"
df['Height'] = df['Height'].fillna('Não definido')
df['Weight'] = df['Weight'].fillna('Não definido')

# Conexão com banco de dados SQLite
engine = create_engine(f'sqlite:///{DB_PATH}')
metadata = MetaData()

# Definindo as tabelas
atletas = Table(
    'Atletas', metadata,
    Column('ID_Atleta', Integer, primary_key=True, autoincrement=True),
    Column('Name', String),
    Column('Sex', String(1)),
    Column('Age', Integer),
    Column('Height', Float),
    Column('Weight', Float)
)

paises = Table(
    'Paises', metadata,
    Column('ID_Pais', Integer, primary_key=True, autoincrement=True),
    Column('NOC', String(3)),
    Column('Team', String)
)

jogos = Table(
    'Jogos', metadata,
    Column('ID_Game', Integer, primary_key=True, autoincrement=True),
    Column('Games', String),
    Column('Year', Integer),
    Column('Season', String)
)

eventos = Table(
    'Eventos', metadata,
    Column('ID_Evento', Integer, primary_key=True, autoincrement=True),
    Column('Event', String),
    Column('Sport', String),
    Column('City', String),
    Column('ID_Game', Integer, ForeignKey('Jogos.ID_Game'))
)

participacoes = Table(
    'Participacoes', metadata,
    Column('ID_Participacoes', Integer, primary_key=True, autoincrement=True),
    Column('ID_Atleta', Integer, ForeignKey('Atletas.ID_Atleta')),
    Column('ID_Team', Integer, ForeignKey('Paises.ID_Pais')),
    Column('ID_Evento', Integer, ForeignKey('Eventos.ID_Evento')),
    Column('Medal', String)
)

# Criar todas as tabelas no banco de dados
metadata.create_all(engine)

# Preparando os DataFrames
atletas_df = df[['Name', 'Sex', 'Age', 'Height', 'Weight']].drop_duplicates().reset_index(drop=True)
paises_df = df[['NOC', 'Team']].drop_duplicates().reset_index(drop=True)
jogos_df = df[['Games', 'Year', 'Season']].drop_duplicates().reset_index(drop=True)

eventos_df = df[['Event', 'Sport', 'City', 'Games']].drop_duplicates().reset_index(drop=True)
eventos_df = eventos_df.merge(jogos_df.reset_index(), left_on='Games', right_on='Games')
eventos_df = eventos_df.rename(columns={'index': 'ID_Game'})[['Event', 'ID_Game']]

participacoes_df = df[['Name', 'NOC', 'Event', 'Medal']]
participacoes_df = participacoes_df.merge(atletas_df.reset_index(), left_on='Name', right_on='Name')
participacoes_df = participacoes_df.merge(paises_df.reset_index(), left_on='NOC', right_on='NOC')
participacoes_df = participacoes_df.merge(eventos_df.reset_index(), left_on='Event', right_on='Event')
participacoes_df = participacoes_df.rename(columns={'index': 'ID_Atleta', 'index_x': 'ID_Team', 'index_y': 'ID_Evento'})[['ID_Atleta', 'ID_Team', 'ID_Evento', 'Medal']]

conn = engine.connect()

# Inserindo DataFrames no Banco
atletas_df.to_sql('Atletas', conn, if_exists='replace', index=False)
paises_df.to_sql('Paises', conn, if_exists='replace', index=False)
jogos_df.to_sql('Jogos', conn, if_exists='replace', index=False)
eventos_df.to_sql('Eventos', conn, if_exists='replace', index=False)
participacoes_df.to_sql('Participacoes', conn, if_exists='replace', index=False)

conn.close()

def medalhas_por_pais():
    query = text("""
    SELECT
        P.NOC AS NOC,
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

def participacoes_medalhas_por_atleta():
    query = text("""
    SELECT A.Name,
            P.NOC AS NOC,
            SUM(CASE WHEN P.Medal = 'Gold' THEN 1 ELSE 0 END) AS Ouro,
            SUM(CASE WHEN P.Medal = 'Silver' THEN 1 ELSE 0 END) AS Prata,
            SUM(CASE WHEN P.Medal = 'Bronze' THEN 1 ELSE 0 END) AS Bronze,
            COUNT(P.ID_Participacoes) AS Total_Participacoes
    FROM Atletas A
    JOIN Participacoes P ON A.ID_Atleta = P.ID_Atleta
    WHERE P.Medal != 'No Medal'
    GROUP BY A.Name
    ORDER BY Total_Participacoes DESC;
    """)
    df_participacoes_medalhas_por_atleta = pd.read_sql(query, engine)
    return df_participacoes_medalhas_por_atleta

df_medalhas_paises = medalhas_por_pais()
df_participacoes_medalhas_por_atleta = participacoes_medalhas_por_atleta()

# Salvar resultados como JSON
df_medalhas_paises.to_json(f'{PATH}Arquivos_json\\medalhas_paises.json', orient='records', indent=4)
df_participacoes_medalhas_por_atleta.to_json(f'{PATH}Arquivos_json\\participacoes_medalhas_por_atleta.json', orient='records', indent=4)
