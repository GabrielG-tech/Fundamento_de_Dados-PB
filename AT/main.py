import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float

PATH = 'AT\\'
CSV_NAME = 'olimpiadas.csv'
CSV_PATH = f'{PATH}{CSV_NAME}' 
DB_NAME = 'olimpiadas'
DB_PATH = f'{PATH}{DB_NAME}.db'

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

# definir as tabelas conforme o modelo físico
atletas = Table('Atletas', metadata,
    Column('ID', Integer, primary_key=True),
    Column('Name', String),
    Column('Sex', String(1)),
    Column('Age', Integer),
    Column('Height', Float),
    Column('Weight', Float),
    Column('Team', String, ForeignKey('Paises.Team')),
)

paises = Table('Paises', metadata,
    Column('Team', String, primary_key=True),
    Column('NOC', String(3))
)

jogos_olimpicos = Table('JogosOlimpicos', metadata,
    Column('Games', String, primary_key=True),
    Column('Year', Integer),
    Column('Season', String),
    Column('City', String)
)

esportes = Table('Esportes', metadata,
    Column('Sport', String, primary_key=True)
)

eventos = Table('Eventos', metadata,
    Column('Event', String, primary_key=True),
    Column('Sport', String, ForeignKey('Esportes.Sport'))
)

medalhas = Table('Medalhas', metadata,
    Column('ID', Integer, ForeignKey('Atletas.ID')),
    Column('Name', Integer, ForeignKey('Atletas.Name')),
    Column('Games', String, ForeignKey('JogosOlimpicos.Games')),
    Column('Event', String, ForeignKey('Eventos.Event')),
    Column('Medal', String)
)

participacao = Table('Participacao', metadata,
    Column('ID', Integer, ForeignKey('Atletas.ID')),
    Column('Event', String, ForeignKey('Eventos.Event'))
)

# Criar todas as tabelas no banco de dados
metadata.create_all(engine)

df_atletas = df[['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight']].drop_duplicates(subset=['ID'])

df_medalhas = df[['ID', 'Name', 'Games', 'Event', 'Medal']]

df_jogos = df[['Games', 'Year', 'Season', 'City']]

df_paises = df[['NOC', 'Team']].drop_duplicates(subset=['Team'])

df_eventos = df[['Event', 'Sport']].drop_duplicates(subset=['Event'])

df_esportes = df[['Sport']].drop_duplicates()

df_participacao = df[['ID', 'Event']]


print('Erro ao Inserir tabelas [Teste]')
# Carregar dados nas tabelas
df_atletas.to_sql('Atletas', con=engine, if_exists='replace', index=False)
df_medalhas.to_sql('Medalhas', con=engine, if_exists='replace', index=False)
df_paises.to_sql('Paises', con=engine, if_exists='replace', index=False)
df_jogos.to_sql('JogosOlimpicos', con=engine, if_exists='replace', index=False)
df_esportes.to_sql('Esportes', con=engine, if_exists='replace', index=False)
df_eventos.to_sql('Eventos', con=engine, if_exists='replace', index=False)
df_participacao.to_sql('Participacao', con=engine, if_exists='replace', index=False)


# Consultas SQL
query_medalhas_por_pais = """
SELECT
    p.Team AS Pais,
    SUM(CASE WHEN m.Medal = 'Gold' THEN 1 ELSE 0 END) AS Ouro,
    SUM(CASE WHEN m.Medal = 'Silver' THEN 1 ELSE 0 END) AS Prata,
    SUM(CASE WHEN m.Medal = 'Bronze' THEN 1 ELSE 0 END) AS Bronze
FROM
    Medalhas m
JOIN
    Atletas a ON m.ID = a.ID
JOIN
    Paises p ON a.Team = p.Team
GROUP BY
    p.Team
ORDER BY
    p.Team
"""

query_medalhas_por_atleta = """
SELECT
    a.Name AS Atleta,
    COUNT(m.Medal) AS Total_Medalhas
FROM
    Medalhas m
JOIN
    Atletas a ON m.ID = a.ID
GROUP BY
    a.Name
ORDER BY
    Total_Medalhas DESC, a.Name
"""

# Executar consultas e tratar erros
try:
    df_medalhas_por_pais = pd.read_sql(query_medalhas_por_pais, engine)
    print(df_medalhas_por_pais)
except Exception as e:
    print(f"Erro ao executar query_medalhas_por_pais: {str(e)}")

try:
    df_medalhas_por_atleta = pd.read_sql(query_medalhas_por_atleta, engine)
    print(df_medalhas_por_atleta)
except Exception as e:
    print(f"Erro ao executar query_medalhas_por_atleta: {str(e)}")