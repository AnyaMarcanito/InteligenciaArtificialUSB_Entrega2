from Movements.steeringOutput import SteeringOutput
from pygame import Vector2 as Vector

class DynamicFlee:
    """
    La clase Flee representa un comportamiento donde un personaje se aleja de un objetivo cuando entra dentro de un cierto radio.
    Atributos:
        character: Kinematic
            El personaje que exhibirá el comportamiento de huida.
        target: Kinematic
            El objetivo del cual el personaje huirá.
        maxAcceleration: float
            La aceleración máxima que el personaje puede alcanzar.
        fleeRadius: float
            El radio dentro del cual el personaje comenzará a huir del objetivo.
    Métodos:
        getSteering():
            Calcula y devuelve la salida de dirección para el comportamiento de huida. Si el objetivo está fuera del radio de huida,
            el personaje se detiene. De lo contrario, acelera alejándose del objetivo.
    """
    def __init__(self, character, target, maxAcceleration, fleeRadius):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.fleeRadius = fleeRadius

    def getSteering(self):
        result = SteeringOutput()
        # Calcular la dirección y la distancia al objetivo.
        direction = self.character.position - self.target.position
        distance = direction.length()
        # Si el objetivo está fuera del radio de huida, detenerse.
        if distance > self.fleeRadius:
            self.character.velocity = Vector(0, 0)
            result.linear = Vector(0, 0)
            result.angular = 0
            return result
        # Si el objetivo está dentro del radio de huida, acelerar alejándose del objetivo.
        result.linear = direction.normalize() * self.maxAcceleration
        result.angular = 0
        # Devolver la salida de dirección.
        return result