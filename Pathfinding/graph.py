# @file graph.py
# @brief Implementación de la clase Graph, que representa un grafo de conexiones entre nodos
# @author Anya Marcano
# @date 2024/11/05

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from connection import Connection
from nodes import Node

class Graph:
    """
    Esta clase encapsula un grafo de conexiones entre nodos en un algoritmo de búsqueda de caminos.
    Incluye un diccionario de conexiones con nodos de inicio como claves y una lista de conexiones como valores.
    Attributes:
        connections (dict): Un diccionario que mapea nodos de inicio a una lista de conexiones.
        Methods:
            __init__(self): Inicializa un nuevo grafo sin conexiones.
            add_connection(self, from_node: Node, to_node: Node, cost: float): Agrega una nueva conexión al grafo.
            get_connections(self, from_node: Node) -> list[Connection]: Devuelve una lista de conexiones para un nodo de inicio dado.
    """
    def __init__(self):
        self.connections = {}

    def add_connection(self, from_node: Node, to_node: Node, cost: float):
        if from_node not in self.connections:
            self.connections[from_node] = []
        self.connections[from_node].append(Connection(from_node, to_node, cost))

    def get_connections(self, from_node: Node) -> list[Connection]:
        return self.connections.get(from_node, [])