# Importamos la función display_input encargada de mostrar la interfaz del usuario
from src.gui.main_window import display_input, create_gui_images

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    # Ejecutamos la función principal para iniciar la interfaz gráfica
    try:
        display_input()
    except :
        create_gui_images()