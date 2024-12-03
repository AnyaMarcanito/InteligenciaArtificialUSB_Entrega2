# @file dynamicFleeDecision.py
# @brief Implementación de decisiones para el comportamiento de Flee dinámico en NPC
# @autor Anya Marcano
# @date 2024/11/05

import sys, os, math, pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DecisionTree.decision_tree import Action, Decision
from pygame import Vector2 as Vector
from Movements.dynamicFlee import DynamicFlee
from Movements.steeringOutput import SteeringOutput

class DynamicFleeAction(Action):
    def __init__(self, enemy, player, max_acceleration, flee_radius):
        self.enemy = enemy
        self.player = player
        self.max_acceleration = max_acceleration
        self.flee_radius = flee_radius
        
    def getSteering(self):
        enemy_position = Vector(self.enemy["x"], self.enemy["y"])
        player_position = Vector(self.player[0], self.player[1])
        
        direction = enemy_position - player_position
        distance = direction.length()
        
        if distance > self.flee_radius:
            return None
        
        direction.normalize()
        steering = direction * self.max_acceleration
        
        return SteeringOutput(linear=steering, angular=0)
    
    def make_decision(self):
        return self.getSteering()
class DynamicFleeDecision:
    def __init__(self, npc_position, player_position, detection_radius, dynamic_flee, move_to_book_action, follow_player_action, return_to_original_position_action):
        self.npc_position = npc_position
        self.player_position = player_position
        self.detection_radius = detection_radius
        self.detection_radius_small = detection_radius * 0.1  # Ajusta este valor según sea necesario
        self.detection_radius_large = detection_radius * 1.5  # Ajusta este valor según sea necesario
        self.dynamic_flee = dynamic_flee
        self.move_to_book_action = move_to_book_action
        self.follow_player_action = follow_player_action
        self.return_to_original_position_action = return_to_original_position_action

    def test_value(self):
        distance = ((self.player_position[0] - self.npc_position[0]) ** 2 + (self.player_position[1] - self.npc_position[1]) ** 2) ** 0.5
        if distance <= self.detection_radius_small:
            return self.dynamic_flee
        elif distance <= self.detection_radius:
            return self.follow_player_action
        else:
            return self.return_to_original_position_action

    def make_decision(self):
        decision = self.test_value()
        return decision
    
class MoveToBookAction:
    def __init__(self, npc, book_position, speed):
        self.npc = npc
        self.book_position = book_position
        self.speed = speed

    def getSteering(self):
        direction = pygame.math.Vector2(self.book_position["x"] - self.npc["x"], self.book_position["y"] - self.npc["y"])
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        return direction
    

class FollowPlayerAction:
    def __init__(self, npc, player_position, speed):
        self.npc = npc
        self.player_position = player_position
        self.speed = speed

    def getSteering(self):
        direction = pygame.math.Vector2(self.player_position[0] - self.npc["x"], self.player_position[1] - self.npc["y"])
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        return direction
    
class MoveToPlayerAction:
    def __init__(self, npc, player_position, chase_speed):
        self.npc = npc
        self.player_position = player_position
        self.chase_speed = chase_speed

    def getSteering(self):
        direction = pygame.math.Vector2(self.player_position[0] - self.npc["x"], self.player_position[1] - self.npc["y"])
        if direction.length() > 0:
            direction = direction.normalize() * self.chase_speed
        return SteeringOutput(direction.x, direction.y)
    
class ReturnToOriginalPositionAction:
    def __init__(self, npc, original_position, speed):
        self.npc = npc
        self.original_position = original_position
        self.speed = speed

    def getSteering(self):
        direction = pygame.math.Vector2(self.original_position["x"] - self.npc["x"], self.original_position["y"] - self.npc["y"])
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        return direction