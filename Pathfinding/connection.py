# @file connection.py
# @brief Implmentacion de la clase Connection, que representa una conexion entre dos nodos
# @author Anya Marcano
# @date 2024/11/05

from nodes import Node

class Connection:
    """
    Esta clase encapsula una conexión entre dos nodos en un algoritmo de búsqueda de caminos. 
            Incluye el nodo de inicio, el nodo de destino y el costo asociado con la conexión.
    Attributes:
        from_node (Node): El nodo de inicio de la conexión.
        to_node (Node): El nodo de destino de la conexión.
        _cost (float): El costo asociado con la conexión.
    Methods:
        __init__(self, from_node: Node, to_node: Node, cost: float): Inicializa una nueva conexión con los nodos y el costo dados.
        get_cost(self) -> float: Devuelve el costo de la conexión.
        getFromNode(self) -> Node: Devuelve el nodo de inicio de la conexión.
        getToNode(self) -> Node: Devuelve el nodo de destino de la conexión.
    """
    def __init__(self, from_node: Node, to_node: Node, cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self._cost = cost

    def get_cost(self) -> float:
        return self._cost
    
    def getFromNode(self) -> Node:
        return self.from_node
    
    def getToNode(self) -> Node:
        return self.to_node