import pygame

class Platform(pygame.sprite.Sprite):
  def __init__(self, color, x, y, platform_width, platform_height):
    super().__init__()
    self.platform_width = platform_width
    self.platform_height = platform_height
    self.image = pygame.Surface((self.platform_width, self.platform_height))
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
