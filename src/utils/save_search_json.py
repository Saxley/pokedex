import os
import json

def save_pokemon_data_as_json(pokemon_data, output_dir):
    """
    Guarda los datos de un Pokémon en un archivo JSON dentro de la carpeta 'pokedex'.

    Args:
        pokemon_data (dict): Diccionario con los datos del Pokémon.
        output_dir (str): Directorio base donde se guardará la carpeta 'pokedex'.
    """
    # Crear la carpeta 'pokedex' si no existe
    pokedex_dir = os.path.join(output_dir, "pokedex")
    os.makedirs(pokedex_dir, exist_ok=True)

    # Crear un archivo JSON con toda la información del Pokémon obtenida de la API
    pokemon_json_path = os.path.join(pokedex_dir, f"{pokemon_data['name'].lower()}.json")

    with open(pokemon_json_path, "w", encoding="utf-8") as json_file:
        json.dump(pokemon_data, json_file, ensure_ascii=False, indent=4)

    print(f"Toda la información del Pokémon guardada en: {pokemon_json_path}")