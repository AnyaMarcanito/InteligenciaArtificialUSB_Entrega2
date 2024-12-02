# @file functions.py
# @brief Implementación de funciones auxiliares para el juego
# @author Anya Marcano
# @date 2024/11/05

import pygame
from Pathfinding.aStar import pathfind_astar
from Pathfinding.manhattanHeuristic import ManhattanHeuristic
from WorldRepresentation.tileGraph import TileGraph

#  Funcion para cargar y escalar imágenes de los personajes
def load_and_scale_image(path, scale_factor=1):
    """
    Carga una imagen y la escala por un factor dado
    :param path: str
    La ruta de la imagen
    :param scale_factor: float
    El factor de escala
    :return: pygame.Surface
    La imagen escalada
    """
    image = pygame.image.load(path)
    scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))
    return scaled_image

def check_collision(x, y, scaled_maze):
    """
    Verifica si el jugador colisiona con el laberinto
    :param x: float
    La posición x del jugador
    :param y: float
    La posición y del jugador
    :param scaled_maze: pygame.Surface
    El laberinto escalado
    :return: bool
    True si el jugador colisiona con el laberinto, False en caso contrario
    """
    # Verificar si la posición está dentro de los límites del mapa
    if x < 0 or y < 0 or x >= scaled_maze.get_width() or y >= scaled_maze.get_height():
        return True
    
    # Obtener el color del píxel en la posición del jugador
    try:
        color = scaled_maze.get_at((int(x), int(y)))
        return color[0] > 246 
    except IndexError:
        return True
    
# Función para obtener el camino entre dos puntos
def get_path(start_x: int, start_y: int, end_x: int, end_y: int, tile_graph: TileGraph, tile_size: int):
    """
    Obtiene el camino entre dos puntos
    :param start_x: int
    La posición x de inicio
    :param start_y: int
    La posición y de inicio
    :param end_x: int
    La posición x de fin
    :param end_y: int
    La posición y de fin
    :param tile_graph: TileGraph
    El grafo de nodos
    :param tile_size: int
    El tamaño de los nodos
    :return: list
    La lista de nodos que representan el camino
    """
    start_node = tile_graph.nodes.get((start_x // tile_size, start_y // tile_size))
    end_node = tile_graph.nodes.get((end_x // tile_size, end_y // tile_size))
    
    if start_node and end_node:
        heuristic = ManhattanHeuristic(end_node)
        path = pathfind_astar(tile_graph, start_node, end_node, heuristic)
        return path
    return None

# Función para encontrar el npc más cercano en base al path finding
def encontrar_NPC_cercano(player_x, player_y, NPC_positions, tile_graph, tile_size):
    """
    Encuentra el NPC más cercano al jugador
    :param player_x: int
    La posición x del jugador
    :param player_y: int
    La posición y del jugador
    :param NPC_positions: list
    La lista de posiciones de los NPCs
    :param tile_graph: TileGraph
    El grafo de nodos
    :param tile_size: int
    El tamaño de los nodos
    :return: list, dict
    La lista de nodos que representan el camino y el NPC objetivo
    """
    mejor_distancia = float('inf')
    mejor_camino = None
    objetivo = None

    for NPC in NPC_positions:
        camino = get_path(player_x, player_y, NPC["x"], NPC["y"], tile_graph, tile_size)
        if camino:
            # Calculamos la longitud del camino
            distancia = len(camino)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_camino = camino
                objetivo = NPC

    return mejor_camino, objetivo

# Función para dibujar el camino
def draw_path(screen, path, camera_x, camera_y, tile_size):
    """
    Dibuja el camino en la pantalla
    :param screen: pygame.Surface
    La pantalla
    :param path: list
    La lista de nodos que representan el camino
    :param camera_x: int
    La posición x de la cámara
    :param camera_y: int
    La posición y de la cámara
    :param tile_size: int
    El tamaño de los nodos
    """
    if path:
        # Se dibujan los nodos
        for i in range(len(path)-1):
            start = path[i].from_node
            end = path[i].to_node
            
            start_pos = (start.x * tile_size - camera_x, 
                        start.y * tile_size - camera_y)
            end_pos = (end.x * tile_size - camera_x,
                      end.y * tile_size - camera_y)
            
            pygame.draw.line(screen, (255, 255, 0), start_pos, end_pos, 2)