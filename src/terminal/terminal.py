# Import the necessary libraries to handle files, images, and graphs.
import os
from PIL import Image, ImageDraw, ImageFont
from src.utils.api import fetch_pokemon_data, fetch_evolution_chain
from src.utils.helpers import create_radar_graph, fetch_and_resize_image
from src.utils.save_search_json import save_pokemon_data_as_json
import matplotlib.pyplot as plt

# Main function to generate static images with Pokémon data.
def generate_static_pokemon_images():
    print("Bienvenido a la Pokédex desde la linea de comandos.")
    # Fetch Pokémon data from the API.
    while True:
        # Ask the user for the name of the Pokémon they want to search for.
        pokemon_name = input("Enter the name of the Pokémon: ").strip().lower()    
        if not pokemon_name:
            # If user not input, display a message warning and instructions for exit of execute.
            print(f"No ingresaste texto, intentalo de nuevo o presiona ctrl+c para salir : {pokemon_name}.")
            continue
        # Search the pokemon
        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data:
            # if found a pokemon, display a message sucessfull
            print(f"¡Éxito! Se encontró información sobre {pokemon_name}.")
            break
        else:
            # if not found a pokemon, display a message warning.
            print(f"No se encontró información sobre el Pokémon: {pokemon_name}. Por favor, inténtalo de nuevo.")


    # Fetch the Pokémon's evolution chain.
    evolutions = fetch_evolution_chain(pokemon_name)

    # Create the output directory to save the generated files.
    output_dir = "assets/pokedex_search"
    os.makedirs(output_dir, exist_ok=True)
    # Create a subdirectory with the Pokémon's name to save its files.
    pokemon_dir = os.path.join(output_dir, pokemon_data['name'].lower())
    os.makedirs(pokemon_dir, exist_ok=True)

    # Attempt to load the Confortaa font; if unavailable, use a default font.
    try:
        font = ImageFont.truetype("confortaa.ttf", 12)
    except OSError:
        font = ImageFont.load_default()

    # Create a radar graph with the Pokémon's stats.
    radar_graph = create_radar_graph(pokemon_data['stats'])
    radar_graph_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_stats.png")
    radar_graph.savefig(radar_graph_path)  # Save the graph in the subdirectory.
    plt.close(radar_graph)  # Close the graph to free resources.
    pokemon_image = fetch_and_resize_image(pokemon_data['image_url'], size=(150, 150))
    # Save the Pokémon's evolution images in the subdirectory.
    for evolution in evolutions:
        evo_image = fetch_and_resize_image(evolution['image_url'], size=(100, 100))
        if evo_image:
            evo_image_path = os.path.join(pokemon_dir, f"{evolution['name']}_evolution.png")
            evo_image.save(evo_image_path)
            print(f"Imagen de la evolución, se almaceno con exíto: {evo_image_path}")

    # Create a combined graph with the Pokémon's data and evolutions.
    if evolutions:
        canvas_width = 800
        canvas_height = 1000
        combined_image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(combined_image)

        # Add the radar graph in the first row.
        radar_graph_image = Image.open(radar_graph_path)
        radar_x = (canvas_width - radar_graph_image.width) // 2
        combined_image.paste(radar_graph_image, (radar_x, 20))

        # Add the Pokémon's data and image in the second row.
        y_offset = 240
        pokemon= pokemon_data['name']
        draw.text((20, y_offset), f"Name: {pokemon_data['name'].upper()}", fill="black", font=font)
        draw.text((20, y_offset + 40), f"Types: {', '.join(pokemon_data['types']).upper()}", fill="black", font=font)
        draw.text((20, y_offset + 80), f"Weight: {pokemon_data['weight']} kg", fill="black", font=font)
        draw.text((20, y_offset + 120), f"Height: {pokemon_data['height']} m", fill="black", font=font)
        draw.text((20, y_offset + 160), f"Abilities: {', '.join(pokemon_data['abilities']).upper()}", fill="black", font=font)

        # Define a starting vertical position for the evolutions to be pasted
        EVOLUTION_START_Y = 50 
        Y_OFFSET_PER_EVOLUTION = 120 # Vertical space between evolution images

        if pokemon_image:
            # 1. Paste the main Pokémon image
            combined_image.paste(pokemon_image, (0, 50))
            # 2. Iterate and paste the evolution images
            current_y = EVOLUTION_START_Y # Initialize the vertical position for the first evolution
            for i, evolution in enumerate(evolutions):
                if evolution['name'] != pokemon:
                    try:
                        # Construct the file path clearly
                        evo_filename = f"{evolution['name'].lower()}_evolution.png"
                        evo_path = f"{output_dir}/{pokemon_data['name'].lower()}/{evo_filename}"
                        evo_image = Image.open(evo_path)

                        # Calculate the horizontal position
                        image_evo_x = canvas_width - evo_image.width - 20

                        # Paste the evolution image at the calculated (x, y)
                        combined_image.paste(evo_image, (image_evo_x, current_y))

                        # Update the vertical position for the next evolution
                        current_y += Y_OFFSET_PER_EVOLUTION 

                    except FileNotFoundError:
                        print(f"Advertencia: No se encontro la imagen de la evolución {evo_path}")
                    except Exception as e:
                        print(f"Ocurrio un error mientras se procesaba {evolution['name']}: {e}")



        combined_image_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_full_details.png")
        combined_image.save(combined_image_path)
        print(f"Se almaceno el gráfico: {combined_image_path} con exíto")

    # Save all the Pokémon's information in a JSON file.
    save_pokemon_data_as_json(pokemon_data, output_dir)

