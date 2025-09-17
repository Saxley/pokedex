try:
    from src.gui.main_window import display_input, create_gui_images
except ModuleNotFoundError:
    print("tkinter no está disponible. Ejecutando en modo terminal.")
    display_input = None
    create_gui_images = None
    from src.utils.api import fetch_pokemon_data, fetch_evolution_chain

if __name__ == "__main__":
    if display_input:
        display_input()  # Ejecutar la interfaz gráfica si tkinter está disponible
    else:
        # Modo terminal: solicitar el nombre del Pokémon y generar imágenes
        pokemon_name = input("Ingrese el nombre del Pokémon: ").strip().lower()

        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data:
            evolutions = fetch_evolution_chain(pokemon_name)
            create_gui_images(pokemon_data, evolutions)
        else:
            print(f"No se encontraron datos para el Pokémon: {pokemon_name}.")