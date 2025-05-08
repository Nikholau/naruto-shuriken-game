import os
import sys
import getopt
import pygame
from pygame.locals import *

from game.background import Background
from game.enemy import Enemy
from game.player import NarutoPlayer

class Game:
    def __init__(self, size, fullscreen):
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("Naruto Shuriken Game")
        
        self.run = True
        self.naruto_hit = False
        self.difficulty_level = 1
        self.difficulty_timer = 0
        self.difficulty_increase_interval = 5000
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.win_shown = False

        self.background = Background("bg.png")
        self.list = {
            "enemies": pygame.sprite.RenderPlain(),
            "player": NarutoPlayer([self.screen_size[0] // 2, self.screen_size[1] - 100]),
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.run = False
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT):
                    self.list["player"].stop()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.list["player"].move_left()
        elif keys[K_RIGHT]:
            self.list["player"].move_right()
        else:
            self.list["player"].stop()

    def manage(self, elapsed_time):
        if self.naruto_hit:
            return

        self.difficulty_timer += elapsed_time
        if self.difficulty_timer >= self.difficulty_increase_interval:
            self.difficulty_level += 1
            self.difficulty_timer = 0
            print(f"Difficulty increased to {self.difficulty_level}")

        import random as Random
        r = Random.randint(0, 100)
        x = Random.randint(1, self.screen_size[0] // 20)
        max_enemies = 5 + self.difficulty_level * 2
        if len(self.list["enemies"]) < max_enemies and r > (40 - self.difficulty_level * 2):
            speed = 2 + self.difficulty_level
            enemy = Enemy([0, 0], speed=[0, speed])
            size = enemy.get_size()
            enemy.set_pos([x * size[0], -size[1]])
            self.list["enemies"].add(enemy)

    def show_text_screen(self, message, color):
        font = pygame.font.SysFont(None, 72)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))

        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    waiting = False
                    self.run = False

    def actors_update(self, dt):
        self.background.update(dt)
        for key, actor in self.list.items():
            if isinstance(actor, pygame.sprite.Group):
                for sprite in actor.sprites():
                    sprite.update(dt)
                    if isinstance(sprite, Enemy) and sprite.rect.top > self.screen_size[1]:
                        self.score += 1
                        sprite.kill()
            else:
                actor.update(dt)

    def actors_draw(self):
        self.background.draw(self.screen)
        for key, actor in self.list.items():
            if isinstance(actor, pygame.sprite.Group):
                actor.draw(self.screen)
            else:
                self.screen.blit(actor.image, actor.rect)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def loop(self):
        clock = pygame.time.Clock()
        dt = 16

        while self.run:
            elapsed = clock.tick(1000 // dt)
            self.handle_events()
            self.actors_update(dt)
            self.manage(elapsed)

            if self.score >= 30 and not self.win_shown:
                self.win_shown = True
                self.actors_draw()
                pygame.display.flip()
                self.show_text_screen("YOU WIN", (0, 255, 0))

            if not self.naruto_hit:
                collisions = pygame.sprite.spritecollide(
                    self.list["player"], self.list["enemies"], dokill=True, collided=pygame.sprite.collide_mask
                )
                if collisions:
                    self.naruto_hit = True
                    self.list["player"].morto = True
                    self.actors_draw()
                    pygame.display.flip()
                    self.show_text_screen("GAME OVER", (255, 0, 0))

            self.actors_draw()
            pygame.display.flip()
            print("FPS: %0.2f" % clock.get_fps())


def usage():
    prog = sys.argv[0]
    print("Usage:")
    print(f"\t{prog} [-f|--fullscreen] [-r <XxY>|--resolution=<XxY>]\n")


def parse_opts(argv):
    try:
        opts, args = getopt.gnu_getopt(argv[1:], "hfr:", ["help", "fullscreen", "resolution="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    options = {
        "fullscreen": False,
        "resolution": (640, 480),
    }

    for o, a in opts:
        if o in ("-f", "--fullscreen"):
            options["fullscreen"] = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-r", "--resolution"):
            a = a.lower()
            for sep in ("x", ",", ":"):
                if sep in a:
                    parts = a.split(sep)
                    if len(parts) == 2:
                        options["resolution"] = (int(parts[0]), int(parts[1]))
                        break
    return options


def main(argv):
    fullpath = os.path.abspath(argv[0])
    dir = os.path.dirname(fullpath)
    os.chdir(dir)

    options = parse_opts(argv)
    game = Game(options["resolution"], options["fullscreen"])
    game.loop()


if __name__ == "__main__":
    main(sys.argv)
