# @file kinematicArrive.py
# @brief Implementación de un comportamiento de llegada cinemática para un personaje.
# @author Anya Marcano
# @date 2024/11/05

import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movements.static import static
from pygame import Vector2 as Vector
from Movements.kinematicSteeringOutput import KinematicSteeringOutput

class KinematicArrive:
    """
    Una clase para representar el comportamiento de llegada cinemática para un personaje.
    Atributos:
    ----------
    character : static
        El personaje que se está moviendo.
    target : static
        El objetivo hacia el cual se mueve el personaje.
    maxSpeed : float
        La velocidad máxima a la que puede moverse el personaje.
    radius : float
        El radio dentro del cual se considera que el personaje ha llegado al objetivo.
    timeToTarget : float
        El tiempo en segundos en el que el personaje intenta alcanzar el objetivo.
    Métodos:
    -------
    getSteering() -> KinematicSteeringOutput:
        Calcula la salida de dirección para el comportamiento de llegada cinemática.
    newOrientation(current: float, velocity: Vector) -> float:
        Calcula la nueva orientación basada en la orientación actual y la velocidad.
    """
    def __init__(self, character: static, target: static, maxSpeed: float, radius: float):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.radius = radius
        self.timeToTarget = 0.25
    
    def getSteering(self) -> KinematicSteeringOutput:
        result = KinematicSteeringOutput(Vector(0, 0), 0)
        # Se obtiene la dirección al objetivo
        result.velocity = self.target.position - self.character.position
        # Se chequea si estamos dentro del radio
        if result.velocity.magnitude() < self.radius:
            return None
        # Debemos movernos al objetivo, y queremos alcanzarlo en el tiempo timeToTarget en segundos
        result.velocity = result.velocity * (1 / self.timeToTarget)
        # Si es muy rápido, llevarlo a la máxima velocidad
        if result.velocity.magnitude() > self.maxSpeed:
            result.velocity = result.velocity.normalize() * self.maxSpeed
        # Se actualiza la orientación
        self.character.orientation = self.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        return result
    
    def newOrientation(self, current: float, velocity: Vector) -> float:
        if velocity.magnitude() > 0:
            return math.atan2(velocity.y, velocity.x)
        else:
            return current