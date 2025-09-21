# Import the `display_input` function from the `main_window` module inside the `src.gui` folder.
# This function is responsible for displaying the graphical interface to interact with the Pokédex.
from src.gui.main_window import display_input
# from src.terminal.terminal import generate_static_pokemon_images

# Main entry point of the application.
# This block ensures that the code inside it will only execute if the file is run directly
# and not if it is imported as a module in another file.
if __name__ == "__main__":
    # Call the `display_input` function to start the graphical interface of the Pokédex.
    display_input()

    # Commented: If you want to use the terminal version instead of the graphical interface,
    # you can uncomment the following line to generate static images of the Pokémon.
    #generate_static_pokemon_images()

