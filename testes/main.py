from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float, text
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
metadata = MetaData()

# Mapeamento das tabelas
atletas = Table('Atletas', metadata,
    Column('ID_Atleta', Integer, primary_key=True, autoincrement=True),
    Column('Name', String),
    Column('Sex', String(1)),
    Column('Age', Integer),
    Column('Height', Float),
    Column('Weight', Float)
)

paises = Table('Paises', metadata,
    Column('ID_Pais', Integer, primary_key=True, autoincrement=True),
    Column('NOC', String(3)),
    Column('Team', String)
)

jogos = Table('Jogos', metadata,
    Column('ID_Game', Integer, primary_key=True, autoincrement=True),
    Column('Games', String),
    Column('Year', Integer),
    Column('Season', String)
)

eventos = Table('Eventos', metadata,
    Column('ID_Evento', Integer, primary_key=True, autoincrement=True),
    Column('Event', String),
    Column('Sport', String),
    Column('City', String),
    Column('ID_Game', Integer, ForeignKey('Jogos.ID_Game'))
)

participacoes = Table('Participacoes', metadata,
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

# Inserindo dados na tabela 'Jogos' para obter os IDs
jogos_df.to_sql('Jogos', engine, if_exists='replace', index=False)

# Verificar a estrutura da tabela 'Jogos' após a criação
print(pd.read_sql('PRAGMA table_info(Jogos)', engine))

# Mapeando o ID_Game para a tabela Eventos
jogos_ids = pd.read_sql('SELECT ID_Game FROM Jogos', engine)
eventos_df = df[['Event', 'Sport', 'City', 'Games']].drop_duplicates().reset_index(drop=True)
eventos_df = eventos_df.merge(jogos_ids, on='Games', how='left')
eventos_df = eventos_df.drop(columns=['Games'])

# Inserindo dados nas tabelas 'Atletas', 'Paises' e 'Eventos'
atletas_df.to_sql('Atletas', engine, if_exists='replace', index=False)
paises_df.to_sql('Paises', engine, if_exists='replace', index=False)
eventos_df.to_sql('Eventos', engine, if_exists='replace', index=False)

# Preparando o DataFrame de Participacoes
atletas_ids = pd.read_sql('SELECT ID_Atleta, Name FROM Atletas', engine)
paises_ids = pd.read_sql('SELECT ID_Pais, NOC FROM Paises', engine)
eventos_ids = pd.read_sql('SELECT ID_Evento, Event FROM Eventos', engine)

participacoes_df = df[['Name', 'NOC', 'Event', 'Medal']]
participacoes_df = participacoes_df.merge(atletas_ids, on='Name', how='left')
participacoes_df = participacoes_df.merge(paises_ids, on='NOC', how='left')
participacoes_df = participacoes_df.merge(eventos_ids, on='Event', how='left')
participacoes_df = participacoes_df[['ID_Atleta', 'ID_Pais', 'ID_Evento', 'Medal']]

# Inserindo dados na tabela 'Participacoes'
participacoes_df.to_sql('Participacoes', engine, if_exists='replace', index=False)

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

# df_medalhas_paises = medalhas_por_pais()
# df_participacoes_atletas = participacoes_por_atleta()

# # DataFrame para Json
# medalhas_paises_json = df_medalhas_paises.to_json(orient='records', indent=4)
# participacoes_atletas_json = df_participacoes_atletas.to_json(orient='records', indent=4)

# # Salvar Json's
# with open(f'{PATH}medalhas_paises.json', 'w') as arquivo:
#     arquivo.write(medalhas_paises_json)

# with open(f'{PATH}participacoes_atletas.json', 'w') as arquivo:
#     arquivo.write(participacoes_atletas_json)
