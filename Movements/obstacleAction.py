import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DecisionTree.decision_tree import Action, Decision
from Movements.static import static
from pygame import Vector2 as Vector
from Movements.kinematicFlee import KinematicFlee

# Clase para definir la acción de atacar
class BombAttackAction(Action):
    def __init__(self, player, direction, attack_sprites_right, attack_sprites_left):
        self.player = player
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        return "attack"

# Clase para definir la acción de huir
class BombFleeAction(Action):
    def __init__(self, player, bombs, max_speed, max_distance, screen_width, screen_height):
        self.player = player
        self.bombs = bombs
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def getSteering(self):
        player_static = static(Vector(self.player[0], self.player[1]), 0)
        
        center_x = sum(bomb["x"] for bomb in self.bombs) / len(self.bombs)
        center_y = sum(bomb["y"] for bomb in self.bombs) / len(self.bombs)
        bombs_center = static(Vector(center_x, center_y), 0)
        # No se pudo implementar el flee
        flee_behavior = KinematicFlee(
            player_static,
            bombs_center,
            self.max_speed,
            self.max_distance,
            self.screen_width,
            self.screen_height
        )
        
        return flee_behavior.getSteering()

# Clase para definir la decisión de atacar o huir
class BombInteractionDecision(Decision):
    def __init__(self, player_pos, bombs, detection_radius, attack_action, flee_action):
        super().__init__(attack_action, flee_action)
        self.player_pos = player_pos
        self.bombs = bombs
        self.detection_radius = detection_radius
        
    def get_bombs_in_range(self):
        bombs_in_range = []
        for bomb in self.bombs:
            dx = self.player_pos[0] - bomb["x"]
            dy = self.player_pos[1] - bomb["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= self.detection_radius:
                bombs_in_range.append(bomb)
        return bombs_in_range
        
    def make_decision(self):
        bombs_in_range = self.get_bombs_in_range()
        
        if len(bombs_in_range) == 0:
            return None
        elif len(bombs_in_range) == 1:
            # Se ataca
            return "attack"
        else:
            # Huir
            return self.false_node
    
    def test_value(self):
        bombs_in_range = self.get_bombs_in_range()
        return len(bombs_in_range) == 1