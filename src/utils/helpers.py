from PIL import Image
import requests
from matplotlib.figure import Figure
from io import BytesIO

# Function to fetch and resize an image from a URL
def fetch_and_resize_image(url, size=(100, 100)):
    """Fetches an image from a URL and resizes it."""
    response = requests.get(url)
    if response.status_code == 200: #Status
        image_data = Image.open(BytesIO(response.content))
        image_data = image_data.resize(size)
        return image_data  # Return the Pillow image object instead of ImageTk.PhotoImage
    return None

# Function to create a radar chart with a Pokémon's stats
def create_radar_graph(stats):
    """Creates a radar chart for a Pokémon's stats."""
    fig = Figure(figsize=(4, 4), facecolor="white")
    ax = fig.add_subplot(111, polar=True)

    # Prepare data for the radar chart
    labels = list(stats.keys())
    values = list(stats.values())
    values += values[:1]  # Close the circle
    angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    angles += angles[:1]

    # Plot the data
    ax.plot(angles, values, linewidth=2, linestyle="dashdot", color="black")
    ax.fill(angles, values, color="orange", alpha=0.4)

    # Add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color="black")
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color="black")

    return fig

# Function to create a bar chart with a move's data
def create_move_graph(move_name, damage, effect):
    """Creates a bar chart for a move's damage and effect."""
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    categories = ["Damage", "Effect"]
    values = [damage, effect]
    ax.bar(categories, values, color=["red", "blue"])
    ax.set_title(f"Statistics of {move_name}")
    return fig
