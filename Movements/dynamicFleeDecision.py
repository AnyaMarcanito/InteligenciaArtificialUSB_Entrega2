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
    def __init__(self, enemy_pos, player_pos, detection_radius_large, detection_radius_small, dynamic_flee, patrol_action):
        super().__init__(patrol_action, dynamic_flee)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.detection_radius_large = detection_radius_large
        self.detection_radius_small = detection_radius_small
        self.dynamic_flee = dynamic_flee
        self.patrol_action = patrol_action

    def test_value(self):
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance <= self.detection_radius_small:
            return "flee"
        elif distance <= self.detection_radius_large:
            return "stop"
        else:
            return "patrol"
        
    def make_decision(self):
        decision = self.test_value()
        if decision == "flee":
            return self.dynamic_flee
        elif decision == "stop":
            return "stop"
        else:
            return self.patrol_action