# @file dijkstra.py
# @brief Implementación del algoritmo de búsqueda de caminos de Dijkstra
# @author Anya Marcano
# @date 2024/11/05
from typing import List, Optional
from dataclasses import dataclass
from graph import Graph
from nodes import Node
from connection import Connection

@dataclass
class NodeRecord:
    """
    Esta clase encapsula un nodo en un algoritmo de búsqueda de caminos.
    Incluye el nodo, la conexión que llevó a este nodo y el costo total hasta este nodo.
    Attributes:
        node (Node): El nodo encapsulado.
        connection (Optional[Connection]): La conexión que llevó a este nodo.
        cost_so_far (float): El costo total hasta este nodo.
    """
    node: Node
    connection: Optional[Connection] = None
    cost_so_far: float = float('inf')

class PathfindingList:
    """
    Esta clase encapsula una lista de nodos en un algoritmo de búsqueda de caminos.
    Incluye una lista de registros de nodos.
    Attributes:
        records (List[NodeRecord]): La lista de registros de nodos.
        Methods:
        __init__(self): Inicializa una nueva lista de nodos.
        __len__(self): Devuelve la cantidad de registros de nodos en la lista.
        add(self, record: NodeRecord): Agrega un registro de nodo a la lista.
        remove(self, record: NodeRecord): Elimina un registro de nodo de la lista.
        contains(self, node: Node) -> bool: Devuelve True si la lista contiene el nodo dado.
        find(self, node: Node) -> Optional[NodeRecord]: Devuelve el registro de nodo correspondiente al nodo dado.
        smallest_element(self) -> NodeRecord: Devuelve el registro de nodo con el menor costo total.
    """
    def __init__(self):
        self.records: List[NodeRecord] = []
    
    def __len__(self):
        return len(self.records)
    
    def add(self, record: NodeRecord):
        self.records.append(record)
    
    def remove(self, record: NodeRecord):
        self.records.remove(record)
    
    def contains(self, node: Node) -> bool:
        return any(record.node == node for record in self.records)
    
    def find(self, node: Node) -> Optional[NodeRecord]:
        for record in self.records:
            if record.node == node:
                return record
        return None
    
    def smallest_element(self) -> NodeRecord:
        return min(self.records, key=lambda x: x.cost_so_far)

def pathfind_dijkstra(graph: Graph, start: Node, goal: Node) -> Optional[List[Connection]]:
    """
    Encuentra el camino más corto entre dos nodos en un grafo utilizando el algoritmo de Dijkstra.
    Args:
        graph (Graph): El grafo en el que se realizará la búsqueda.
        start (Node): El nodo de inicio del camino.
        goal (Node): El nodo de destino del camino.
        Returns:
        Optional[List[Connection]]: La lista de conexiones que forman el camino más corto, o None si no se encontró un camino.
    """
    # Inicializar el nodo de inicio
    start_record = NodeRecord(node=start, cost_so_far=0)
    
    # Inicializar las listas abierta y cerrada
    open_list = PathfindingList()
    open_list.add(start_record)
    closed_list = PathfindingList()
    
    # Iterar hasta que la lista abierta esté vacía
    while len(open_list) > 0:
        current = open_list.smallest_element()
        
        # Si el nodo actual es el nodo de destino, detener la búsqueda
        if current.node == goal:
            break
            
        # Conseguir las conexiones del nodo actual
        connections = graph.get_connections(current.node)
        
        # Iterar sobre las conexiones
        for connection in connections:
            end_node = connection.to_node
            end_node_cost = current.cost_so_far + connection.get_cost()
            
            # Si el nodo está en la lista cerrada, continuar
            if closed_list.contains(end_node):
                continue
                
            # Verificar si el nodo está en la lista abierta
            elif open_list.contains(end_node):
                end_node_record = open_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
            else:
                end_node_record = NodeRecord(node=end_node)
                
            # Actualizar el registro del nodo
            end_node_record.cost_so_far = end_node_cost
            end_node_record.connection = connection
            
            # Agregar el nodo a la lista abierta si no está allí
            if not open_list.contains(end_node):
                open_list.add(end_node_record)
                
        # Mover el nodo actual a la lista cerrada
        open_list.remove(current)
        closed_list.add(current)
    
    # Retornar None si no se encontró un camino
    if current.node != goal:
        return None
        
    # Reconstruir el camino
    path = []
    
    # Iterar desde el nodo de destino hasta el nodo de inicio
    while current.node != start:
        path.append(current.connection)
        current = closed_list.find(current.connection.from_node)
        
    # Devolver el camino en orden inverso
    path.reverse()
    return path