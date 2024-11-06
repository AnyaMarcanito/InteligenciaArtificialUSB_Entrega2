# @file kinematicFlee.py
# @brief Implementación de un comportamiento de huida cinemática para un personaje en un espacio 2D.
# @author Anya Marcano
# @date 2024/11/05

import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movements.static import static
from pygame import Vector2 as Vector
from Movements.kinematicSteeringOutput import KinematicSteeringOutput

class KinematicFlee:
    """
    Una clase para representar el comportamiento de huida cinemática para un personaje en un espacio 2D.
    Atributos
    ----------
    character : static
        El personaje que está huyendo.
    target : static
        El objetivo del cual el personaje está huyendo.
    maxSpeed : float
        La velocidad máxima a la que el personaje puede moverse.
    maxDistance : float
        La distancia máxima a la que el comportamiento de huida está activo.
    screen_width : int
        El ancho de la pantalla.
    screen_height : int
        La altura de la pantalla.
    Métodos
    -------
    getSteering() -> KinematicSteeringOutput:
        Calcula la salida de dirección para que el personaje huya del objetivo.
    getEdgeForce() -> Vector:
        Calcula la fuerza a aplicar cuando el personaje está cerca de los bordes de la pantalla.
    newOrientation(current: float, velocity: Vector) -> float:
        Calcula la nueva orientación del personaje basada en su velocidad.
    """
    def __init__(self, character: static, target: static, maxSpeed: float, maxDistance: float, screen_width: int, screen_height: int):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.maxDistance = maxDistance
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def getSteering(self) -> KinematicSteeringOutput:
        result = KinematicSteeringOutput(Vector(0, 0), 0)
        
        direction = self.character.position - self.target.position
        distance = direction.magnitude()
        
        if distance > 0:
            result.velocity = direction.normalize() * self.maxSpeed 
        edge_force = self.getEdgeForce()
        result.velocity += edge_force
        
        self.character.orientation = self.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        
        return result
    
    def getEdgeForce(self) -> Vector:
        force = Vector(0, 0)
        edge_distance = 50 

        if self.character.position.x < edge_distance:
            force.x += self.maxSpeed * (1 - self.character.position.x / edge_distance)
        elif self.character.position.x > self.screen_width - edge_distance:
            force.x -= self.maxSpeed * (1 - (self.screen_width - self.character.position.x) / edge_distance)

        if self.character.position.y < edge_distance:
            force.y += self.maxSpeed * (1 - self.character.position.y / edge_distance)
        elif self.character.position.y > self.screen_height - edge_distance:
            force.y -= self.maxSpeed * (1 - (self.screen_height - self.character.position.y) / edge_distance)

        return force
        
    def newOrientation(self, current: float, velocity: Vector) -> float:
        if velocity.magnitude() > 0:
            return math.atan2(velocity.y, velocity.x)
        else:
            return current