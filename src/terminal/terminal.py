import os
from PIL import Image, ImageDraw, ImageFont
from src.utils.api import fetch_pokemon_data, fetch_evolution_chain
from src.utils.helpers import create_radar_graph, fetch_and_resize_image
import matplotlib.pyplot as plt

# Función para generar imágenes estáticas con los datos del Pokémon
def generate_static_pokemon_images():
    print("Bienvenido a la Pokédex desde la línea de comandos.")
    pokemon_name = input("Ingrese el nombre del Pokémon: ").strip().lower()

    # Obtener los datos del Pokémon
    pokemon_data = fetch_pokemon_data(pokemon_name)
    if not pokemon_data:
        print(f"No se encontraron datos para el Pokémon: {pokemon_name}.")
        return

    # Obtener las evoluciones del Pokémon
    evolutions = fetch_evolution_chain(pokemon_name)

    # Crear el directorio de salida
    output_dir = "assets/pokedex_search"
    os.makedirs(output_dir, exist_ok=True)

    # Crear la imagen principal
    main_image = Image.new("RGB", (800, 600), "red")
    draw = ImageDraw.Draw(main_image)

    # Intentar cargar la fuente Arial, usar una fuente predeterminada si no está disponible
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    # Agregar el nombre y detalles del Pokémon
    draw.text((20, 20), f"Name: {pokemon_data['name'].upper()}", fill="white", font=font)
    draw.text((20, 60), f"Types: {', '.join(pokemon_data['types']).upper()}", fill="white", font=font)
    draw.text((20, 100), f"Weight: {pokemon_data['weight']} kg", fill="white", font=font)
    draw.text((20, 140), f"Height: {pokemon_data['height']} m", fill="white", font=font)
    draw.text((20, 180), f"Abilities: {', '.join(pokemon_data['abilities']).upper()}", fill="white", font=font)

    # Agregar la imagen del Pokémon
    pokemon_image = fetch_and_resize_image(pokemon_data['image_url'], size=(150, 150))
    if pokemon_image:
        main_image.paste(pokemon_image, (600, 20))  # Directly paste the Pillow image object

    # Crear un subdirectorio con el nombre del Pokémon
    pokemon_dir = os.path.join(output_dir, pokemon_data['name'].lower())
    os.makedirs(pokemon_dir, exist_ok=True)

    # Guardar la imagen principal en el subdirectorio
    main_image_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_details.png")
    main_image.save(main_image_path)
    print(f"Imagen principal guardada en: {main_image_path}")

    # Crear un gráfico de radar para las estadísticas del Pokémon
    radar_graph = create_radar_graph(pokemon_data['stats'])
    # Guardar el gráfico de radar en el subdirectorio
    radar_graph_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_stats.png")
    # Guardar y cerrar el gráfico de radar antes de abrirlo
    radar_graph.savefig(radar_graph_path)
    plt.close(radar_graph)

    # Guardar las imágenes de las evoluciones en el subdirectorio
    for evolution in evolutions:
        evo_image = fetch_and_resize_image(evolution['image_url'], size=(100, 100))
        if evo_image:
            evo_image_path = os.path.join(pokemon_dir, f"{evolution['name']}_evolution.png")
            evo_image.save(evo_image_path)
            print(f"Imagen de evolución guardada en: {evo_image_path}")

    # Crear un gráfico combinado como tabla de 2 filas
    if evolutions:
        # Dimensiones del lienzo principal
        canvas_width = 800
        canvas_height = 600  # Espacio para dos filas
        combined_image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(combined_image)

        # Primera fila: Gráfico de radar
        radar_graph_image = Image.open(radar_graph_path)
        radar_x = (canvas_width - radar_graph_image.width) // 2  # Centrar horizontalmente
        combined_image.paste(radar_graph_image, (radar_x, 20))

        # Segunda fila: Datos del Pokémon y su imagen
        y_offset = 300
        draw.text((20, y_offset), f"Name: {pokemon_data['name'].upper()}", fill="black", font=font)
        draw.text((20, y_offset + 40), f"Types: {', '.join(pokemon_data['types']).upper()}", fill="black", font=font)
        draw.text((20, y_offset + 80), f"Weight: {pokemon_data['weight']} kg", fill="black", font=font)
        draw.text((20, y_offset + 120), f"Height: {pokemon_data['height']} m", fill="black", font=font)
        draw.text((20, y_offset + 160), f"Abilities: {', '.join(pokemon_data['abilities']).upper()}", fill="black", font=font)

        # Imagen del Pokémon a la derecha
        pokemon_image = fetch_and_resize_image(pokemon_data['image_url'], size=(200, 200))
        if pokemon_image:
            image_x = canvas_width - pokemon_image.width - 20  # Alinear a la derecha
            combined_image.paste(pokemon_image, (image_x, y_offset))

        # Guardar el gráfico combinado en el subdirectorio
        combined_image_path = os.path.join(pokemon_dir, f"{pokemon_data['name']}_full_details.png")
        combined_image.save(combined_image_path)
        print(f"Gráfico completo guardado en: {combined_image_path}")