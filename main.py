import pygame
import sys
from os.path import normcase
from player import Player
from platform_1 import Platform

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constants
WIDTH = 1280
HEIGHT = 748
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLATFORM_WIDTH = 400
PLATFORM_HEIGHT = 20
WHITE = (255, 255, 255)
PINK = (255, 192, 203)  # Pink color
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FONT_SIZE = 36
BACKGROUND = pygame.image.load(normcase("assets/background_enhanced.jpg"))
lives = 5  # Number of lives for each player
winner_text = ""
FPS = 60
PLATFORM_COLOR = (215, 113, 101)

# bullets
MAX_BULLETS = 5
BULLET_VEL = 20
player1_bullets = []
player2_bullets = []
player1_ammo = MAX_BULLETS
player2_ammo = MAX_BULLETS

# bullet sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(normcase("assets/086553_bullet-hit-39853.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(normcase("assets/desert-eagle-gunshot-14622.mp3"))
RELOAD_SOUND = pygame.mixer.Sound(normcase("assets/revolvercock1-6924.mp3"))
NO_AMMO_SOUND = pygame.mixer.Sound(normcase("assets/empty-gun-shot-6209.mp3"))

# background music
main_game_music = pygame.mixer.Sound(normcase('assets/wii-shop-channel-background-music-hd.mp3'))
main_menu_music = pygame.mixer.Sound(normcase('assets/gaming-background-music-hd.mp3'))

PLAYER_1_HIT = pygame.USEREVENT + 1
PLAYER_2_HIT = pygame.USEREVENT + 2

font = pygame.font.SysFont(None, FONT_SIZE)
title_font = pygame.font.SysFont(None, FONT_SIZE * 2)
# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ULTIMATE SPINJITSU MASTER")

# Create players
player1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'dash': pygame.K_LSHIFT}
player2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'dash': pygame.K_RSHIFT}
player1 = Player(50, HEIGHT - PLAYER_HEIGHT, player1_controls, pygame.image.load("assets/red_player.jpg"), PLAYER_WIDTH, PLAYER_HEIGHT)
player2 = Player(WIDTH - PLAYER_WIDTH - 50, HEIGHT - PLAYER_HEIGHT, player2_controls, pygame.image.load("assets/green_player.jpg"), PLAYER_WIDTH, PLAYER_HEIGHT)
player1.opponent = player2
player2.opponent = player1
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# Create platforms
platforms = pygame.sprite.Group()
platforms.add(Platform(PLATFORM_COLOR, 0, HEIGHT - 10, WIDTH, 10))  # Ground platform
platforms.add(Platform(PLATFORM_COLOR, 20, HEIGHT - 372, 325, 10))  
platforms.add(Platform(PLATFORM_COLOR, 500, HEIGHT - 250, 350, 10)) # right reload box is on this  
platforms.add(Platform(PLATFORM_COLOR, 425, HEIGHT - 500, 325, 10))  
platforms.add(Platform(PLATFORM_COLOR, WIDTH - 385, HEIGHT - 415, 280, 10))  
platforms.add(Platform(PLATFORM_COLOR, WIDTH - 340, HEIGHT - 140, 200, 10))  
platforms.add(Platform(PLATFORM_COLOR, 120, HEIGHT - 90, 240, 10))  #  left reload box is on this
all_sprites.add(platforms)

# Create Dummies
MAIN_DUMMY_IMG = pygame.transform.scale(pygame.image.load("assets/reload_box.png"), (53, 40)) 
SECONDARY_DUMMY_IMG = pygame.transform.scale(pygame.image.load("assets/empty_box.png"), (53, 40)) 
left_dummy = MAIN_DUMMY_IMG
left_dummy_rect = MAIN_DUMMY_IMG.get_rect(bottomleft = (150, HEIGHT - 90))
left_dummy_timer = 301
right_dummy = MAIN_DUMMY_IMG
right_dummy_rect = MAIN_DUMMY_IMG.get_rect(bottomleft = (750, HEIGHT - 250))
right_dummy_timer = 301

