# @file kinematicArriveDecision.py
# @brief Implementación de decisiones para el comportamiento de Arrive en NPC
# @author Anya Marcano
# @date 2024/11/05

import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DecisionTree.decision_tree import Action, Decision
from Movements.static import static
from pygame import Vector2 as Vector
from Movements.kinematicArrive import KinematicArrive

class KinematicArriveAction(Action):
    """
    Representa una acción donde un personaje enemigo llega a la posición del jugador usando movimiento cinemático.
    Atributos:
        enemy (dict): Un diccionario que contiene la posición del enemigo con las claves "x" y "y".
        player (tuple): Una tupla que contiene la posición del jugador (x, y).
        max_speed (float): La velocidad máxima a la que el enemigo puede moverse.
        arrival_radius (float): El radio dentro del cual el enemigo comienza a desacelerar para llegar a la posición del jugador.
    Métodos:
        make_decision():
            Crea y devuelve un objeto KinematicArrive basado en las posiciones actuales del enemigo y el jugador.
    """
    def __init__(self, enemy, player, max_speed, arrival_radius):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.arrival_radius = arrival_radius
        
    def make_decision(self):
        enemy_static = static(Vector(self.enemy["x"], self.enemy["y"]), 0)
        player_static = static(Vector(self.player[0], self.enemy["y"]), 0)
        return KinematicArrive(enemy_static, player_static, self.max_speed, self.arrival_radius)

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
    def __init__(self, enemy, direction, attack_sprites_right, attack_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        print("Attack action triggered!")
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
        test_value(): Calcula la distancia entre el jugador y el enemigo, y verifica si el jugador ha llegado dentro del radio especificado y si la decisión del false_node es una instancia de KinematicArrive.
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
        return isinstance(self.false_node.make_decision(), KinematicArrive) and distance <= self.arrival_radius

class AttackAction(Action):
    def __init__(self, enemy, direction, attack_sprites_right, attack_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        return "attack"
