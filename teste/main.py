import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import *

PATH = 'AT\\'
CSV_NAME = 'olimpiadas.csv'
CSV_PATH = f'{PATH}{CSV_NAME}' 
DB_NAME = 'olimpiadas'
DB_PATH = f'{PATH}{DB_NAME}.db'

def conectar_db(DB_PATH):
    engine = create_engine(f'sqlite:///{DB_PATH}')
    Base.metadata.create_all(engine)  # Cria as tabelas se ainda não existirem
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session

def exportar_db(df, table_name, session):
    try:
        df.to_sql(table_name, session.get_bind(), if_exists='replace', index=False)
        print(f"Dados exportados para a tabela '{table_name}' com sucesso!")
    except Exception as e:
        print(f'Erro ao exportar para o banco de dados: {e}')

def carregar_dados(df, session):
    # Preenchendo valores nulos em Height e Weight
    df['Height'] = df['Height'].fillna(df['Height'].mean()).round(2)
    df['Weight'] = df['Weight'].fillna(df['Weight'].mean()).round(2)
    
    # Transformando altura de centímetros para metros
    df['Height'] = df['Height'] / 100

    # Substituindo valores nulos, NA ou vazios em Medal por "No Medal"
    df['Medal'] = df['Medal'].fillna('No Medal')
    df['Medal'] = df['Medal'].replace(['NA', '', None], 'No Medal')

    atletas = df[['Name', 'Sex', 'Height', 'Weight', 'Team']].drop_duplicates().reset_index(drop=True)
    paises = df[['Team']].drop_duplicates().reset_index(drop=True)
    eventos = df[['Event', 'Year', 'Sport', 'City']].drop_duplicates().reset_index(drop=True)
    medalhas = df[['Medal']].drop_duplicates().reset_index(drop=True)

    # Inserção de dados normalizados nas tabelas
    for _, row in atletas.iterrows():
        pais = session.query(Pais).filter_by(nome=row['Team']).first()
        if pais:
            pais_id = pais.id
            session.add(Atleta(nome=row['Name'], sexo=row['Sex'], altura=row['Height'], peso=row['Weight'], pais_id=pais_id))
        else:
            print(f"País '{row['Team']}' não encontrado na base de dados. Atleta '{row['Name']}' não foi inserido.")

    for _, row in paises.iterrows():
        pais_existe = session.query(Pais).filter_by(nome=row['Team']).first()
        if not pais_existe:
            session.add(Pais(nome=row['Team']))

    for _, row in eventos.iterrows():
        esporte = session.query(Esporte).filter_by(nome=row['Sport']).first()
        if not esporte:
            esporte = Esporte(nome=row['Sport'])
            session.add(esporte)
            session.commit()
        jogos = Jogos(ano=row['Year'], temporada='Summer' if row['Year'] % 4 == 0 else 'Winter', cidade=row['City'])
        session.add(jogos)
        session.commit()
        session.add(Evento(nome=row['Event'], esporte_id=esporte.id, jogos_id=jogos.id))

    for _, row in medalhas.iterrows():
        session.add(Medalha(tipo=row['Medal']))

    session.commit()

    # Inserção das participações
    for _, row in df.iterrows():
        atleta = session.query(Atleta).filter_by(nome=row['Name']).first()
        if atleta:
            evento = session.query(Evento).filter_by(nome=row['Event']).first()
            if evento:
                jogos = session.query(Jogos).filter_by(ano=row['Year']).first()
                if jogos:
                    session.add(Participacao(id_atleta=atleta.id, id_evento=evento.id, id_jogos=jogos.id, medalha=row['Medal']))
                else:
                    print(f"Jogos não encontrados para o ano '{row['Year']}'. Participação do atleta '{row['Name']}' não foi inserida.")
            else:
                print(f"Evento '{row['Event']}' não encontrado na base de dados. Participação do atleta '{row['Name']}' não foi inserida.")
        else:
            print(f"Atleta '{row['Name']}' não encontrado na base de dados. Participação não foi inserida.")

    session.commit()

def consultar_totais_medalhas_pais(session):
    query = session.query(
        Pais.nome,
        Medalha.tipo,
        func.count(Participacao.id_atleta).label('total')
    ).join(Atleta, Atleta.pais_id == Pais.id) \
    .join(Participacao, Participacao.id_atleta == Atleta.id) \
    .join(Medalha, Medalha.id == Participacao.medalha) \
    .group_by(Pais.nome, Medalha.tipo) \
    .order_by(Pais.nome)

    df = pd.read_sql(query.statement, session.get_bind())
    return df

def consultar_medalhas_atleta(session):
    query = session.query(
        Atleta.nome,
        Medalha.tipo,
        func.count(Participacao.id_atleta).label('total')
    ).join(Participacao, Participacao.id_atleta == Atleta.id) \
    .join(Medalha, Medalha.id == Participacao.medalha) \
    .group_by(Atleta.nome, Medalha.tipo) \
    .order_by(Atleta.nome)

    df = pd.read_sql(query.statement, session.get_bind())
    return df

def salvar_json(df, filename):
    df.to_json(filename, orient='records', indent=4)
    print(f"Dados salvos em '{filename}' com sucesso!")

# Carregar o arquivo CSV
df = pd.read_csv(CSV_PATH)

# Configurar a conexão com o banco de dados SQLite
engine, session = conectar_db(DB_PATH)

# Exportar DataFrame para o SQLite
exportar_db(df, DB_NAME, session)

# Carregar dados no banco de dados
carregar_dados(df, session)

# Realizar consultas
df1 = consultar_totais_medalhas_pais(session)
df2 = consultar_medalhas_atleta(session)

# Verificar o conteúdo dos dataframes antes de salvar
print("DataFrame 1 (Totais de Medalhas por País):")
print(df1.head())
print("\nDataFrame 2 (Medalhas por Atleta):")
print(df2.head())

# Salvar resultados em JSON
salvar_json(df1, f'{PATH}totais_medalhas_paises.json')
salvar_json(df2, f'{PATH}medalhas_atletas.json')
