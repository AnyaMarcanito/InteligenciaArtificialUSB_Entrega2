import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Pathfinding.nodes import TileNode
from Pathfinding.graph import Graph


class TileGraph(Graph):
    def __init__(self, maze_surface: pygame.Surface, tile_size: int = 32):
        super().__init__()
        self.tile_size = tile_size
        self.maze_surface = maze_surface
        self.nodes = {}
        self.create_graph_from_maze()
    
    def create_graph_from_maze(self):
        width = self.maze_surface.get_width() // self.tile_size
        height = self.maze_surface.get_height() // self.tile_size
        
        # Create nodes for walkable tiles
        for y in range(height):
            for x in range(width):
                if not self.is_wall(x, y):
                    node = TileNode(x, y)
                    self.nodes[(x, y)] = node
                    
        # Create connections between adjacent walkable tiles
        for y in range(height):
            for x in range(width):
                if (x, y) in self.nodes:
                    self.add_connections_for_tile(x, y)
    
    def is_wall(self, x: int, y: int) -> bool:
        pixel_x = x * self.tile_size + self.tile_size // 2
        pixel_y = y * self.tile_size + self.tile_size // 2
        try:
            color = self.maze_surface.get_at((pixel_x, pixel_y))
            return color[0] > 246  # Using your existing collision logic
        except IndexError:
            return True
    
    def add_connections_for_tile(self, x: int, y: int):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional movement
        current_node = self.nodes[(x, y)]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in self.nodes:
                neighbor_node = self.nodes[(new_x, new_y)]
                self.add_connection(current_node, neighbor_node, 1.0)
    
    def draw_world_representation(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        # Dibuja la cuadrícula
        for (x, y), node in self.nodes.items():
            screen_x = x * self.tile_size - camera_x
            screen_y = y * self.tile_size - camera_y
            
            # Dibuja el borde de cada tile
            pygame.draw.rect(surface, (255, 255, 255), 
                            (screen_x, screen_y, self.tile_size, self.tile_size), 1)
            
            # Dibuja el nodo representativo (punto central)
            pygame.draw.circle(surface, (255, 0, 255),
                            (screen_x + self.tile_size//2, screen_y + self.tile_size//2), 3)
            
            # Dibuja las conexiones
            for connection in self.get_connections(node):
                to_node = connection.getToNode()
                if isinstance(to_node, TileNode):
                    end_x = to_node.x * self.tile_size - camera_x + self.tile_size//2
                    end_y = to_node.y * self.tile_size - camera_y + self.tile_size//2
                    pygame.draw.line(surface, (0, 255, 255),
                                (screen_x + self.tile_size//2, screen_y + self.tile_size//2),
                                (end_x, end_y), 1)