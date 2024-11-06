# @file pathfindingList.py
# @brief Implementación de la lista de pathfinding
# @author Anya Marcano
# @date 2024/11/05

from dataclasses import dataclass
from nodes import Node
from connection import Connection
from typing import List, Optional
@dataclass
class NodeRecord:
    """
    Clase que representa un nodo en la lista de pathfinding
    Atributos:
        node (Node): El nodo que representa este registro
        connection (Connection): La conexión que lleva a este nodo desde el nodo anterior
        cost_so_far (float): El costo acumulado para llegar a este nodo
        estimated_total_cost (float): El costo total estimado para llegar a la meta desde este nodo
    """
    node: Node
    connection: Optional[Connection] = None
    cost_so_far: float = float('inf')
    estimated_total_cost: float = float('inf')
class PathfindingList:
    """
    Clase que representa una lista de pathfinding
    Atributos:
        records (List[NodeRecord]): Una lista de registros de nodos
        Métodos:
            __init__(self): Inicializa una nueva lista de pathfinding sin registros.
            __len__(self): Devuelve la cantidad de registros en la lista.
            add(self, record: NodeRecord): Agrega un nuevo registro a la lista.
            remove(self, record: NodeRecord): Elimina un registro de la lista.
            contains(self, node: Node) -> bool: Devuelve si la lista contiene un nodo dado.
            find(self, node: Node) -> Optional[NodeRecord]: Encuentra un registro en la lista dado un nodo.
            smallest_element(self) -> NodeRecord: Devuelve el registro con el menor costo total estimado.
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
        return min(self.records, key=lambda x: x.estimated_total_cost)
