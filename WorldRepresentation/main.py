# @file main.py
# @brief Implementación de un juego de Sakura Card Captor con pathfinding y decisiones de comportamiento.
# @author Anya Marcano
# @date 2024/11/05

import pygame, sys
from tileGraph import TileGraph
from Movements.kinematicArrive import KinematicArrive
from Movements.kinematicFlee import KinematicFlee
from Movements.kinematicArriveDecision import KinematicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision
from Movements.kinematicFleeDecision import KinematicFleeAction
from pygame.locals import *
from Utils.functions import *
import math

# PANTALLA --------------------------------------------------------------------------------------------------------------------------------
# Inicialización del juego
pygame.init()
pygame.display.set_caption("🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸 SakuraCardCaptor 🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸")

# Configuración de la pantalla
screen_width, screen_height = 1270, 700
SCREEN = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load(".\Assets\disenoFondo.png").convert()

# Configuración del zoom en el mapa
ZOOM = 3
scaled_maze = pygame.transform.scale(
    background, 
    (int(background.get_width() * ZOOM), 
     int(background.get_height() * ZOOM))
)
SCREEN.blit(background, (0,0))

# Configuracion para el World Representation (Tile Graph)
tile_size = 32
tile_graph = TileGraph(scaled_maze, tile_size)
maze_mask = pygame.mask.from_surface(scaled_maze)
show_path = False

# Configuración de la cámara y limites del mundo
camera_x = 0
camera_y = 0
CAMERA_MARGIN = 200
MAP_WIDTH = scaled_maze.get_width()
MAP_HEIGHT = scaled_maze.get_height()

# Control de FPS
clock = pygame.time.Clock()

# PLAYER -> SAKURA --------------------------------------------------------------------------------------------------------------------------------

# Velocidad y contador de pasos para la animación
PLAYER_animation_speed = 0.2
PLAYER_steps = 0

# Velocidad de movimiento, posición y direccion inicial del jugador
PLAYER_x = 50
PLAYER_y = 500
PLAYER_direction = 'right'
PLAYER_MOVEMENT_SPEED = 4
PLAYER_SCALE = 1

# Cargar imágenes
PLAYER_sakura = load_and_scale_image(".\Assets\sakuraStand.png")
PLAYER_rightMov = [pygame.image.load(f".\Assets\secuenciaSakura{i}.png") for i in range(0, 4)]
PLAYER_leftMov = [pygame.image.load(f".\Assets\secuenciaSakuraLeft{i}.png") for i in range(0, 4)]
PLAYER_upMov = [pygame.image.load(f".\Assets\secuenciaSakuraUp{i}.png") for i in range(0, 4)]
PLAYER_downMov = [pygame.image.load(f".\Assets\secuenciaSakuraDown{i}.png") for i in range(0, 4)]
PLAYER_rightAttack = [pygame.image.load(f".\Assets\SakuraInvocation{i}.png") for i in range(0, 10)]
PLAYER_leftAttack = [pygame.image.load(f".\Assets\SakuraInvocationLeft{i}.png") for i in range(0, 10)]

# Escalar tamaño
scaled_player = pygame.transform.scale(
    PLAYER_sakura,
    (int(PLAYER_sakura.get_width() * PLAYER_SCALE),
     int(PLAYER_sakura.get_height() * PLAYER_SCALE))
)

# NPC -> ERIOL & YUE --------------------------------------------------------------------------------------------------------------------------------
# Contador de pasos, dirección y variables de los NPC
NPC_steps = [0, 0]
NPC_directions = ['right', 'right']
NPC_SPEED = 5
NPC_SCALE = 1
NPC_MAX_SPEED = 3

# Variables de l personaje 1 -> Eriol
NPC_ERIOL_DETECTION_RADIUS = 100
NPC_ERIOL_ARRIVAL_RADIUS = 300
ERIOL_MIN_X = 0
ERIOL_MAX_X = 3000

# Imagenes del personaje 1 -> Eriol
NPC_eriol = pygame.image.load(".\Assets\Eriol.png")
NPC_rightMovEriol = [pygame.image.load(f".\Assets\SecuenciaEriol{i}.png") for i in range(1, 6)]
NPC_leftMovEriol = [pygame.image.load(f".\Assets\SecuenciaEriolLeft{i}.png") for i in range(1, 6)]
NPC_rightAttackEriol = [pygame.image.load(f".\Assets\EriolAttack{i}.png") for i in range(0, 2)]
NPC_leftAttackEriol = [pygame.image.load(f".\Assets\EriolAttackLeft{i}.png") for i in range(0, 2)]

