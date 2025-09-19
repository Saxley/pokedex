import os
import json

def save_pokemon_data_as_json(pokemon_data, output_dir):
    """
    Saves Pokémon data to a JSON file inside the 'pokedex' folder.

    Args:
        pokemon_data (dict): Dictionary containing the Pokémon data.
        output_dir (str): Base directory where the 'pokedex' folder will be created.
    """
    # Create the 'pokedex' folder if it doesn't exist
    pokedex_dir = os.path.join(output_dir, "pokedex")
    os.makedirs(pokedex_dir, exist_ok=True)

    # Create a JSON file with all the Pokémon information retrieved from the API
    pokemon_json_path = os.path.join(pokedex_dir, f"{pokemon_data['name'].lower()}.json")

    with open(pokemon_json_path, "w", encoding="utf-8") as json_file:
        json.dump(pokemon_data, json_file, ensure_ascii=False, indent=4)

    print(f"All Pokémon information saved in: {pokemon_json_path}")