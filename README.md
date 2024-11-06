# InteligenciaArtificialUSB_Entrega2
## Estudiante

Anya Marcano, 19-10336

## Descripción
Este proyecto implementa un sistema de inteligencia artificial para un juego, utilizando técnicas de pathfinding, decisiones basadas en árboles de decisión y movimientos cinemáticos. El objetivo es crear NPCs (personajes no jugables) que puedan tomar decisiones y moverse de manera inteligente en el mundo del juego.

## Estructura del Proyecto
El proyecto está organizado en los siguientes directorios:

- **Assets/**: Contiene los recursos gráficos y otros activos del juego.
- **DecisionTree/**: Implementa la lógica de los árboles de decisión.
  - `decision_tree.py`: Contiene la implementación del árbol de decisión.
- **Movements/**: Implementa los diferentes tipos de movimientos cinemáticos.
  - `kinematicArrive.py`: Movimiento de llegada cinemático.
  - `kinematicArriveDecision.py`: Decisión de llegada cinemática.
  - `kinematicFlee.py`: Movimiento de huida cinemático.
  - `kinematicFleeDecision.py`: Decisión de huida cinemática.
  - `kinematicSteeringOutput.py`: Salida de dirección cinemática.
  - `static.py`: Movimiento estático.
- **Pathfinding/**: Implementa los algoritmos de pathfinding.
  - `aStar.py`: Algoritmo A*.
  - `connection.py`: Conexiones entre nodos.
  - `dijkstra.py`: Algoritmo de Dijkstra.
  - `graph.py`: Representación del grafo.
  - `heuristic.py`: Heurísticas para pathfinding.
  - `manhattanHeuristic.py`: Heurística de Manhattan.
  - `nodes.py`: Nodos del grafo.
  - `pathfindingList.py`: Lista de pathfinding.
- **Utils/**: Funciones utilitarias.
  - `functions.py`: Funciones auxiliares.
- **WorldRepresentation/**: Representación del mundo del juego.
  - `main.py`: Archivo principal que ejecuta el juego.
  - `tileGraph.py`: Representación gráfica del mundo en tiles.

## Ejecución

Desde el directorio WorldRepresentation/ ejecutar 
```bash
python main.py
```