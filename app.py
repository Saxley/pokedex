# Importamos la función `display_input` desde el módulo `main_window` dentro de la carpeta `src.gui`.
# Esta función se encarga de mostrar la interfaz gráfica para interactuar con la Pokédex.
from src.gui.main_window import display_input

# Punto de entrada principal de la aplicación.
# Este bloque asegura que el código dentro de él solo se ejecutará si el archivo se ejecuta directamente
# y no si se importa como un módulo en otro archivo.
if __name__ == "__main__":
    # Llamamos a la función `display_input` para iniciar la interfaz gráfica de la Pokédex.
    display_input()

    # Comentado: Si se quisiera usar la versión de terminal en lugar de la interfaz gráfica,
    # se podría descomentar la siguiente línea para generar imágenes estáticas de los Pokémon.
    # src.terminal.terminal.generate_static_pokemon_images()