# Escalar tamaño del NPC
scaled_eriol = pygame.transform.scale(
    NPC_eriol,
    (int(NPC_eriol.get_width() * NPC_SCALE),
     int(NPC_eriol.get_height() * NPC_SCALE))
)

# Variables de las acciones
NPC_YUE_DETECTION_RADIUS = 100
NPC_YUE_FLEE_SPEED = 4
NPC_YUE_MIN_X = 150
NPC_YUE_MAX_X = 900

# Imagenes del personaje 2 -> Yue
NPC_yue = pygame.image.load(".\Assets\YueStanding.png")
NPC_rightMovYue = [pygame.image.load(f".\Assets\SecuenciaYue{i}.png") for i in range(0, 4)]
NPC_leftMovYue = [pygame.image.load(f".\Assets\SecuenciaYueLeft{i}.png") for i in range(0, 4)]

# Escalar tamaño del NPC
scaled_yue = pygame.transform.scale(
    NPC_yue,
    (int(NPC_yue.get_width() * NPC_SCALE),
     int(NPC_yue.get_height() * NPC_SCALE))
)

# Posiciones de los NPC
NPC_positions = [
    {"x": 800, "y": 800, "sprite": scaled_eriol, "sprites_right": NPC_rightMovEriol, "sprites_left": NPC_leftMovEriol, "is_attacking": False},
    {"x": 600, "y": 500, "sprite": scaled_yue, "sprites_right": NPC_rightMovYue, "sprites_left": NPC_leftMovYue, "is_attacking": False}
]

# OBSTACLE--------------------------------------------------------------------------------------------------------------------------------
# Variables de los obstáculos
OBS_SCALE = 0.5
OBS_DETECTION_RADIUS = 80
OBS_EXPLOSION_SPEED = 0.2

# Imagenes de los obstáculos
obstacle = pygame.image.load(".\Assets\Trampa.png")
obstacle_explosion = [pygame.image.load(f".\Assets\Trampa{i}.png") for i in range(1, 8)]

# Posiciones de los obstáculos
obstacle_positions = [
    {"x": 900, "y": 1200},  
    {"x": 1650, "y": 600},  
    {"x": 1075, "y": 450},  
    {"x": 500, "y": 200},
    {"x": 200, "y": 200},
    {"x": 200, "y": 800},
    {"x": 1500, "y": 800}, 
]

# Escalar tamaño
scaled_obstacle = pygame.transform.scale(
    obstacle,
    (int(obstacle.get_width() * OBS_SCALE),
     int(obstacle.get_height() * OBS_SCALE))
)

# Estados
obstacle_states = [{"exploding": False, "frame": 0} for _ in obstacle_positions]

# PATHFINDING-------------------------------------------------------------------------------------------------------------------------
# Variables para Pathfinding
current_path = None
target_exp = None
current_sprite = PLAYER_sakura

# FUNCIONES---------------------------------------------------------------------------------------------------------------------------
# Función para decidir el comportamiento de Eriol
def test_player_in_range_and_zone(NPC_pos, player_pos):
    dx = player_pos[0] - NPC_pos[0]
    dy = player_pos[1] - NPC_pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    
    # Detectamos si el jugador está dentro del radio de detección
    in_range = distance <= NPC_ERIOL_DETECTION_RADIUS
    
    # Se expande el área cuando se persigue al jugador
    if in_range:
        in_zone = ERIOL_MIN_X - 100 <= NPC_pos[0] <= ERIOL_MAX_X + 100
    else:
        in_zone = ERIOL_MIN_X <= NPC_pos[0] <= ERIOL_MAX_X
    
    return in_range and in_zone

def reset_experiment1():
    NPC_positions[0]["x"] = 1000
    NPC_positions[0]["y"] = 680
    global exp1_pathfinding, pastel_visible
    exp1_pathfinding = False
    pastel_visible = False

def reset_experiment2():
    global exp2_pathfinding, taza_visible
    exp2_pathfinding = False 
    taza_visible = False

