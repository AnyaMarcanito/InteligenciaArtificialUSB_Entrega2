# @file kinematicSteeringOutput.py
# @brief Implementación de la clase KinematicSteeringOutput
# @author Anya Marcano
# @date 2024/11/05

from pygame import Vector2 as Vector

class KinematicSteeringOutput:
    def __init__(self, velocity: Vector, rotation: float):
        self.velocity = velocity
        self.rotation = rotation
    