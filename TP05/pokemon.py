import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para extrair e processar os dados da página
def web_scrape_pokemon_data():
    url = "https://pokemondb.net/pokedex/stats/gen1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar a tabela de estatísticas
    table = soup.find('table', {'id': 'pokedex'})
    
    # Ler a tabela HTML com pandas
    df = pd.read_html(str(table))[0]
    
    return df

# Função para responder todas as perguntas
def info_data(df):
    # 1. Número de pokémons apresentados
    num_pokemons = len(df)
    
    # 2. Tipo de pokémon mais comum
    types = df['Type']
    most_common_type = types.value_counts().idxmax()
    
    # 3. Pokémons com maior HP
    max_hp = df[df['HP'] == df['HP'].max()]
    
    # 4. Pokémons com maior Attack
    max_attack = df[df['Attack'] == df['Attack'].max()]
    
    # 5. Pokémons com maior Defence
    max_defence = df[df['Defense'] == df['Defense'].max()]
    
    # 6. Pokémons com maior Speed
    max_speed = df[df['Speed'] == df['Speed'].max()]
    
    # Resultados
    print(f"1. Número de pokémons apresentados: {num_pokemons}")
    print(f"2. Tipo de pokémon mais comum: {most_common_type}")
    print(f"3. Pokémons com maior HP:\n{max_hp[['Name', 'HP']]}")
    print(f"4. Pokémons com maior Attack:\n{max_attack[['Name', 'Attack']]}")
    print(f"5. Pokémons com maior Defence:\n{max_defence[['Name', 'Defense']]}")
    print(f"6. Pokémons com maior Speed:\n{max_speed[['Name', 'Speed']]}")

df = web_scrape_pokemon_data()
info_data(df)
