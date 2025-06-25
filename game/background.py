import os
import pygame
from game.settings import IMAGES_DIR

class Background:
    def __init__(self, image_name="bg-1.png"):
        self.set_image(image_name)

    def set_image(self, image_name):
        image_path = os.path.join(IMAGES_DIR, image_name)
        self.image = pygame.image.load(image_path).convert()
        screen = pygame.display.get_surface()
        self.image = pygame.transform.scale(self.image, screen.get_size())
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
