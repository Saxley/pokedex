import tkinter as tk # This library is used to create the GUI user interface
from tkinter import messagebox # messagebox helps display error messages
from PIL import ImageTk # Helps generate images
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.utils.api import fetch_pokemon_data, fetch_evolution_chain, fetch_move_data
from src.utils.helpers import create_radar_graph, fetch_and_resize_image, create_move_graph
from src.utils.save_search_json import save_pokemon_data_as_json

# Function to display a graph of a move
# This function creates a new window that shows a graph with the damage and effect of a move
def display_move_graph(move_name):
        """Displays a graph with the damage and effect of a move."""
        move_data = fetch_move_data(move_name)
        if not move_data:
            messagebox.showerror("Error", f"Could not fetch data for the move: {move_name}.")
            return

        # Create a new window for the graph
        graph_window = tk.Toplevel()
        graph_window.title(f"Move: {move_name}")

        # Create the graph using the helper function from helpers
        fig = create_move_graph(move_name, move_data["power"], len(move_data["effect"]))

        # Embed the graph in the window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Button to close the window
        close_button = tk.Button(graph_window, text="Close", command=graph_window.destroy, bg="black", fg="white", font=("Confortaa", 10))
        close_button.pack(pady=10)

# Function to display the evolutions of a Pokémon
# This function generates horizontal buttons with the evolutions of the current Pokémon
# Each button allows loading the data of the corresponding Pokémon
def display_evolutions(image_frame, pokemon_name, window):
    """Displays evolution buttons horizontally at the bottom of the image frame,
    with the Close button below them.
    """
    bottom_frame_search = tk.Frame(image_frame, bg="red") 
    bottom_frame_search.pack(side="bottom", fill="x")
    
    bottom_frame = tk.Frame(bottom_frame_search, bg="red") 
    bottom_frame.pack(side="bottom", fill="x")

    # Get evolution data
    evolution_data = fetch_evolution_chain(pokemon_name)
    evolution_frame = tk.Frame(bottom_frame_search, bg="red")
    evolution_frame.pack(side="top", pady=5)
    for evolution in evolution_data:
        # Fetch and resize the evolution image
        evo_image = fetch_and_resize_image(evolution['image_url'], size=(50, 50)) 
        if evo_image:
            # Convert the Pillow image to ImageTk.PhotoImage
            evo_image_tk = ImageTk.PhotoImage(evo_image)
            # Create a button with the evolution image
            evo_button = tk.Button(evolution_frame, image=evo_image_tk, bg="red", command=lambda name=evolution['name']: [window.destroy(), display_pokemon_data(name)])
            evo_button.image = evo_image_tk  # Keep a reference to avoid garbage collection
            evo_button.pack(side="left", padx=5)
        else:
            # Create a button with the evolution name if no image is available
            evo_button = tk.Button(evolution_frame, text=evolution['name'], bg="red", command=lambda name=evolution['name']: [window.destroy(), display_pokemon_data(name)])
            evo_button.pack(side="left", padx=5)
    # Button to search for another Pokémon
    search_button = tk.Button(bottom_frame_search, text="Buscar otro Pokémon", command=lambda: [window.destroy(), display_input()], bg="#FA8800", fg="white", font=("Confortaa", 12))
    search_button.pack(side="bottom", pady=(0, 5))
    # Button to close the window
    close_button = tk.Button(bottom_frame, text="Cerrar", command=window.destroy, bg="black", fg="white", font=("Confortaa", 10))
    close_button.pack(side="bottom", pady=10)

