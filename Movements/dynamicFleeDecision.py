# @file dynamicFleeDecision.py
# @brief Implementación de decisiones para el comportamiento de Flee dinámico en NPC
# @autor Anya Marcano
# @date 2024/11/05

import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DecisionTree.decision_tree import Action, Decision
from pygame import Vector2 as Vector
from Movements.dynamicFlee import DynamicFlee

class static:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

class DynamicFleeAction(Action):
    def __init__(self, enemy, player, max_acceleration, flee_radius):
        self.enemy = enemy
        self.player = player
        self.max_acceleration = max_acceleration
        self.flee_radius = flee_radius
        
    def getSteering(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.player[1]), 0)
        
        flee_behavior = DynamicFlee(
            enemy_static,
            player_static,
            self.max_acceleration,
            self.flee_radius
        )
        
        return flee_behavior.getSteering()
    
    def make_decision(self):
        return self.getSteering() 
 
class DynamicFleeDecision(Decision):
    def __init__(self, enemy_pos, player_pos, player_attacking, detection_radius, dynamic_flee, patrol_action, min_x, max_x):
        super().__init__(patrol_action, dynamic_flee)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.player_attacking = player_attacking
        self.detection_radius = detection_radius
        self.dynamic_flee = dynamic_flee
        self.min_x = min_x
        self.max_x = max_x

    def test_value(self):
        # Calcula la distancia al jugador
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Verifica si está en rango
        return distance <= self.detection_radius
        
    def make_decision(self):
        if self.test_value():
            return self.dynamic_flee
        return "patrol"
   
class Exp2AttackAction(Action):
    def __init__(self, enemy, direction, attack_sprites_right, attack_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        self.enemy["is_attacking"] = True
        return "attack"

class PlayerAttackingDecision:
    def __init__(self, flee_action, attack_action):
        self.flee_action = flee_action
        self.attack_action = attack_action
        
    def make_decision(self, is_player_attacking):
        if is_player_attacking:
            return self.flee_action
        return self.attack_action