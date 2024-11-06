# @file heuristic.py
# @brief Implementación de la clase Heuristic, que representa una heurística para estimar el costo de un camino
# @author Anya Marcano
# @date 2024/11/05

from nodes import Node
from abc import ABC, abstractmethod

class Heuristic(ABC):
    """
    Clase abstracta que representa una heurística para estimar el costo de un camino entre dos nodos.
    Attributes:
    goal_node (Node): El nodo de destino al que se desea llegar.
    Methods:
        __init__(self, goal_node: Node): Inicializa una nueva heurística con el nodo de destino dado.
        estimate(self, from_node: Node) -> float: Estima el costo de un camino desde un nodo dado al nodo de destino.
        estimate_between(self, from_node: Node, to_node: Node) -> float: Calcula el costo estimado entre dos nodos.
    """
    def __init__(self, goal_node: Node):
        self.goal_node = goal_node
    
    def estimate(self, from_node: Node) -> float:
        return self.estimate_between(from_node, self.goal_node)
    
    @abstractmethod
    def estimate_between(self, from_node: Node, to_node: Node) -> float:
        """Calculate the estimated cost between any two nodes"""
        pass