clock = pygame.time.Clock()
game_active = False

def main_menu():
    main_game_music.stop()
    main_menu_music.play(-1)
    main_menu_music.set_volume(0.25)
    
    global player1_ammo
    global player2_ammo
    global game_active  # Declare game_active as global
    global winner_text
    global left_dummy_timer
    global right_dummy_timer
    while not game_active:  # Loop while game_active is False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player1.lives = 5
                player2.lives = 5
                player1_ammo = MAX_BULLETS
                player2_ammo = MAX_BULLETS
                player1_bullets.clear()
                player2_bullets.clear()
                left_dummy_timer = 301
                right_dummy_timer = 301
                game_active = True  # Set game_active to True when spacebar is pressed

        screen.fill(PINK)
        title = title_font.render("Ultimate Spinjitsu Master", True, BLACK)
        text = font.render("Press SPACEBAR to start", True, BLACK)
        winner = font.render(winner_text, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        winner_rect = winner.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(title, title_rect)
        screen.blit(text, text_rect)
        screen.blit(winner, winner_rect)

        pygame.display.update()
        clock.tick(30)

def handle_bullets():
    for bullet in player1_bullets:
        pygame.draw.rect(screen, 'red', bullet)
        if player2.rect.center > player1.rect.center:
            bullet.x += BULLET_VEL
        else:
            bullet.x -= BULLET_VEL
        if bullet.colliderect(player2.rect):
            player1_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(PLAYER_2_HIT))
        elif bullet.x > WIDTH or bullet.x < 0:
            player1_bullets.remove(bullet)
        

    for bullet in player2_bullets:
        pygame.draw.rect(screen, 'green', bullet)
        if player1.rect.center < player2.rect.center:
            bullet.x -= BULLET_VEL
        else:
            bullet.x += BULLET_VEL
        if bullet.colliderect(player1.rect):
            player2_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(PLAYER_1_HIT))
        elif bullet.x < 0 or bullet.x > WIDTH:
            player2_bullets.remove(bullet)

