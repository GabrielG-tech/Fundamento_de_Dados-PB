import requests
from bs4 import BeautifulSoup
import pandas as pd

def web_scrape_pokemon_data():
    """
    Extrai e processa dados de estatísticas de pokémons da geração 1 de um site da web.
    
    Returns:
        pandas.DataFrame: Um DataFrame contendo as estatísticas dos pokémons da geração 1.
    """
    url = "https://pokemondb.net/pokedex/stats/gen1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar a tabela de estatísticas
    table = soup.find('table', {'id': 'pokedex'})
    
    # Ler a tabela HTML com pandas
    df = pd.read_html(str(table))[0]
    
    return df

def info_data(df):
    """
    Processa o DataFrame de estatísticas dos pokémons e imprime várias informações.

    Args:
        df (pandas.DataFrame): O DataFrame contendo as estatísticas dos pokémons.

    Prints:
        Número de pokémons apresentados, tipo de pokémon mais comum, 
        pokémons com maior HP, maior Attack, maior Defence e maior Speed.
    """
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
