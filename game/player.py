import pygame
import os
from game.settings import IMAGES_DIR
from game.objects import Ship
from game.objects import Rasengan


class NarutoPlayer(Ship):
    def __init__(self, position):
        super().__init__(position, lives=3, speed=[0, 0], image="Nstanding.png")

        self.standing = pygame.image.load(os.path.join(IMAGES_DIR, "Nstanding.png")).convert_alpha()
        self.left_frames = [
            pygame.image.load(os.path.join(IMAGES_DIR, f"NL{i}.png")).convert_alpha()
            for i in range(1, 5)
        ]
        self.right_frames = [
            pygame.image.load(os.path.join(IMAGES_DIR, f"NR{i}.png")).convert_alpha()
            for i in range(1, 5)
        ]
        self.dead = pygame.image.load(os.path.join(IMAGES_DIR, "Nd.png")).convert_alpha()

        self.current_frame = 0
        self.direction = "standing"
        self.speed_x = 5
        self.morto = False

    def move_left(self):
        if self.morto:
            return
        self.direction = "left"
        self.rect.x -= self.speed_x

    def move_right(self):
        if self.morto:
            return
        self.direction = "right"
        self.rect.x += self.speed_x

    def stop(self):
        if self.morto:
            return
        self.direction = "standing"

    def shoot_rasengan(self):
        return Rasengan((self.rect.centerx, self.rect.top))

    def update(self, dt):
        if self.morto:
            self.image = self.dead
            return

        self.current_frame += 1
        if self.direction == "left":
            self.image = self.left_frames[self.current_frame % len(self.left_frames)]
        elif self.direction == "right":
            self.image = self.right_frames[self.current_frame % len(self.right_frames)]
        else:
            self.image = self.standing

        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right
