import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float

df = pd.read_csv('AT\\olimpiadas.csv')

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
    Column('Weight', Float)
)

paises = Table('Paises', metadata,
    Column('NOC', String(3), primary_key=True),
    Column('Team', String)
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
    Column('ID_Atleta', Integer, ForeignKey('Atletas.ID')),
    Column('Games', String, ForeignKey('JogosOlimpicos.Games')),
    Column('Event', String, ForeignKey('Eventos.Event')),
    Column('Medal', String)
)

# Criar todas as tabelas no banco de dados
metadata.create_all(engine)

# Remover duplicatas baseadas na coluna 'ID' e garantir unicidade dos IDs
df_atletas = df[['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight']].drop_duplicates(subset=['ID'])

# Verificar duplicidade de IDs já presentes no banco de dados
with engine.connect() as connection:
    existing_ids = pd.read_sql('SELECT ID FROM Atletas', connection)['ID'].tolist()
    df_atletas = df_atletas[~df_atletas['ID'].isin(existing_ids)]

# Países
df_paises = df[['NOC', 'Team']].drop_duplicates()

# Jogos Olímpicos
df_jogos = df[['Games', 'Year', 'Season', 'City']].drop_duplicates()

# Verificar se os jogos olímpicos já existem na tabela antes de inserir
with engine.connect() as connection:
    existing_games = pd.read_sql('SELECT Games FROM JogosOlimpicos', connection)['Games'].tolist()
    df_jogos = df_jogos[~df_jogos['Games'].isin(existing_games)]

# Esportes
df_esportes = df[['Sport']].drop_duplicates()

# Eventos
df_eventos = df[['Event', 'Sport']].drop_duplicates()

# Medalhas
df_medalhas = df[['ID', 'Games', 'Event', 'Medal']].drop_duplicates()

# Carregar dados nas tabelas
df_atletas.to_sql('Atletas', con=engine, if_exists='append', index=False)
df_paises.to_sql('Paises', con=engine, if_exists='append', index=False)
df_jogos.to_sql('JogosOlimpicos', con=engine, if_exists='append', index=False)
df_esportes.to_sql('Esportes', con=engine, if_exists='append', index=False)
df_eventos.to_sql('Eventos', con=engine, if_exists='append', index=False)
df_medalhas.to_sql('Medalhas', con=engine, if_exists='append', index=False)

# Query para obter os totais de medalhas (ouro, prata e bronze) por país
query_medalhas_por_pais = """
SELECT
    p.Team AS Pais,
    SUM(CASE WHEN m.Medal = 'Gold' THEN 1 ELSE 0 END) AS Ouro,
    SUM(CASE WHEN m.Medal = 'Silver' THEN 1 ELSE 0 END) AS Prata,
    SUM(CASE WHEN m.Medal = 'Bronze' THEN 1 ELSE 0 END) AS Bronze
FROM
    Medalhas m
JOIN
    Atletas a ON m.ID_Atleta = a.ID
JOIN
    Paises p ON a.NOC = p.NOC
GROUP BY
    p.Team
ORDER BY
    p.Team
"""

# Query para encontrar atletas que ganharam mais de uma medalha em um único evento
query_atletas_multiplas_medalhas = """
SELECT
    a.Name AS Atleta,
    a.Sex AS Sexo,
    a.Team AS Time,
    e.Event AS Evento,
    COUNT(m.Medal) AS Total_Medalhas
FROM
    Medalhas m
JOIN
    Atletas a ON m.ID_Atleta = a.ID
JOIN
    Eventos e ON m.Event = e.Event
JOIN
    Paises p ON a.NOC = p.NOC
GROUP BY
    a.Name, a.Sex, p.Team, e.Event
HAVING
    COUNT(m.Medal) > 1
ORDER BY
    Total_Medalhas DESC, a.Name
"""

# Executando a primeira consulta
df_medalhas_por_pais = pd.read_sql(query_medalhas_por_pais, engine)
print(df_medalhas_por_pais)

# Executando a segunda consulta
df_atletas_multiplas_medalhas = pd.read_sql(query_atletas_multiplas_medalhas, engine)
print(df_atletas_multiplas_medalhas)
