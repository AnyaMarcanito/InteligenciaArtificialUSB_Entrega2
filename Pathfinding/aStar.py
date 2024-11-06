# @file aStar.py
# @brief Implementación del algoritmo A* para encontrar el camino más corto entre dos nodos
# @author Anya Marcano
# @date 2024/11/05

from typing import List, Optional
from graph import Graph
from nodes import Node
from connection import Connection
from heuristic import Heuristic
from pathfindingList import NodeRecord, PathfindingList

def pathfind_astar(graph: Graph, start: Node, goal: Node, heuristic: Heuristic) -> Optional[List[Connection]]:
    """
    Implementa el algoritmo A* para encontrar el camino más corto entre dos nodos en un grafo.
    Args:
        graph (Graph): El grafo en el cual realizar la búsqueda de caminos.
        start (Node): El nodo de inicio.
        goal (Node): El nodo objetivo.
        heuristic (Heuristic): La función heurística para estimar el costo desde un nodo hasta el objetivo.
    Returns:
        Optional[List[Connection]]: Una lista de conexiones que representan el camino más corto desde el inicio hasta el objetivo,
                                    o None si no se encuentra ningún camino.
    """
    # Inicializar el nodo de inicio
    start_record = NodeRecord(
        node=start,
        cost_so_far=0,
        estimated_total_cost=heuristic.estimate(start)
    )
    
    # Inicializar las listas abierta y cerrada
    open_list = PathfindingList()
    open_list.add(start_record)
    closed_list = PathfindingList()
    
    # Iterar hasta que la lista abierta esté vacía
    while len(open_list) > 0:
        current = open_list.smallest_element()
        
        # Si el nodo actual es el objetivo, terminar
        if current.node == goal:
            break
            
        # Calcular los costos de los nodos adyacentes   
        connections = graph.get_connections(current.node)
        
        # Iterar sobre las conexiones
        for connection in connections:
            end_node = connection.to_node
            end_node_cost = current.cost_so_far + connection.get_cost()
            
            # Manejar nodos cerrados
            if closed_list.contains(end_node):
                end_node_record = closed_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
                closed_list.remove(end_node_record)
                end_node_heuristic = end_node_record.estimated_total_cost - end_node_record.cost_so_far
                
            # Manejar nodos abiertos
            elif open_list.contains(end_node):
                end_node_record = open_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
                end_node_heuristic = end_node_record.estimated_total_cost - end_node_record.cost_so_far
                
            # Manekar nodos no visitados
            else:
                end_node_record = NodeRecord(node=end_node)
                end_node_heuristic = heuristic.estimate(end_node)
            
            # Actualizar el nodo
            end_node_record.cost_so_far = end_node_cost
            end_node_record.connection = connection
            end_node_record.estimated_total_cost = end_node_cost + end_node_heuristic
            
            # Agregar el nodo a la lista abierta si no está allí
            if not open_list.contains(end_node):
                open_list.add(end_node_record)
                
        # Mpver el nodo actual a la lista cerrada
        open_list.remove(current)
        closed_list.add(current)
    
    # Retornar None si no se encontró un camino
    if current.node != goal:
        return None
        
    # Reconstruir el camino
    path = []
    
    # Iterar desde el nodo objetivo hasta el nodo de inicio
    while current.node != start:
        path.append(current.connection)
        current = closed_list.find(current.connection.from_node)
        
    # Invertir el camino
    path.reverse()
    return path