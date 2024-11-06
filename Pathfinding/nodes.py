# @file nodes.py
# @brief Implementación de las clases Node y TileNode, que representan nodos en un algoritmo de búsqueda de caminos.
# @author Anya Marcano
# @date 2024/11/05

class Node:
    """
    Clase abstracta que representa un nodo en un algoritmo de búsqueda de caminos.
    Attributes:
        name (str): El nombre del nodo.
        Methods:
            __init__(self, name: str): Inicializa un nuevo nodo con el nombre dado.
    """
    def __init__(self, name):
        self.name = name

class TileNode(Node):
    """
    Clase que representa un nodo en un grafo de nodos de mosaico.
    Attributes:
        x (int): La coordenada x del nodo.
        y (int): La coordenada y del nodo.
        Methods:
            __init__(self, x: int, y: int): Inicializa un nuevo nodo de mosaico con las coordenadas dadas.
    """
    def __init__(self, x: int, y: int):
        super().__init__(f"tile_{x}_{y}")
        self.x = x
        self.y = y