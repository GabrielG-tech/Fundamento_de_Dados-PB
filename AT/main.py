from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float, func, select
import pandas as pd

PATH = 'AT\\'
CSV_NAME = 'olimpiadas.csv'
CSV_PATH = f'{PATH}{CSV_NAME}' 
DB_NAME = 'olimpiadas'
DB_PATH = f'{PATH}{DB_NAME}.db'

# Carregar dados do CSV
df = pd.read_csv(CSV_PATH)

# substituir os valores 'NA' de Medal para 'No Medal'
df['Medal'] = df['Medal'].fillna('No Medal')

# substituir os valores 'NA' de Height e Weight pela média
mean_height = df[df['Height'].notna()]['Height'].round().mean()
mean_weight = df[df['Weight'].notna()]['Weight'].round().mean()

df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')

df['Height'] = df['Height'].fillna(mean_height)
df['Weight'] = df['Weight'].fillna(mean_weight)

df['Height'] = df['Height'].round().astype(int) / 100
df['Weight'] = df['Weight'].round(1).astype(int)

# conexão com banco de dados SQLite
engine = create_engine('sqlite:///AT/olimpiadas.db')
metadata = MetaData()

# mapeamento das tabelas
atletas = Table('Atletas', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Name', String),
    Column('Sex', String(1)),
    Column('Age', Integer),
    Column('Height', Float),
    Column('Weight', Float),
    Column('Team', String, ForeignKey('Paises.Team')),
)

paises = Table('Paises', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Team', String),
    Column('NOC', String(3))
)

jogos_olimpicos = Table('JogosOlimpicos', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Games', String),
    Column('Year', Integer),
    Column('Season', String),
    Column('City', String)
)

esportes = Table('Esportes', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Sport', String)
)

eventos = Table('Eventos', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Event', String),
    Column('Sport', String, ForeignKey('Esportes.Sport'))
)

medalhas = Table('Medalhas', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Name', Integer, ForeignKey('Atletas.ID')),
    Column('Games', String, ForeignKey('JogosOlimpicos.Games')),
    Column('Event', String, ForeignKey('Eventos.Event')),
    Column('Medal', String)
)

participacao = Table('Participacao', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('Name.Atleta', Integer, ForeignKey('Atletas.Name')),
    Column('ID.Evento', Integer, ForeignKey('Eventos.ID'))
)

# Criar todas as tabelas no banco de dados
metadata.create_all(engine)

# Carregar dados nas tabelas
df_atletas = df[['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight']].drop_duplicates(subset=['ID'])
df_medalhas = df[['ID', 'Name', 'Games', 'Event', 'Medal']]
df_paises = df[['NOC', 'Team']].drop_duplicates(subset=['Team'])
df_jogos = df[['Games', 'Year', 'Season', 'City']].drop_duplicates()
df_esportes = df[['Sport']].drop_duplicates()
df_eventos = df[['Event', 'Sport']].drop_duplicates(subset=['Event'])
df_participacao = df[['ID', 'Name', 'Event']]

df_atletas.to_sql('Atletas', con=engine, if_exists='replace', index=False)
df_medalhas.to_sql('Medalhas', con=engine, if_exists='replace', index=False)
df_paises.to_sql('Paises', con=engine, if_exists='replace', index=False)
df_jogos.to_sql('JogosOlimpicos', con=engine, if_exists='replace', index=False)
df_esportes.to_sql('Esportes', con=engine, if_exists='replace', index=False)
df_eventos.to_sql('Eventos', con=engine, if_exists='replace', index=False)
df_participacao.to_sql('Participacao', con=engine, if_exists='replace', index=False)

def medalhas_por_pais():
    query = """
    SELECT
        P.NOC AS noc,
        SUM(CASE WHEN M.Medal = 'Gold' THEN 1 ELSE 0 END) AS Ouro,
        SUM(CASE WHEN M.Medal = 'Silver' THEN 1 ELSE 0 END) AS Prata,
        SUM(CASE WHEN M.Medal = 'Bronze' THEN 1 ELSE 0 END) AS Bronze,
        COUNT(M.Medal) AS Total_Medalhas
    FROM Paises P
    LEFT JOIN Atletas A ON P.Team = A.Team
    LEFT JOIN Medalhas M ON A.ID = M.Name
    WHERE M.Medal != 'No Medal'
    GROUP BY P.NOC
    ORDER BY P.NOC;
    """
    df_medalhas_paises = pd.read_sql(query, engine)
    return df_medalhas_paises

def participacoes_por_atleta():
    query = """
    SELECT A.Name, COUNT(P.ID) AS Total_Participacoes
    FROM Atletas A
    LEFT JOIN Participacao P ON A.ID = P.ID_Atleta
    GROUP BY A.Name
    ORDER BY Total_Participacoes DESC
    """
    df_participacoes_atletas = pd.read_sql(query, engine)
    return df_participacoes_atletas


df_medalhas_paises = medalhas_por_pais()
# df_participacoes_atletas = participacoes_por_atleta()

# DataFrame para Json
medalhas_paises_json = df_medalhas_paises.to_json(orient='records', indent=4)
# participacoes_atletas_json = df_participacoes_atletas.to_json(orient='records', indent=4)

# Salvar Json's
with open(f'{PATH}medalhas_paises.json', 'w') as arquivo:
    arquivo.write(medalhas_paises_json)

# with open(f'{PATH}participacoes_atletas.json', 'w') as arquivo:
#     arquivo.write(participacoes_atletas_json)
