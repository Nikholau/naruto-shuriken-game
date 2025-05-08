import pygame
import os
from game.settings import IMAGES_DIR
from game.objects import Ship


class Enemy(Ship):
    def __init__(self, position, lives=0, speed=None, image=None):
        self.frames = [
            pygame.image.load(os.path.join(IMAGES_DIR, "shuriken.png")).convert_alpha(),
            pygame.image.load(os.path.join(IMAGES_DIR, "movement-shuriken.png")).convert_alpha(),
        ]
        self.current_frame = 0
        self.frame_delay = 5
        self.frame_counter = 0

        image = self.frames[0]
        super().__init__(position, lives, speed, image)

    def update(self, dt):
        super().update(dt)

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)
