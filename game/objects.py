import pygame
import os
from game.settings import IMAGES_DIR


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, position, speed=None):
        super().__init__()
        self.image = image
        if isinstance(self.image, str):
            self.image = os.path.join(IMAGES_DIR, self.image)
            self.image = pygame.image.load(self.image)

        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.set_pos(position)
        self.set_speed(speed or (0, 2))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
        if self.rect.left > self.area.right or self.rect.top > self.area.bottom or self.rect.right < 0:
            self.kill()
        if self.rect.bottom < -40:
            self.kill()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_pos(self):
        return (self.rect.center[0], self.rect.bottom)

    def set_pos(self, pos):
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.image.get_size()


class Ship(GameObject):
    def __init__(self, position, lives=0, speed=[0, 0], image=None):
        self.acceleration = [3, 3]
        if not image:
            image = "nave.png"
        super().__init__(image, position, speed)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives
