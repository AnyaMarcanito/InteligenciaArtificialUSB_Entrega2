# @file kinematicFleeDecision.py
# @brief Implementación de decisiones para el comportamiento de Flee en NPC
# @author Anya Marcano
# @date 2024/11/05

import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DecisionTree.decision_tree import Action, Decision
from Movements.static import static
from pygame import Vector2 as Vector
from Movements.kinematicFlee import KinematicFlee

class KinematicFleeAction(Action):
    """
    Una clase para representar la acción de huida cinemática para un personaje enemigo en un juego.
    Atributos
    ---------
    enemy : dict
        Un diccionario que contiene la posición del enemigo con las claves "x" y "y".
    player : tuple
        Una tupla que contiene la posición del jugador (x, y).
    max_speed : float
        La velocidad máxima a la que el enemigo puede huir.
    max_distance : float
        La distancia máxima dentro de la cual el enemigo comenzará a huir del jugador.
    screen_width : int
        El ancho de la pantalla del juego.
    screen_height : int
        La altura de la pantalla del juego.
    min_x : int
        El límite mínimo de la coordenada x para el movimiento del enemigo.
    max_x : int
        El límite máximo de la coordenada x para el movimiento del enemigo.
    Métodos
    -------
    make_decision():
        Determina si el enemigo debe huir en función de la posición del jugador y actualiza la posición del enemigo en consecuencia.
    """
    def __init__(self, enemy, player, max_speed, max_distance, screen_width, screen_height, min_x, max_x):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.min_x = min_x
        self.max_x = max_x

    def getSteering(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.player[1]), 0)
        
        flee_behavior = KinematicFlee(
            enemy_static,
            player_static,
            self.max_speed,
            self.max_distance,
            self.screen_width,
            self.screen_height
        )
        
        return flee_behavior.getSteering()
    
    def make_decision(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.player[1]), 0)
        
        dx = self.enemy["x"] - self.player[0]
        dy = self.enemy["y"] - self.player[1]
        distance = (dx*dx + dy*dy)**0.5
        
        if distance <= self.max_distance:
            flee_behavior = KinematicFlee(
                enemy_static,
                player_static,
                self.max_speed,
                self.max_distance,
                self.screen_width,
                self.screen_height
            )
            steering = flee_behavior.getSteering()
            if steering:
                new_x = self.enemy["x"] + steering.velocity.x
                if self.min_x + steering.velocity.x <= new_x <= self.max_x+ steering.velocity.x:
                    self.enemy["x"] = new_x
                    self.enemy["y"] = enemy_static.position.y
                    
            return flee_behavior
        return None
    
class KinematicFleeDecision(Decision):
    def __init__(self, enemy, player_pos, player_attacking, detection_radius, kinematic_flee, attack_action, patrol_action, min_x, max_x):
        super().__init__(attack_action, patrol_action)
        self.enemy = enemy
        self.player_pos = player_pos
        self.player_attacking = player_attacking
        self.detection_radius = detection_radius
        self.kinematic_flee = kinematic_flee
        self.min_x = min_x
        self.max_x = max_x

    def test_value(self):
        # Calcula la distancia al jugador
        dx = self.player_pos[0] - self.enemy["x"]
        dy = self.player_pos[1] - self.enemy["y"]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Verifica si está en rango
        return distance <= self.detection_radius
        
    def make_decision(self):
        if self.test_value():
            if self.player_attacking:
                return self.kinematic_flee
            return "attack"
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