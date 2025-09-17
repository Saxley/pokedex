import src.terminal.terminal
from src.gui.main_window import display_input
# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    try:
        display_input()
    except ImportError as e:
        print("No se pudo cargar la interfaz gráfica. Cambiando al modo terminal.")
        print(f"Detalles del error: {e}")
        src.terminal.terminal.generate_static_pokemon_images()
    except Exception as e:
        print("Ocurrió un error inesperado. Cambiando al modo terminal.")
        print(f"Detalles del error: {e}")
        src.terminal.terminal.generate_static_pokemon_images()