# Function to display Pokémon data
# This function creates the main window where Pokémon data is displayed
# Includes the image, stats, moves, and evolutions
def display_pokemon_data(pokemon_name):
    """Display Pokémon data in a graphical window."""
    # Fetch Pokémon data
    pokemon_data = fetch_pokemon_data(pokemon_name)
    if not pokemon_data:
        messagebox.showerror("Error", f"Could not fetch data for {pokemon_name}.")
        if 'window' in locals():  # Check if 'window' is defined
            window.destroy()  # Destroy the current window if it exists
        display_input()  # Redirect to the input function
        return

    # Create main window
    window = tk.Tk()
    window.title("Pokédex")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    target_percentage = 0.60
    window_width = int(screen_width * target_percentage)
    window_height = int(screen_height * target_percentage)
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)


    window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    window.configure(bg="red")

    # Layout frames
    image_frame = tk.Frame(window, bg="red", width=200)
    image_frame.pack(side="left", fill="y")

    graph_frame = tk.Frame(window, bg="white")
    graph_frame.pack(side="right", fill="both", expand=True)

    # Display Pokémon image on the left side
    image = fetch_and_resize_image(pokemon_data['image_url'], size=(200, 200))
    # Convert the Pillow image to ImageTk.PhotoImage
    if image:
        image_tk = ImageTk.PhotoImage(image)
        img_label = tk.Label(image_frame, image=image_tk, bg="red")
        img_label.image = image_tk  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)

    # Display Pokémon information below the image
    info = f"""
    {pokemon_data['name'].upper()}
    TIPOS: {', '.join(pokemon_data['types']).upper()}
    PESO: {pokemon_data['weight']} KG
    ALTURA: {pokemon_data['height']} M
    HABILIDADES: {', '.join(pokemon_data['abilities']).upper()}
    """
    info_label = tk.Label(image_frame, text=info, bg="red", fg="white", justify="left", font=("Confortaa", 10), wraplength=180)
    info_label.pack(pady=10)

    # Display radar graph for Pokémon stats
    stats_radar_graph = create_radar_graph(pokemon_data['stats'])
    radar_canvas = FigureCanvasTkAgg(stats_radar_graph, master=graph_frame)
    radar_canvas.draw()
    radar_canvas.get_tk_widget().pack(fill="both", expand=True)

    # Update scrollable list for moves with matching background color and limited visible items
    moves_label = tk.Label(image_frame, text="MOVIMIENTOS:", bg="red", fg="white", font=("Confortaa", 10, "bold"))
    moves_label.pack(pady=(10, 0))

    moves_frame = tk.Frame(image_frame, bg="red")
    moves_frame.pack(fill="both", expand=True, pady=(0, 10))

    moves_scrollbar = tk.Scrollbar(moves_frame, orient="vertical", bg="red", troughcolor="red", activebackground="red", highlightbackground="red")
    moves_listbox = tk.Listbox(moves_frame, yscrollcommand=moves_scrollbar.set, bg="red", fg="white", font=("Confortaa", 10), height=3)

    moves_scrollbar.pack(side="left", fill="y")
    moves_listbox.pack(side="left", fill="both", expand=True)
    moves_scrollbar.config(command=moves_listbox.yview)

    for move in pokemon_data['moves']:
        moves_listbox.insert(tk.END, move.upper())

    # Update the moves listbox to bind the selection event
    moves_listbox.bind("<Double-1>", lambda event: display_move_graph(moves_listbox.get(moves_listbox.curselection())))

    # Call display_evolutions to add evolution buttons
    display_evolutions(image_frame, pokemon_name, window)

    # Save Pokémon information to a JSON file
    output_dir = "assets/pokedex_search"
    save_pokemon_data_as_json(pokemon_data, output_dir)

    window.mainloop()

# Function to center a window on the screen
# Calculates the coordinates needed to position the window in the center
def displays_center(window):
    """Center a given window on the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Function to display an input box
# Allows the user to enter the name of a Pokémon to search for its data
def display_input():
    """Display an input dialog to ask the user which Pokémon to search for."""
    input_window = tk.Tk()
    input_window.title("Pokédex")
    input_window.configure(bg="red")

    label = tk.Label(input_window, text="¿Qué Pokémon deseas buscar?", bg="red", fg="white", font=("Confortaa", 12))
    label.pack(pady=10)

    entry = tk.Entry(input_window, justify='center', font=("Confortaa", 12))
    entry.pack(pady=10)

    def on_submit():
        pokemon_name = entry.get().strip()
        if pokemon_name:
            input_window.destroy()
            display_pokemon_data(pokemon_name)

    submit_button = tk.Button(input_window, text="Buscar", command=on_submit, bg="black", fg="white", font=("Confortaa", 10))
    submit_button.pack(pady=10)

    # Center the input window
    displays_center(input_window)

    input_window.mainloop()
