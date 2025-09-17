try:
    # Importamos la función display_input encargada de mostrar la interfaz del usuario
    from src.gui.main_window import display_input, create_gui_images
except ModuleNotFoundError:
    print("tkinter no está disponible. Ejecutando en modo terminal.")
    display_input = None
    create_gui_images = None

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    if display_input:
        # Ejecutamos la función principal para iniciar la interfaz gráfica
        display_input()
    else:
        from src.utils.api import fetch_pokemon_data, fetch_evolution_chain
        from src.gui.main_window import create_gui_images
        # Modo terminal: solicitar el nombre del Pokémon y generar imágenes
        pokemon_name = input("Ingrese el nombre del Pokémon: ").strip().lower()

        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data:
            evolutions = fetch_evolution_chain(pokemon_name)
            create_gui_images(pokemon_data, evolutions)
        else:
            print(f"No se encontraron datos para el Pokémon: {pokemon_name}.")