# @file static.py
# @brief Implementacion de la clase static
# @author Anya Marcano
# @date 2024/11/05

from pygame import Vector2 as Vector
class static:
    def __init__(self, position: Vector, orientation: float):
        self.position = position
        self.orientation = orientation
        self.x = position.x
        self.y = position.y