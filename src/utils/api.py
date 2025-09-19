import requests

# Function to fetch Pokémon data from the PokéAPI
def fetch_pokemon_data(pokemon_name):
    """Fetches Pokémon data from the PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200: #Status
        data = response.json()
        return {
            "name": data["name"],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            "image_url": data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "weight": data["weight"] / 10,  # Convert to kilograms
            "height": data["height"] / 10,  # Convert to meters
            "moves": [move["move"]["name"] for move in data["moves"]],
        }
    return None

# Function to fetch the evolution chain of a Pokémon
def fetch_evolution_chain(pokemon_name):
    """Fetches the evolution chain of a Pokémon."""
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
    species_response = requests.get(species_url)
    if species_response.status_code == 200: #Status
        species_data = species_response.json()
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_chain_url)
        if evolution_response.status_code == 200: #Status
            evolution_data = evolution_response.json()
            chain = evolution_data["chain"]
            evolutions = []

            # Internal function to extract evolutions
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

# Function to fetch move data from the PokéAPI
def fetch_move_data(move_name):
    """Fetches move data from the PokéAPI."""
    url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200: #Status
        data = response.json()
        return {
            "name": data["name"],
            "power": data.get("power", 0) or 0,  # Ensure power is 0 if None
            "effect": data["effect_entries"][0]["short_effect"] if data["effect_entries"] else "No effect description available."
        }
    return None
