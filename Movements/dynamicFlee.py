from Movements.steeringOutput import SteeringOutput
from pygame import Vector2 as Vector

class DynamicFlee:
    def __init__(self, character, target, maxAcceleration, fleeRadius):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.fleeRadius = fleeRadius

    def getSteering(self):
        result = SteeringOutput()
        direction = self.character.position - self.target.position
        distance = direction.length()
        if distance > self.fleeRadius:
            return None
        direction.normalize()
        result.linear = direction * self.maxAcceleration
        result.angular = 0
        return result