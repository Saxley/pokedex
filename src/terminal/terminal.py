# Import the necessary libraries to handle files, images, and graphs.
import os
from PIL import Image, ImageDraw, ImageFont
from src.utils.api import fetch_pokemon_data, fetch_evolution_chain
from src.utils.helpers import create_radar_graph, fetch_and_resize_image
from src.utils.save_search_json import save_pokemon_data_as_json
import matplotlib.pyplot as plt

# Main function to generate static images with Pokémon data.
def generate_static_pokemon_images():
    print("Welcome to the Pokédex from the command line.")
    # Ask the user for the name of the Pokémon they want to search for.
    pokemon_name = input("Enter the name of the Pokémon: ").strip().lower()

    # Fetch Pokémon data from the API.
    pokemon_data = fetch_pokemon_data(pokemon_name)
    if not pokemon_data:
        # If no data is found, display a message and terminate execution.
        print(f"No data found for the Pokémon: {pokemon_name}.")
        return

    # Fetch the Pokémon's evolution chain.
    evolutions = fetch_evolution_chain(pokemon_name)

    # Create the output directory to save the generated files.
    output_dir = "assets/pokedex_search"
    os.makedirs(output_dir, exist_ok=True)

    # Create a main image to display the Pokémon's data.
    main_image = Image.new("RGB", (800, 600), "red")
    draw = ImageDraw.Draw(main_image)

    # Attempt to load the Arial font; if unavailable, use a default font.
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    # Add the Pokémon's name and details to the main image.
    draw.text((20, 20), f"Name: {pokemon_data['name'].upper()}", fill="white", font=font)
    draw.text((20, 60), f"Types: {', '.join(pokemon_data['types']).upper()}", fill="white", font=font)
    draw.text((20, 100), f"Weight: {pokemon_data['weight']} kg", fill="white", font=font)
    draw.text((20, 140), f"Height: {pokemon_data['height']} m", fill="white", font=font)
    draw.text((20, 180), f"Abilities: {', '.join(pokemon_data['abilities']).upper()}", fill="white", font=font)

    # Add the Pokémon's image in the top-right corner.
    pokemon_image = fetch_and_resize_image(pokemon_data['image_url'], size=(150, 150))
    if pokemon_image:
        main_image.paste(pokemon_image, (600, 20))  # Paste the image directly onto the canvas.

    # Create a subdirectory with the Pokémon's name to save its files.
    pokemon_dir = os.path.join(output_dir, pokemon_data['name'].lower())
    os.makedirs(pokemon_dir, exist_ok=True)

    # Save the main image in the subdirectory.
    main_image_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_details.png")
    main_image.save(main_image_path)
    print(f"Main image saved at: {main_image_path}")

    # Create a radar graph with the Pokémon's stats.
    radar_graph = create_radar_graph(pokemon_data['stats'])
    radar_graph_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_stats.png")
    radar_graph.savefig(radar_graph_path)  # Save the graph in the subdirectory.
    plt.close(radar_graph)  # Close the graph to free resources.

    # Save the Pokémon's evolution images in the subdirectory.
    for evolution in evolutions:
        evo_image = fetch_and_resize_image(evolution['image_url'], size=(100, 100))
        if evo_image:
            evo_image_path = os.path.join(pokemon_dir, f"{evolution['name']}_evolution.png")
            evo_image.save(evo_image_path)
            print(f"Evolution image saved at: {evo_image_path}")

    # Create a combined graph with the Pokémon's data and evolutions.
    if evolutions:
        canvas_width = 800
        canvas_height = 600
        combined_image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(combined_image)

        # Add the radar graph in the first row.
        radar_graph_image = Image.open(radar_graph_path)
        radar_x = (canvas_width - radar_graph_image.width) // 2
        combined_image.paste(radar_graph_image, (radar_x, 20))

        # Add the Pokémon's data and image in the second row.
        y_offset = 300
        draw.text((20, y_offset), f"Name: {pokemon_data['name'].upper()}", fill="black", font=font)
        draw.text((20, y_offset + 40), f"Types: {', '.join(pokemon_data['types']).upper()}", fill="black", font=font)
        draw.text((20, y_offset + 80), f"Weight: {pokemon_data['weight']} kg", fill="black", font=font)
        draw.text((20, y_offset + 120), f"Height: {pokemon_data['height']} m", fill="black", font=font)
        draw.text((20, y_offset + 160), f"Abilities: {', '.join(pokemon_data['abilities']).upper()}", fill="black", font=font)

        pokemon_image = fetch_and_resize_image(pokemon_data['image_url'], size=(200, 200))
        if pokemon_image:
            image_x = canvas_width - pokemon_image.width - 20
            combined_image.paste(pokemon_image, (image_x, y_offset))

        combined_image_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_full_details.png")
        combined_image.save(combined_image_path)
        print(f"Complete graph saved at: {combined_image_path}")

    # Save all the Pokémon's information in a JSON file.
    save_pokemon_data_as_json(pokemon_data, output_dir)

