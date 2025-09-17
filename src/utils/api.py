import requests

# Función para obtener los datos de un Pokémon desde la PokéAPI
def fetch_pokemon_data(pokemon_name):
    """Obtiene los datos de un Pokémon desde la PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            "image_url": data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "weight": data["weight"] / 10,  # Convertir a kilogramos
            "height": data["height"] / 10,  # Convertir a metros
            "moves": [move["move"]["name"] for move in data["moves"]],
        }
    return None

# Función para obtener la cadena de evoluciones de un Pokémon
def fetch_evolution_chain(pokemon_name):
    """Obtiene la cadena de evoluciones de un Pokémon."""
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
    species_response = requests.get(species_url)
    if species_response.status_code == 200:
        species_data = species_response.json()
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_chain_url)
        if evolution_response.status_code == 200:
            evolution_data = evolution_response.json()
            chain = evolution_data["chain"]
            evolutions = []

            # Función interna para extraer las evoluciones
            def extract_evolutions(chain):
                evolutions.append({
                    "name": chain["species"]["name"],
                    "image_url": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{chain['species']['url'].split('/')[-2]}.png"
                })
                for evo in chain.get("evolves_to", []):
                    extract_evolutions(evo)

            extract_evolutions(chain)
            return evolutions
    return []

# Función para obtener los datos de un movimiento desde la PokéAPI
def fetch_move_data(move_name):
    """Obtiene los datos de un movimiento desde la PokéAPI."""
    url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "power": data.get("power", 0) or 0,  # Asegurar que el poder sea 0 si es None
            "effect": data["effect_entries"][0]["short_effect"] if data["effect_entries"] else "No hay descripción del efecto."
        }
    return None
