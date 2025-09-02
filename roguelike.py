# roguelike.py

import pgzrun
import random
import math
from pgzero.actor import Actor
from pgzero.rect import Rect

# ==============================================================================
# --- 1. CONFIGURAÇÕES E CONSTANTES DO JOGO ---
# ==============================================================================

WIDTH = 800
HEIGHT = 600
TITLE = "The Cursed Serpent's"

MAP_WIDTH = 50
MAP_HEIGHT = 38
TILE_SIZE = 16

BORDER_TILE = 1
FLOOR_TILE = 0
TILE_LEGEND = {
    0: 'gram1', 1: 'stone1', 2: 'moss',
    3: 'sand', 4: 'stone2', 5: 'gram2'
}

PLAYER_SPEED = 3
ENEMY_SPEED = 1
ENEMY_CHASE_RADIUS = 150
NUM_ENEMIES = 10
NUM_POTIONS = 5

# ==============================================================================
# --- 2. CLASSES ---
# ==============================================================================

class Animator:
    def __init__(self, animations, speed=10):
        self.animations = animations
        self.animation_speed = speed
        self.timer = 0
        self.current_frame_index = 0
        self.current_animation = None
        self.image_name = ''
        if self.animations:
            first_anim = list(self.animations.keys())[0]
            self.play(first_anim)

    def play(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame_index = 0
            self.timer = 0
            self.image_name = self.animations[self.current_animation][0]

    def update(self):
        if self.current_animation is None: return
        self.timer += 1
        if self.timer >= self.animation_speed:
            self.timer = 0
            animation_list = self.animations[self.current_animation]
            self.current_frame_index = (self.current_frame_index + 1) % len(animation_list)
            self.image_name = animation_list[self.current_frame_index]

    def get_current_image_name(self):
        return self.image_name

class Character:
    def __init__(self, x, y, speed, animations):
        self.animator = Animator(animations)
        self.actor = Actor(self.animator.get_current_image_name(), (x, y))
        self.speed = speed
        self.potion_count = 0

    def draw(self):
        self.actor.draw()

    def update(self):
        self.animator.update()
        self.actor.image = self.animator.get_current_image_name()

    def move(self, dx, dy, grid):
        if dx>0: self.animator.play('walk_right')
        elif dx<0: self.animator.play('walk_left')
        elif dy>0: self.animator.play('walk_down')
        elif dy<0: self.animator.play('walk_up')
        else: self.animator.play('idle')
        next_x = self.actor.x + dx
        next_y = self.actor.y + dy
        grid_col = int(next_x // TILE_SIZE)
        grid_row = int(next_y // TILE_SIZE)
        if 0 <= grid_row < len(grid) and 0 <= grid_col < len(grid[0]):
            if grid[grid_row][grid_col] != BORDER_TILE:
                self.actor.x = next_x
                self.actor.y = next_y

class Enemy(Character):
    def __init__(self, x, y, speed, animations):
        super().__init__(x, y, speed, animations)
        self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.wander_timer = 0
        self.wander_interval = 45

    def _choose_new_direction(self):
        choices = [(1,0), (-1,0), (0,1), (0,-1)]
        opposite = (-self.dir[0], -self.dir[1])
        if opposite in choices and len(choices)>1:
            choices.remove(opposite)
        self.dir = random.choice(choices)

    def _wander(self, grid):
        self.wander_timer += 1
        dx, dy = self.dir
        before = (self.actor.x, self.actor.y)
        self.move(dx*self.speed, dy*self.speed, grid)
        after = (self.actor.x, self.actor.y)
        if after == before:
            self._choose_new_direction()
        else:
            if self.wander_timer >= self.wander_interval:
                self.wander_timer = 0
                if random.random() < 0.5: self._choose_new_direction()

    def update_ai(self, grid, player_actor):
        dx_to_player = player_actor.x - self.actor.x
        dy_to_player = player_actor.y - self.actor.y
        distance_to_player = math.hypot(dx_to_player, dy_to_player)
        if distance_to_player < ENEMY_CHASE_RADIUS:
            dx = self.speed if dx_to_player>0 else (-self.speed if dx_to_player<0 else 0)
            dy = self.speed if dy_to_player>0 else (-self.speed if dy_to_player<0 else 0)
            self.move(dx, dy, grid)
        else:
            self._wander(grid)

# ==============================================================================
# --- 3. FUNÇÕES AUXILIARES ---
# ==============================================================================

def generate_maze(width, height):
    maze = [[BORDER_TILE for _ in range(width)] for _ in range(height)]
    def carve(x, y):
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 3 <= nx < width-3 and 3 <= ny < height-3 and maze[ny][nx]==BORDER_TILE:
                maze[y+dy//2][x+dx//2] = FLOOR_TILE
                maze[ny][nx] = FLOOR_TILE
                carve(nx, ny)
    maze[3][3] = FLOOR_TILE
    carve(3,3)
    return maze

def widen_paths(maze, width, height):
    new_maze = [row[:] for row in maze]
    for y in range(1,height-1):
        for x in range(1,width-1):
            if maze[y][x]==FLOOR_TILE and x+1<width-1:
                new_maze[y][x+1]=FLOOR_TILE
    return new_maze

def reset_game():
    global MAP_GRID, player, enemies, potions, safe_spots
    thin_maze = generate_maze(MAP_WIDTH, MAP_HEIGHT)
    MAP_GRID = widen_paths(thin_maze, MAP_WIDTH, MAP_HEIGHT)
    safe_spots = [(col*TILE_SIZE,row*TILE_SIZE) for row,row_data in enumerate(MAP_GRID) for col,tile_id in enumerate(row_data) if tile_id==FLOOR_TILE]

    player_start_pos = random.choice(safe_spots)
    safe_spots.remove(player_start_pos)
    player = Character(player_start_pos[0], player_start_pos[1], PLAYER_SPEED, PLAYER_ANIMATIONS)

    potions.clear()
    for _ in range(NUM_POTIONS):
        if safe_spots:
            pos = random.choice(safe_spots)
            safe_spots.remove(pos)
            potions.append(Actor('potion_red', pos))

    enemies.clear()
    for _ in range(NUM_ENEMIES):
        if safe_spots:
            pos = random.choice(safe_spots)
            safe_spots.remove(pos)
            enemies.append(Enemy(pos[0], pos[1], ENEMY_SPEED, ENEMY_ANIMATIONS))

# ==============================================================================
# --- 4. INICIALIZAÇÃO ---
# ==============================================================================

game_state = 'menu'
current_music_volume = 1.0

PLAYER_ANIMATIONS = {
    'idle': ['hero_down_0'],
    'walk_down': ['hero_down_0','hero_down_1','hero_down_2'],
    'walk_up': ['hero_up_0','hero_up_1','hero_up_2'],
    'walk_left': ['hero_left_0','hero_left_1','hero_left_2'],
    'walk_right': ['hero_right_0','hero_right_1','hero_right_2']
}
ENEMY_ANIMATIONS = {
    'walk_left': ['enemy_left_0','enemy_left_1','enemy_left_2'],
    'walk_right': ['enemy_right_0','enemy_right_1','enemy_right_2'],
    'walk_down': ['enemy_down_0','enemy_down_1','enemy_down_2'],
    'walk_up': ['enemy_up_0','enemy_up_1','enemy_up_2'],
    'idle': ['enemy_down_0']
}

menu_background = Actor('fundo_menu', pos=(WIDTH/2, HEIGHT/2))
start_button = Actor('play_button', pos=(WIDTH/2, 400))
sound_button = Actor('sound_on', pos=(30,30))
exit_button = Actor('exit_button', pos=(WIDTH-30, HEIGHT-30))
return_button_rect = Rect((WIDTH/2-100, HEIGHT/2+50), (200,50))
play_again_rect = Rect((WIDTH/2-100, HEIGHT/2+100), (200,50))
start_game_rect = Rect((WIDTH/2-100, HEIGHT/2+200),(200,50))  # botão iniciar no instructions

safe_spots=[]
player=None
enemies=[]
potions=[]
MAP_GRID=[]

reset_game()

# ==============================================================================
# --- 5. LOOP PRINCIPAL ---
# ==============================================================================

def draw_menu():
    menu_background.draw()
    start_button.draw()
    sound_button.draw()
    exit_button.draw()

def draw_instructions():
    screen.clear()
    # Fundo escurecido
    screen.fill((30, 30, 30))

    # Título
    screen.draw.text(
        "INSTRUÇÕES", 
        center=(WIDTH/2, HEIGHT/2-150), 
        fontsize=60, 
        color="white", 
        ocolor="black", 
        owidth=2
    )

    # Texto explicativo
    instruction_text = (
    "BEM-VINDO, AVENTUREIRO!\n"
    "SUA MISSÃO MÁGICA: COLETAR TODAS \n"
    "AS POÇÕES ENCANTADAS 🧪\n"
    "MAS CUIDADO! AS COBRAS MALANDRAS 🐍\n"
    " PODEM ROUBAR SUAS POÇÕES.\n"
    "PERCA TODAS, E SUA AVENTURA TERMINA!\n"
    "CLIQUE EM 'COMEÇAR' PARA DESPERTAR A MAGIA!"
    )
    screen.draw.text(
        instruction_text, 
        center=(WIDTH/2, HEIGHT/2), 
        fontsize=35, 
        color="yellow", 
        ocolor="black", 
        owidth=1.5
    )
    # Botão COMEÇAR
    screen.draw.filled_rect(start_game_rect, "red")
    screen.draw.text(
        "COMEÇAR", 
        center=start_game_rect.center, 
        fontsize=40, 
        color="white"
    )

def draw():
    if game_state=='menu':
        draw_menu()
    elif game_state=='instructions':
        draw_instructions()
    elif game_state=='playing':
        screen.clear()
        for row_index,row in enumerate(MAP_GRID):
            for col_index,tile_id in enumerate(row):
                screen.blit(TILE_LEGEND[tile_id],(col_index*TILE_SIZE,row_index*TILE_SIZE))
        player.draw()
        for enemy in enemies: enemy.draw()
        for potion in potions: potion.draw()
        sound_button.draw()
        exit_button.draw()
        screen.draw.text(f"P: {player.potion_count}", topright=(WIDTH-20,20), fontsize=30, color="yellow", ocolor="black", owidth=1.0)
    elif game_state in ['game_over','win']:
        screen.clear()
        for row_index,row in enumerate(MAP_GRID):
            for col_index,tile_id in enumerate(row):
                screen.blit(TILE_LEGEND[tile_id],(col_index*TILE_SIZE,row_index*TILE_SIZE))
        msg="VOCÊ VENCEU!" if game_state=='win' else "FIM DE JOGO"
        screen.draw.text(msg, center=(WIDTH/2,HEIGHT/2), fontsize=60, color="gold" if game_state=='win' else "red", ocolor="black", owidth=1.5)
        screen.draw.filled_rect(return_button_rect, "darkgreen")
        screen.draw.text("Retornar ao Menu", center=return_button_rect.center, fontsize=30, color="white")
        screen.draw.filled_rect(play_again_rect, "orange")
        screen.draw.text("Jogar Novamente", center=play_again_rect.center, fontsize=30, color="white")

def update():
    global game_state
    if game_state != 'playing': return
    dx, dy = 0,0
    if keyboard.left: dx=-player.speed
    elif keyboard.right: dx=player.speed
    elif keyboard.up: dy=-player.speed
    elif keyboard.down: dy=player.speed
    player.move(dx, dy, MAP_GRID)
    player.update()
    for enemy in enemies:
        enemy.update_ai(MAP_GRID, player.actor)
        enemy.update()
    for enemy in enemies[:]:
        if player.actor.colliderect(enemy.actor):
            if player.potion_count>0:
                player.potion_count-=1
                enemies.remove(enemy)
            else:
                game_state='game_over'
    for potion in potions[:]:
        if player.actor.colliderect(potion):
            potions.remove(potion)
            player.potion_count+=1
    if not potions: game_state='win'

def on_mouse_down(pos):
    global game_state, current_music_volume
    if sound_button.collidepoint(pos):
        current_music_volume=0.0 if current_music_volume>0 else 1.0
        sound_button.image='sound_on' if current_music_volume>0 else 'sound_off'
        return
    if exit_button.collidepoint(pos):
        pgzrun.go_quit()
        return
    if game_state=='menu':
        if start_button.collidepoint(pos):
            game_state='instructions'
    elif game_state=='instructions':
        if start_game_rect.collidepoint(pos):
            reset_game()
            game_state='playing'
    elif game_state in ['game_over','win']:
        if return_button_rect.collidepoint(pos):
            game_state='menu'
        elif play_again_rect.collidepoint(pos):
            reset_game()
            game_state='playing'

# ==============================================================================
# --- 6. INICIAR O JOGO ---
# ==============================================================================

# INICIA A MÚSICA DE FUNDO EM LOOP
music.play('snake_sound') # <-- Adicione esta linha
music.set_volume(current_music_volume) # Garante que a música começa com o volume certo

pgzrun.go()
