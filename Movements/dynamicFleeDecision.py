# @file dynamicFleeDecision.py
# @brief Implementación de decisiones para el comportamiento de Flee dinámico en NPC
# @autor Anya Marcano
# @date 2024/11/05

import sys, os, math
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
class DynamicFleeDecision(Decision):
    def __init__(self, enemy_pos, player_pos, detection_radius, dynamic_flee):
        super().__init__(None, dynamic_flee)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.detection_radius = detection_radius
        self.dynamic_flee = dynamic_flee

    def test_value(self):
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance <= self.detection_radius
        
    def make_decision(self):
        if self.test_value():
            return self.dynamic_flee
        return None