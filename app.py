import src.terminal.terminal
from src.gui.main_window import display_input
# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    try:
        display_input()
    except:
        src.terminal.terminal.generate_static_pokemon_images()