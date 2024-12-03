# @file dynamicArriveDecision.py
# @brief Implementación de decisiones para el comportamiento de DynamicArrive en NPC
# @autor Anya Marcano
# @date 2024/11/05

import sys, os, math, pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DecisionTree.decision_tree import Action, Decision
from Movements.static import static
from pygame import Vector2 as Vector
from Movements.dynamicArrive import DynamicArrive
from Movements.steeringOutput import SteeringOutput

class DynamicArriveAction(Action):
    """
    Representa una acción donde un personaje enemigo llega a la posición del jugador usando movimiento dinámico.
    Atributos:
        enemy (dict): Un diccionario que contiene la posición del enemigo con las claves "x" y "y".
        player (tuple): Una tupla que contiene la posición del jugador (x, y).
        max_speed (float): La velocidad máxima a la que el enemigo puede moverse.
        max_acceleration (float): La aceleración máxima que el enemigo puede alcanzar.
        arrival_radius (float): El radio dentro del cual el enemigo comienza a desacelerar para llegar a la posición del jugador.
        slow_radius (float): El radio dentro del cual el enemigo comienza a desacelerar.
    Métodos:
        make_decision():
            Crea y devuelve un objeto DynamicArrive basado en las posiciones actuales del enemigo y el jugador.
    """
    def __init__(self, enemy, player, max_speed, max_acceleration, arrival_radius, slow_radius):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.arrival_radius = arrival_radius
        self.slow_radius = slow_radius
        
    def make_decision(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.player[1]), 0)
        return DynamicArrive(enemy_static, player_static, self.max_acceleration, self.max_speed, self.arrival_radius, self.slow_radius)

class PatrolAction(Action):
    """
    PatrolAction es una clase que representa una acción donde un enemigo patrulla en una dirección dada.
    Atributos:
        enemy: El enemigo que realizará la acción de patrullar.
        direction: La dirección en la que el enemigo patrullará.
    Métodos:
        make_decision():
            Devuelve la cadena "patrol" indicando la decisión de patrullar.
    """
    def __init__(self, enemy, direction):
        self.enemy = enemy
        self.direction = direction
        
    def make_decision(self):
        return "patrol"

class InRangeDecision(Decision):
    """
    InRangeDecision es una clase de toma de decisiones que determina si un enemigo está dentro de un rango dado de un jugador.
    Atributos:
        enemy_pos (tuple): La posición (x, y) del enemigo.
        player_pos (tuple): La posición (x, y) del jugador.
        true_node (DecisionNode): El nodo a ejecutar si la decisión es verdadera.
        false_node (DecisionNode): El nodo a ejecutar si la decisión es falsa.
        range (float): El rango dentro del cual se considera que el enemigo está dentro del rango.
        test_function (function): La función que se utilizará para probar si el enemigo está dentro del rango.
    Métodos:
        test_value(): Calcula la distancia entre el enemigo y el jugador y verifica si el enemigo está dentro del rango especificado.
    """
    def __init__(self, enemy_pos, player_pos, true_node, false_node, test_function):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.test_function = test_function
        
    def test_value(self):
        return self.test_function(self.enemy_pos, self.player_pos)

class AttackAction(Action):    
    """
    Representa una acción de ataque en un juego.
    Atributos:
        enemy: El enemigo objetivo del ataque.
        direction: La dirección del ataque.
        attack_sprites_right: Los sprites utilizados para la animación del ataque cuando se mira hacia la derecha.
        attack_sprites_left: Los sprites utilizados para la animación del ataque cuando se mira hacia la izquierda.
    Métodos:
        make_decision():
            Activa la acción de ataque y devuelve la cadena "attack".
    """
    def __init__(self, npc, player_position, arrival_radius, right_attack_sprites, left_attack_sprites):
        self.npc = npc
        self.player_position = player_position
        self.arrival_radius = arrival_radius
        self.right_attack_sprites = right_attack_sprites
        self.left_attack_sprites = left_attack_sprites
        
    def make_decision(self):
        return "attack"

class PlayerReachedDecision(Decision):
    """
    PlayerReachedDecision es una clase de toma de decisiones que determina si un jugador ha alcanzado una cierta posición relativa a un enemigo.
    Atributos:
        enemy_pos (tuple): La posición (x, y) del enemigo.
        player_pos (tuple): La posición (x, y) del jugador.
        true_node (DecisionNode): El nodo a ejecutar si la decisión es verdadera.
        false_node (DecisionNode): El nodo a ejecutar si la decisión es falsa.
        arrival_radius (float): El radio dentro del cual se considera que el jugador ha llegado.
    Métodos:
        test_value(): Calcula la distancia entre el jugador y el enemigo, y verifica si el jugador ha llegado dentro del radio especificado y si la decisión del false_node es una instancia de DynamicArrive.
    """
    def __init__(self, enemy_pos, player_pos, true_node, false_node, arrival_radius):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.arrival_radius = arrival_radius
        
    def test_value(self):
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance <= self.arrival_radius

class DisappearAction(Action):
    def __init__(self, enemy, direction, disappear_sprites_right, disappear_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.disappear_sprites_right = disappear_sprites_right
        self.disappear_sprites_left = disappear_sprites_left
        
    def make_decision(self):
        return "disappear"

# Clase que representa la decisión del jugador cuando está atacando
class PlayerAttackingInRangeDecision(Decision):
    def __init__(self, enemy_pos, player_pos, player_attacking, detection_radius, true_node, false_node):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.player_attacking = player_attacking
        self.detection_radius = detection_radius
        
    def test_value(self):
        dx = self.player_pos[0] - self.enemy_pos[0]
        dy = self.player_pos[1] - self.enemy_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)

        return self.player_attacking and distance <= self.detection_radius
    
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

class SteeringOutput:
    def __init__(self, x, y):
        self.linear = pygame.math.Vector2(x, y)

class AttackAction:
    def __init__(self, npc, player_position, arrival_radius, right_attack_sprites, left_attack_sprites):
        self.npc = npc
        self.player_position = player_position
        self.arrival_radius = arrival_radius
        self.right_attack_sprites = right_attack_sprites
        self.left_attack_sprites = left_attack_sprites

    def perform_attack(self):
        # Lógica de ataque
        pass

class ReturnToOriginalPositionActionForEriol:
    def __init__(self, npc, original_position, chase_speed):
        self.npc = npc
        self.original_position = original_position  # Asegúrate de que esto sea una tupla
        self.chase_speed = chase_speed

    def getSteering(self):
        direction = pygame.math.Vector2(self.original_position[0] - self.npc["x"], self.original_position[1] - self.npc["y"])
        if direction.length() > 0:
            direction = direction.normalize() * self.chase_speed
        return SteeringOutput(direction.x, direction.y)
    
class CollisionAvoidanceForEriol:
    def __init__(self, npc, obstacles, max_avoid_force=1.0, avoid_radius=50):
        self.npc = npc
        self.obstacles = obstacles
        self.max_avoid_force = max_avoid_force
        self.avoid_radius = avoid_radius

    def getSteering(self):
        steering = pygame.math.Vector2(0, 0)
        for obstacle in self.obstacles:
            if obstacle is None:
                continue
            direction = pygame.math.Vector2(obstacle["x"] - self.npc["x"], obstacle["y"] - self.npc["y"])
            distance = direction.length()
            if distance < self.avoid_radius and distance > 0:
                direction = direction.normalize()
                avoid_force = self.max_avoid_force * (self.avoid_radius - distance) / self.avoid_radius
                steering += direction * avoid_force
        return SteeringOutput(steering.x, steering.y)