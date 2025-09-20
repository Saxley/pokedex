# POKEDEX

> Este proyecto se realizo con ayuda del material que se encuentra en el curso, ademas se tomo como referencia el proyecto del sitio web https://programmerclick.com/article/37062133001/, utiliza diferentes bibliotecas.

## Versión terminal.

> Ubicación : src.terminal.terminal.py<br>Esta versión utiliza las siguientes librerias:

- **os** : Esta librería nos ayuda a ingresar, editar y modificar los directorios.
- **PIL** : La libreria PIL nos ayuda a crear y renderizar las imagenes y textos.
- **matplotlib** : Esta libreria nos ayuda a generar el grafico de radar sobre las estadisticas del personaje.
- **requests** : Esta libreria nos ayuda a hacer las peticiones a la API pokemon, así como trabajar los status code
- **io.BytesIO** : Esta libreria nos ayuda a crear en memoria del programa archivos temporales. La utilizo para poder crear y leer las imagenes y posteriormente guardarlas en el directorio creado con la libreria os.
- **json** : Esta libreria nos ayuda a crear archivos json.

> El proyecto se dividio en 4 archivos, esto con el fin de poder reutilizar el codigo para futuras mejoras.<br>Lo dividi con una estructura de carpetas muy similar a un proyecto web.<br>Tenemos la carpeta **src**, carpeta donde almacenamos las funciones que se subdividen en diferentes directorios, tenemos la carpeta **utils** en esta carpeta se almacenan las funciones que se dedican a realizar las peticiones a la API pokemon **(api.py)**, tambien almacena las funciones que nos ayudan a crear los graficos y las imagenes **(helpers.py)** y por ultimo la funcion que nos ayuda a almacnar la información recolectada en un archivo json **(save_search_json.py)**. Despues tenemos la carpeta **terminal** en esta carpeta va toda la logica de nuestra aplicación, es donde llamamos de forma ordenada a las funciones que contiene utils, para poder generar nuestra imagen estatica. El flujo de ejecución es el siguiente:<br>Solicitamos al usuario que introduzca el nombre de un pokemon, mediante un ciclo while se analizara si el usuario, introdujo o no el nombre, si lo introdujo se llamara a la funcion **fetch_pokemon_data**(se encarga de traer los datos del pokemon, nombre,estadisticas,url de la imagen front,su tipo de pokemon,abilidades,altura,peso y movimientos), si la funcion retorna None(vacío) notificamos al usuario que no se encontro su pokemon e invitamos a que lo intente de nuevo.

```python
while True:
        # Ask the user for the name of the Pokémon they want to search for.
        pokemon_name = input("Enter the name of the Pokémon: ").strip().lower()
        if not pokemon_name:
            # If user not input, display a message warning and instructions for exit of execute.
            print(f"No ingresaste texto, intentalo de nuevo o presiona ctrl+c para salir : {pokemon_name}.")
            continue
        # Search the pokemon
        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data:
            # if found a pokemon, display a message sucessfull
            print(f"¡Éxito! Se encontró información sobre {pokemon_name}.")
            break
        else:
            # if not found a pokemon, display a message warning.
            print(f"No se encontró información sobre el Pokémon: {pokemon_name}. Por favor, inténtalo de nuevo.")
```

> Una vez encontrada la información llamamos a la función **fetch_evolution_chain** la cual se encargara de traer las url de las imagenes de los pokemones y sus respectivos nombres.

## Versión GUI.

> Ubicación : src.gui.main_window.py<br>Esta versión utiliza las siguientes librerias:

### Instrucciones.

> El usuario debe introducir el nombre del pokemón.<br>Debe mostrar una imagen y las estadisticas.<br>Las estadisticas deben contener:

1. Peso [x]
2. Tamaño [x]
3. Movimientos [x]
4. Habilidades [x]
5. Tipos [x]

> Se debera guardar la información en un json dentro de una carpeta llamada pokedex.<br>Terminado se debera subir el codigo a github donde se explicaran los siguientes puntos:

1. Como lo realizaste.
2. Que bibliotecas se necesitan, para que otro usuario pueda ejecutar el proyecto.
3. Mostrando imagenes de muestra de algun resultado.
4. Describir que has aprendido en este curso.

### Objetivos

- Aprenderá a consumir una API web pública con la librería requests.
- Dominará la gestión de códigos de status de una API así como el manejo de los resultados.
- Será capaz de crear un archivo dentro del sistema operativo y guardar información en él.
- Arenderá un poco del mundo Pokémon.

### Requisitos:

- El proyecto debe realizarse de forma individual.
- Los participantes deben entregar el link de su repositorio público de GitHub donde en el README.md detallen cómo lo hicieron, qué bibliotecas necesitaría otro usuario para ejecutar el proyecto, mostrando imágenes de muestra de algún resultado de búsqueda de un pokémon y describiendo qué han aprendido en este módulo.

### Entregables

> Los participantes deberán entregar un repositorio de su código en GitHub con los siguientes archivos:

- README.md : Donde explicarán su proyecto y lo que han aprendido como previamente se mencionó.
- Archivo .py: El código funcional comentado de su proyecto.
- Carpeta “pokedex”: Una carpeta con un archivo .json adentro para demostrar que han podido guardar información en un archivo con éxito.
