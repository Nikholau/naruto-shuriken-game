import pygame
import os
from game.settings import IMAGES_DIR


class Background:
    def __init__(self, image="bg.png"):
        if isinstance(image, str):
            image = os.path.join(IMAGES_DIR, image)
            self.image = pygame.image.load(image).convert()

        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()

        self.image = pygame.transform.scale(self.image, screen_rect.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