# Main game loop
def main():
    main_menu_music.stop()
    main_game_music.play(-1)
    main_game_music.set_volume(0.25)
    # Reset player positions
    global player1_ammo
    global player2_ammo
    global left_dummy_timer
    global right_dummy_timer
    global left_dummy
    global right_dummy
    global FPS
    global game_active  # Declare game_active as global
    
    player1.rect.x = 50
    player1.rect.y = HEIGHT - PLAYER_HEIGHT
    player2.rect.x = WIDTH - PLAYER_WIDTH - 50
    
    player2.rect.y = HEIGHT - PLAYER_HEIGHT
    
    running = True
    while game_active:  # Loop while game_active is True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(player1_bullets) < MAX_BULLETS and player1_ammo > 0:
                    bullet = pygame.Rect(player1.rect.center[0], player1.rect.center[1], 10, 10)
                    player1_bullets.append(bullet)  
                    player1_ammo -= 1
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_LCTRL and player1_ammo == 0:
                    NO_AMMO_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and player2_ammo == 0:
                    NO_AMMO_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(player2_bullets) < MAX_BULLETS and player2_ammo > 0:
                    bullet = pygame.Rect(player2.rect.center[0], player2.rect.center[1], 10, 10)
                    player2_bullets.append(bullet)
                    player2_ammo -= 1
                    BULLET_FIRE_SOUND.play()
            
            
            if event.type == PLAYER_2_HIT:
                player2.lives -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == PLAYER_1_HIT:
                player1.lives -= 1
                BULLET_HIT_SOUND.play()
        
        FPS = 60
        for bullet in player1_bullets:
            if bullet.colliderect(player2.slow_motion_zone):
                FPS = 20
        
        for bullet in player2_bullets:
            if bullet.colliderect(player1.slow_motion_zone):
                FPS = 20
        
        # ammo box reload
        left_dummy_timer += 1
        right_dummy_timer += 1
        if player1_ammo < MAX_BULLETS and player1.rect.colliderect(left_dummy_rect) and left_dummy_timer > 300:
            player1_ammo = MAX_BULLETS
            left_dummy = SECONDARY_DUMMY_IMG
            RELOAD_SOUND.play()
            left_dummy_timer = 0
        elif player1_ammo < MAX_BULLETS and player1.rect.colliderect(right_dummy_rect) and right_dummy_timer > 300:
            player1_ammo = MAX_BULLETS
            right_dummy = SECONDARY_DUMMY_IMG
            right_dummy_timer = 0
            RELOAD_SOUND.play()
            
        if player2_ammo < MAX_BULLETS and player2.rect.colliderect(left_dummy_rect) and left_dummy_timer > 300:
            player2_ammo = MAX_BULLETS
            left_dummy = SECONDARY_DUMMY_IMG
            left_dummy_timer = 0
            RELOAD_SOUND.play()
        elif player2_ammo < MAX_BULLETS and player2.rect.colliderect(right_dummy_rect) and right_dummy_timer > 300:
            player2_ammo = MAX_BULLETS
            right_dummy = SECONDARY_DUMMY_IMG
            right_dummy_timer = 0
            RELOAD_SOUND.play()
        
        if left_dummy_timer > 300 and not (player1.rect.colliderect(left_dummy_rect) or player2.rect.colliderect(left_dummy_rect)):
            left_dummy = MAIN_DUMMY_IMG
        if right_dummy_timer > 300 and not (player1.rect.colliderect(right_dummy_rect) or player2.rect.colliderect(right_dummy_rect)):
            right_dummy = MAIN_DUMMY_IMG
        
        global winner_text
        if player1.lives <= 0:
            game_active = False
            winner_text = "green ninja won!"
        elif player2.lives <= 0:
            game_active = False
            winner_text = "red ninja won!"
        
        # Update
        all_sprites.update(platforms, WIDTH, HEIGHT)

        # Draw
        # screen.fill(WHITE)
        screen.blit(pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT)), (0, 0))
        screen.blit(left_dummy, left_dummy_rect)
        screen.blit(right_dummy, right_dummy_rect)
        
        player1_hp_text = font.render(f"Health: {player1.lives}", True, BLACK)
        player1_hp_text_rect = player1_hp_text.get_rect(topleft = (32, 32))
        player1_ammo_text = font.render(f"Ammo: {player1_ammo}", True, BLACK)
        player1_ammo_text_rect = player1_ammo_text.get_rect(topleft = (32, 64))
        
        player2_hp_text = font.render(f"Health: {player2.lives}", True, BLACK)
        player2_hp_text_rect = player2_hp_text.get_rect(topright = (WIDTH - 32, 32))
        player2_ammo_text = font.render(f"Ammo: {player2_ammo}", True, BLACK)
        player2_ammo_text_rect = player2_ammo_text.get_rect(topright = (WIDTH - 32, 64))
        
        screen.blit(player1_hp_text, player1_hp_text_rect)
        screen.blit(player1_ammo_text, player1_ammo_text_rect)
        
        screen.blit(player2_hp_text, player2_hp_text_rect)
        screen.blit(player2_ammo_text, player2_ammo_text_rect)
        
        # for slow motion zone debugging
        # pygame.draw.rect(screen, "red", player1.slow_motion_zone)
        # pygame.draw.rect(screen, "green", player2.slow_motion_zone)
        
        handle_bullets()
        
        all_sprites.draw(screen)
        pygame.display.update()

        # Cap the frame rate
        clock.tick(FPS)

# Main loop
while True:
    main_menu()  # Run main menu loop
    main()       # Run main game loop
