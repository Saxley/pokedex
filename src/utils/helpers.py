from PIL import Image
import requests
from matplotlib.figure import Figure
from io import BytesIO

# Función para obtener y redimensionar una imagen desde una URL
def fetch_and_resize_image(url, size=(100, 100)):
    """Obtiene una imagen desde una URL y la redimensiona."""
    response = requests.get(url)
    if response.status_code == 200:
        image_data = Image.open(BytesIO(response.content))
        image_data = image_data.resize(size)
        return image_data  # Return the Pillow image object instead of ImageTk.PhotoImage
    return None

# Función para crear un gráfico de radar con las estadísticas de un Pokémon
def create_radar_graph(stats):
    """Crea un gráfico de radar para las estadísticas de un Pokémon."""
    fig = Figure(figsize=(4, 4), facecolor="white")
    ax = fig.add_subplot(111, polar=True)

    # Preparar los datos para el gráfico de radar
    labels = list(stats.keys())
    values = list(stats.values())
    values += values[:1]  # Cerrar el círculo
    angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    angles += angles[:1]

    # Graficar los datos
    ax.plot(angles, values, linewidth=2, linestyle="dashdot", color="black")
    ax.fill(angles, values, color="orange", alpha=0.4)

    # Agregar etiquetas
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color="black")
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color="black")

    return fig

# Función para crear un gráfico de barras con los datos de un movimiento
def create_move_graph(move_name, damage, effect):
    """Crea un gráfico de barras para el daño y efecto de un movimiento."""
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    categories = ["Daño", "Efecto"]
    values = [damage, effect]
    ax.bar(categories, values, color=["red", "blue"])
    ax.set_title(f"Estadísticas de {move_name}")
    return fig