# BUCLE DE JUEGO---------------------------------------------------------------------------------------------------------------------
while True:
    # FPS
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    new_x = PLAYER_x
    new_y = PLAYER_y
    
    # CONTROLES---------------------------------------------------------------------------------------------------------------------
    if keys[pygame.K_LEFT]:
        new_x -= PLAYER_MOVEMENT_SPEED
        PLAYER_direction = 'left'
        PLAYER_steps += PLAYER_animation_speed
        if PLAYER_steps >= len(PLAYER_leftMov):
            PLAYER_steps = 0
        current_sprite = PLAYER_leftMov[int(PLAYER_steps)]

    elif keys[pygame.K_RIGHT]:
        new_x += PLAYER_MOVEMENT_SPEED
        PLAYER_direction = 'right'
        PLAYER_steps += PLAYER_animation_speed
        if PLAYER_steps >= len(PLAYER_rightMov):
            PLAYER_steps = 0
        current_sprite = PLAYER_rightMov[int(PLAYER_steps)]
    
    elif keys[pygame.K_UP]:
        new_y -= PLAYER_MOVEMENT_SPEED
        PLAYER_steps += PLAYER_animation_speed
        if PLAYER_steps >= len(PLAYER_upMov):
            PLAYER_steps = 0
        current_sprite = PLAYER_upMov[int(PLAYER_steps)]
    
    elif keys[pygame.K_DOWN]:
        new_y += PLAYER_MOVEMENT_SPEED
        PLAYER_steps += PLAYER_animation_speed
        if PLAYER_steps >= len(PLAYER_downMov):
            PLAYER_steps = 0
        current_sprite = PLAYER_downMov[int(PLAYER_steps)]

    #  Barra espaciadora
    elif keys[pygame.K_SPACE]:
        show_path = True
        current_path, target_exp = encontrar_NPC_cercano(PLAYER_x, PLAYER_y, NPC_positions, tile_graph, tile_size)
        # Si se utilizó path finding
        if current_path:
            next_node = current_path[0].to_node
            target_x = next_node.x * tile_size
            target_y = next_node.y * tile_size
            
            # Se calcula la dirección de movimiento
            dx = target_x - PLAYER_x
            dy = target_y - PLAYER_y
            dist = ((dx**2 + dy**2)**0.5)
            
            if dist > 0:
                dx = dx/dist * PLAYER_MOVEMENT_SPEED  
                dy = dy/dist * PLAYER_MOVEMENT_SPEED
                
                new_x = PLAYER_x + dx
                new_y = PLAYER_y + dy

                if abs(dx) > abs(dy):
                    direccion = 'derecha' if dx > 0 else 'izquierda'
                    current_sprite = PLAYER_rightMov[int(PLAYER_steps)] if dx > 0 else PLAYER_leftMov[int(PLAYER_steps)]
                else:
                    direccion = 'arriba' if dy < 0 else 'abajo'
                    current_sprite = PLAYER_upMov[int(PLAYER_steps)] if dy < 0 else PLAYER_downMov[int(PLAYER_steps)]
            
                PLAYER_steps += PLAYER_animation_speed
                if PLAYER_steps >= len(PLAYER_rightMov):
                    PLAYER_steps = 0
                
                if not check_collision(new_x, new_y, scaled_maze):
                    PLAYER_x = new_x
                    PLAYER_y = new_y
            
            # Se dibuja el path
            draw_path(SCREEN, current_path, camera_x, camera_y, tile_size)
    
    elif keys[pygame.K_s]:
        PLAYER_steps += PLAYER_animation_speed
        if PLAYER_steps >= len(PLAYER_rightAttack):
            PLAYER_steps = 0
        current_sprite = PLAYER_rightAttack[int(PLAYER_steps)] if PLAYER_direction == 'right' else PLAYER_leftAttack[int(PLAYER_steps)]
        scaled_current_sprite = pygame.transform.scale(
            current_sprite,
            (int(current_sprite.get_width() * PLAYER_SCALE),
            int(current_sprite.get_height() * PLAYER_SCALE))
        )
    
    else:
        show_path = False
        current_path = None
        PLAYER_steps = 0
        current_sprite = PLAYER_sakura

    # Se escala la imagen del sprite actual
    scaled_current_sprite = pygame.transform.scale(
        current_sprite,
        (int(current_sprite.get_width() * PLAYER_SCALE),
         int(current_sprite.get_height() * PLAYER_SCALE))
    )

    # Verificar colisiones antes de actualizar la posición 
    if not check_collision(new_x, new_y, scaled_maze):
        PLAYER_x = new_x
        PLAYER_y = new_y
    
    # Limitar al jugador dentro del mundo
    PLAYER_x = max(scaled_player.get_width()//2, min(MAP_WIDTH - scaled_player.get_width()//2, PLAYER_x))
    PLAYER_y = max(scaled_player.get_height()//2, min(MAP_HEIGHT - scaled_player.get_height()//2, PLAYER_y))
    
    # CAMARA---------------------------------------------------------------------------------------------------------------------
    player_screen_x = PLAYER_x - camera_x
    player_screen_y = PLAYER_y - camera_y
    
    if player_screen_x > screen_width - CAMERA_MARGIN:
        camera_x += player_screen_x - (screen_width - CAMERA_MARGIN)
    elif player_screen_x < CAMERA_MARGIN:
        camera_x += player_screen_x - CAMERA_MARGIN
        
    if player_screen_y > screen_height - CAMERA_MARGIN:
        camera_y += player_screen_y - (screen_height - CAMERA_MARGIN)
    elif player_screen_y < CAMERA_MARGIN:
        camera_y += player_screen_y - CAMERA_MARGIN
    
    camera_x = max(0, min(camera_x, MAP_WIDTH - screen_width))
    camera_y = max(0, min(camera_y, MAP_HEIGHT - screen_height))
    
    # ACTUALIZACIONES---------------------------------------------------------------------------------------------------------------------
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(scaled_maze, (-camera_x, -camera_y))
    tile_graph.draw_world_representation(SCREEN, camera_x, camera_y)
    SCREEN.blit(scaled_current_sprite, (PLAYER_x - camera_x - scaled_current_sprite.get_width()//2, PLAYER_y - camera_y - scaled_current_sprite.get_height()//2))
    
    # DECISIONES DE LOS NPC---------------------------------------------------------------------------------------------------------------------
    for i, NPC in enumerate(NPC_positions):
        # Comportamiento de Eriol
        if i == 0:
            kinematic_action = KinematicArriveAction(NPC, (PLAYER_x, PLAYER_y), NPC_MAX_SPEED, NPC_ERIOL_ARRIVAL_RADIUS)
            patrol_action = PatrolAction(NPC, NPC_directions[i])
            # Se determina la decisión
            chase_decision = InRangeDecision(
                (NPC["x"], NPC["y"]),
                (PLAYER_x, PLAYER_y),
                kinematic_action,
                patrol_action,
                test_player_in_range_and_zone
            )
            attack_action = AttackAction(NPC, NPC_directions[i], NPC_rightAttackEriol, NPC_leftAttackEriol)
            attack_decision = PlayerReachedDecision(
                (NPC["x"], NPC["y"]),
                (PLAYER_x, PLAYER_y),
                attack_action,
                chase_decision,
                NPC_ERIOL_ARRIVAL_RADIUS
            )
            action = attack_decision.make_decision()

            # Si el jugador está cerca, Eriol ataca
            if action == "attack":
                NPC["is_attacking"] = True
                NPC_steps[i] += 0.2
                attack_sprites = NPC_rightAttackEriol if NPC_directions[i] == 'right' else NPC_leftAttackEriol
                if NPC_steps[i] >= len(attack_sprites):
                    NPC_steps[i] = 0
                    NPC["is_attacking"] = False
                current_frame = int(NPC_steps[i])
                if current_frame >= len(attack_sprites):
                    current_frame = len(attack_sprites) - 1
                NPC["sprite"] = pygame.transform.scale(
                    attack_sprites[current_frame],
                    (int(attack_sprites[current_frame].get_width() * NPC_SCALE),
                    int(attack_sprites[current_frame].get_height() * NPC_SCALE))
                )
            # Si esta cerca, Eriol persigue al jugador
            elif isinstance(action, KinematicArrive):
                NPC["is_attacking"] = False
                steering = action.getSteering()
                if steering:
                    new_x = NPC["x"] + steering.velocity.x
                    NPC["x"] = new_x
                    NPC_directions[i] = 'right' if steering.velocity.x > 0 else 'left'
                    
            # Si no, Eriol patrulla
            elif action == "patrol":
                NPC["is_attacking"] = False
                if NPC_directions[i] == 'right':
                    new_x = NPC["x"] + NPC_SPEED
                else:
                    new_x = NPC["x"] - NPC_SPEED
                if check_collision(new_x, NPC["y"], scaled_maze):
                    NPC_directions[i] = 'left' if NPC_directions[i] == 'right' else 'right'
                else:
                    NPC["x"] = new_x

        # Comportamiento de Yue
        else:
            kinematic_flee = KinematicFleeAction(
                NPC,
                (PLAYER_x, PLAYER_y),
                NPC_YUE_FLEE_SPEED,
                NPC_YUE_DETECTION_RADIUS,
                MAP_WIDTH,
                MAP_HEIGHT,
                NPC_YUE_MIN_X,
                NPC_YUE_MAX_X
            )
            patrol_action = PatrolAction(NPC, NPC_directions[i])
            flee_decision = InRangeDecision(
                (NPC["x"], NPC["y"]),
                (PLAYER_x, PLAYER_y),
                kinematic_flee,
                patrol_action,
                lambda pos1, pos2: (
                    math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2) <= NPC_YUE_DETECTION_RADIUS
                    and NPC_YUE_MIN_X <= pos1[0] <= NPC_YUE_MAX_X
                )
            )
            action = flee_decision.make_decision()

            # Si el jugador está cerca, Yue huye
            if isinstance(action, KinematicFlee):
                steering = action.getSteering()
                if steering:
                    new_x = NPC["x"] + steering.velocity.x
                    if NPC_YUE_MIN_X <= new_x <= NPC_YUE_MAX_X:
                        NPC["x"] = new_x
                    NPC_directions[i] = 'right' if steering.velocity.x > 0 else 'left'

            # Si no, Yue patrulla
            else:
                if NPC_directions[i] == 'right':
                    new_x = NPC["x"] + NPC_SPEED
                    if new_x > NPC_YUE_MAX_X:
                        NPC_directions[i] = 'left'
                else:
                    new_x = NPC["x"] - NPC_SPEED
                    if new_x < NPC_YUE_MIN_X:
                        NPC_directions[i] = 'right'
                if check_collision(new_x, NPC["y"], scaled_maze):
                    NPC_directions[i] = 'left' if NPC_directions[i] == 'right' else 'right'
                else:
                    NPC["x"] = new_x
                
        # ANIMACIONES---------------------------------------------------------------------------------------------------------------------
        if not NPC["is_attacking"]:
            NPC_steps[i] += 0.2
            if NPC_directions[i] == 'right':
                sprites = NPC["sprites_right"]
            else:
                sprites = NPC["sprites_left"]
            
            if NPC_steps[i] >= len(sprites):
                NPC_steps[i] = 0
            
            current_frame = int(NPC_steps[i])
            NPC["sprite"] = pygame.transform.scale(
                sprites[current_frame],
                (int(sprites[current_frame].get_width() * NPC_SCALE),
                int(sprites[current_frame].get_height() * NPC_SCALE))
            )
    
    # ANIMACION DE LOS OBSTACULOS---------------------------------------------------------------------------------------------------------------------
    for i, obstacle in enumerate(obstacle_positions):
        if not obstacle_states[i]["exploding"]:
            # Calculamos la distancia entre el obstaculo y el jugador
            dx = PLAYER_x - obstacle["x"]
            dy = PLAYER_y - obstacle["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= OBS_DETECTION_RADIUS:
                obstacle_states[i]["exploding"] = True
                
        if obstacle_states[i]["exploding"]:
            obstacle_states[i]["frame"] += OBS_EXPLOSION_SPEED
            if obstacle_states[i]["frame"] >= len(obstacle_explosion):
                # Eliminamos el obstaculo si llega al último sprite
                obstacle_positions[i] = None
                continue
                
            current_frame = int(obstacle_states[i]["frame"])
            if current_frame < len(obstacle_explosion):
                scaled_explosion = pygame.transform.scale(
                    obstacle_explosion[current_frame],
                    (int(obstacle_explosion[current_frame].get_width() * OBS_SCALE),
                    int(obstacle_explosion[current_frame].get_height() * OBS_SCALE))
                )
                SCREEN.blit(scaled_explosion,
                            (obstacle["x"] - camera_x - scaled_explosion.get_width()//2,
                            obstacle["y"] - camera_y - scaled_explosion.get_height()//2))
        else:
            SCREEN.blit(scaled_obstacle,
                        (obstacle["x"] - camera_x - scaled_obstacle.get_width()//2,
                        obstacle["y"] - camera_y - scaled_obstacle.get_height()//2))
    # DIBUJAR NPC Y OBSTACULOS---------------------------------------------------------------------------------------------------------------------
    for NPC in NPC_positions:
        SCREEN.blit(NPC["sprite"], 
                     (NPC["x"] - camera_x - NPC["sprite"].get_width()//2,
                      NPC["y"] - camera_y - NPC["sprite"].get_height()//2))

    for obstacle in obstacle_positions:
        if obstacle:
            SCREEN.blit(scaled_obstacle,
                        (obstacle["x"] - camera_x - scaled_obstacle.get_width()//2,
                        obstacle["y"] - camera_y - scaled_obstacle.get_height()//2))
    
    # Si se ejecutó el path finding se dibuja la línea:
    if current_path and show_path:
        draw_path(SCREEN, current_path, camera_x, camera_y, tile_size)
    
    pygame.display.flip()
