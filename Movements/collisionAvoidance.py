from pygame import Vector2 as Vector
from Movements.steeringOutput import SteeringOutput
import pygame

class CollisionAvoidance:
    def __init__(self, character, obstacles, max_avoid_force, avoid_radius):
        self.character = character
        self.obstacles = obstacles
        self.max_avoid_force = max_avoid_force
        self.avoid_radius = avoid_radius

    def getSteering(self):
        result = SteeringOutput()
        character_position = pygame.math.Vector2(self.character["x"], self.character["y"])
        for obstacle in self.obstacles:
            if obstacle is None:
                continue
            obstacle_position = pygame.math.Vector2(obstacle["x"], obstacle["y"])
            direction = obstacle_position - character_position
            distance = direction.length()
            if distance < self.avoid_radius and distance > 0:
                direction = direction.normalize()
                avoid_force = direction * self.max_avoid_force * (self.avoid_radius - distance) / self.avoid_radius
                result.linear -= avoid_force
        return result