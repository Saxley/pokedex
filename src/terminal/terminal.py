# Importamos las bibliotecas necesarias para manejar archivos, imágenes y gráficos.
import os
from PIL import Image, ImageDraw, ImageFont
from src.utils.api import fetch_pokemon_data, fetch_evolution_chain
from src.utils.helpers import create_radar_graph, fetch_and_resize_image
from src.utils.save_search_json import save_pokemon_data_as_json
import matplotlib.pyplot as plt

# Función principal para generar imágenes estáticas con los datos del Pokémon.
def generate_static_pokemon_images():
    print("Bienvenido a la Pokédex desde la línea de comandos.")
    # Solicitamos al usuario el nombre del Pokémon que desea buscar.
    pokemon_name = input("Ingrese el nombre del Pokémon: ").strip().lower()

    # Obtenemos los datos del Pokémon desde la API.
    pokemon_data = fetch_pokemon_data(pokemon_name)
    if not pokemon_data:
        # Si no se encuentran datos, mostramos un mensaje y terminamos la ejecución.
        print(f"No se encontraron datos para el Pokémon: {pokemon_name}.")
        return

    # Obtenemos la cadena de evoluciones del Pokémon.
    evolutions = fetch_evolution_chain(pokemon_name)

    # Creamos el directorio de salida para guardar los archivos generados.
    output_dir = "assets/pokedex_search"
    os.makedirs(output_dir, exist_ok=True)

    # Creamos una imagen principal para mostrar los datos del Pokémon.
    main_image = Image.new("RGB", (800, 600), "red")
    draw = ImageDraw.Draw(main_image)

    # Intentamos cargar la fuente Arial; si no está disponible, usamos una fuente predeterminada.
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    # Agregamos el nombre y detalles del Pokémon en la imagen principal.
    draw.text((20, 20), f"Name: {pokemon_data['name'].upper()}", fill="white", font=font)
    draw.text((20, 60), f"Types: {', '.join(pokemon_data['types']).upper()}", fill="white", font=font)
    draw.text((20, 100), f"Weight: {pokemon_data['weight']} kg", fill="white", font=font)
    draw.text((20, 140), f"Height: {pokemon_data['height']} m", fill="white", font=font)
    draw.text((20, 180), f"Abilities: {', '.join(pokemon_data['abilities']).upper()}", fill="white", font=font)

    # Agregamos la imagen del Pokémon en la esquina superior derecha.
    pokemon_image = fetch_and_resize_image(pokemon_data['image_url'], size=(150, 150))
    if pokemon_image:
        main_image.paste(pokemon_image, (600, 20))  # Pegamos la imagen directamente en el lienzo.

    # Creamos un subdirectorio con el nombre del Pokémon para guardar sus archivos.
    pokemon_dir = os.path.join(output_dir, pokemon_data['name'].lower())
    os.makedirs(pokemon_dir, exist_ok=True)

    # Guardamos la imagen principal en el subdirectorio.
    main_image_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_details.png")
    main_image.save(main_image_path)
    print(f"Imagen principal guardada en: {main_image_path}")

    # Creamos un gráfico de radar con las estadísticas del Pokémon.
    radar_graph = create_radar_graph(pokemon_data['stats'])
    radar_graph_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_stats.png")
    radar_graph.savefig(radar_graph_path)  # Guardamos el gráfico en el subdirectorio.
    plt.close(radar_graph)  # Cerramos el gráfico para liberar recursos.

    # Guardamos las imágenes de las evoluciones del Pokémon en el subdirectorio.
    for evolution in evolutions:
        evo_image = fetch_and_resize_image(evolution['image_url'], size=(100, 100))
        if evo_image:
            evo_image_path = os.path.join(pokemon_dir, f"{evolution['name']}_evolution.png")
            evo_image.save(evo_image_path)
            print(f"Imagen de evolución guardada en: {evo_image_path}")

    # Creamos un gráfico combinado con los datos y evoluciones del Pokémon.
    if evolutions:
        canvas_width = 800
        canvas_height = 600
        combined_image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(combined_image)

        # Agregamos el gráfico de radar en la primera fila.
        radar_graph_image = Image.open(radar_graph_path)
        radar_x = (canvas_width - radar_graph_image.width) // 2
        combined_image.paste(radar_graph_image, (radar_x, 20))

        # Agregamos los datos del Pokémon y su imagen en la segunda fila.
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
        print(f"Gráfico completo guardado en: {combined_image_path}")

    # Guardamos toda la información del Pokémon en un archivo JSON.
    save_pokemon_data_as_json(pokemon_data, output_dir)

