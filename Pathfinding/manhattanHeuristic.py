# @file manhattanHeuristic.py
# @brief Implementación de la clase ManhattanHeuristic, que representa una heurística de distancia de Manhattan
# @author Anya Marcano
# @date 2024/11/05
from heuristic import Heuristic
from nodes import TileNode
from nodes import Node

class ManhattanHeuristic(Heuristic):
    """
    Clase que representa una heurística de distancia de Manhattan para estimar el costo de un camino entre dos nodos.
    Attributes:
        goal_node (Node): El nodo de destino al que se desea llegar.
        Methods:
            estimate_between(self, from_node: Node, to_node: Node) -> float: Calcula el costo estimado entre dos nodos.
    """
    def estimate_between(self, from_node: Node, to_node: Node) -> float:
        from_tile = from_node
        to_tile = to_node
        if isinstance(from_node, TileNode) and isinstance(to_node, TileNode):
            return abs(from_tile.x - to_tile.x) + abs(from_tile.y - to_tile.y)
        return 0