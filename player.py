import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls, player_img, player_width, player_height):
        super().__init__()
        self.player_width = player_width
        self.player_height = player_height
        self.player_img = player_img
        self.image = self.player_img
        self.image = pygame.transform.scale(self.image, (player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.jump_power = -12
        self.dash_cooldown = 0
        self.on_ground = False
        self.controls = controls
        self.opponent = 0
        self.lives = 5  # Number of lives for each player
        self.MAX_BULLETS = 5
        self.BULLET_VEL = 20
        self.bullets = []
        self.slow_motion_zone = pygame.Rect(x, y, player_width * 7, player_height * 7)
        

    def update(self, platforms, screen_width, screen_height):
        keys = pygame.key.get_pressed()
        self.slow_motion_zone.center = self.rect.center
        # Movement
        self.vel_x = 0
        if keys[self.controls['left']]:
            self.vel_x = -5
        if keys[self.controls['right']]:
            self.vel_x = 5

        # Dash
        if keys[self.controls['dash']] and self.dash_cooldown == 0 and keys[self.controls['jump']]:
            self.vel_y = self.jump_power  # dash power for horizontal
            self.dash_cooldown = 60  # Cooldown for a second (60 frames)

        # Jump
        if keys[self.controls['jump']]:
            if self.on_ground:
                self.vel_y = self.jump_power
                self.on_ground = False

        # Apply gravity
        if self.rect.left > 0 or self.rect.right < screen_width:
            self.vel_y += 0.5  # Regular gravity

        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Collision with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    
        
        if self.rect.colliderect(self.opponent.rect):
            if self.vel_y > 0:
                self.rect.bottom = self.opponent.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_x > 0:
                self.rect.left = self.opponent.rect.right
                self.rect.right = self.opponent.rect.left
                self.vel_x = 0
            elif self.vel_x < 0:
                self.rect.right = self.opponent.rect.left
                self.rect.left = self.opponent.rect.right
                self.vel_x = 0
            # elif self.vel_y < 0:
            #     self.rect.top = self.opponent.rect.bottom
            #     self.vel_y = 0
            

        # Prevent from going out of the screen
        self.rect.x = max(0, min(self.rect.x, screen_width - self.player_width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.player_height))

        # Update dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
