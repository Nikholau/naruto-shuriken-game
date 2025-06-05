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
        self.paused = False
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
            "rasengans": pygame.sprite.RenderPlain(),
        }
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.run = False
                elif event.key == K_p:
                    self.paused = not self.paused
                elif event.key == K_r and (self.naruto_hit or self.win_shown):
                    self.__init__(self.screen_size, False)  # Reinicia o jogo
                elif event.key == K_SPACE:
                    rasengan = self.list["player"].shoot_rasengan()
                    if rasengan:
                        self.list["rasengans"].add(rasengan)

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT):
                    self.list["player"].stop()

        # Movimento contínuo baseado em tecla pressionada
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.list["player"].move_left()
        elif keys[K_RIGHT]:
            self.list["player"].move_right()
        else:
            self.list["player"].stop()

    
    def show_start_screen(self):
        selected_difficulty = 1
        font = pygame.font.SysFont(None, 36)
        big_font = pygame.font.SysFont(None, 64)

        while True:
            self.screen.fill((0, 0, 0))
            
            title = big_font.render("Naruto Shuriken Game", True, (255, 255, 0))
            self.screen.blit(title, (self.screen_size[0] // 2 - title.get_width() // 2, 50))

            instructions = [
                "Setas ← → para mover",
                "Espaço para lançar Rasengan",
                "P para pausar | ESC para sair",
                "",
                "Escolha a dificuldade: 1 (Fácil), 2 (Média), 3 (Difícil)",
                f"Selecionado: {selected_difficulty}",
                "",
                "Pressione ENTER para começar"
            ]

            for i, line in enumerate(instructions):
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (self.screen_size[0] // 2 - text.get_width() // 2, 150 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.run = False
                        return
                    elif event.key == K_1:
                        selected_difficulty = 1
                    elif event.key == K_2:
                        selected_difficulty = 2
                    elif event.key == K_3:
                        selected_difficulty = 3
                    elif event.key == K_RETURN:
                        self.difficulty_level = selected_difficulty
                        return
        



    def reset_game(self):
        self.run = True
        self.paused = False
        self.naruto_hit = False
        self.difficulty_level = 1
        self.difficulty_timer = 0
        self.score = 0
        self.win_shown = False
        self.list = {
            "enemies": pygame.sprite.RenderPlain(),
            "player": NarutoPlayer([self.screen_size[0] // 2, self.screen_size[1] - 100]),
            "rasengans": pygame.sprite.RenderPlain(),
            }


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

        sub_font = pygame.font.SysFont(None, 36)
        sub_text = sub_font.render("Pressione R para reiniciar ou ESC para sair", True, (200, 200, 200))
        sub_rect = sub_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + 60))
        self.screen.blit(sub_text, sub_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    return False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.run = False
                        return False
                    elif event.key == K_r:
                        return True


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

        if "rasengans" in self.list:
            self.list["rasengans"].update(dt)
            for rasengan in self.list["rasengans"]:
                hits = pygame.sprite.spritecollide(rasengan, self.list["enemies"], dokill=False, collided=pygame.sprite.collide_mask)
                for enemy in hits:
                    enemy.kill()
                    self.score += 1
                    rasengan.kill()


    def actors_draw(self):
        self.background.draw(self.screen)
        for key, actor in self.list.items():
            if isinstance(actor, pygame.sprite.Group):
                actor.draw(self.screen)
            else:
                self.screen.blit(actor.image, actor.rect)

        if "rasengans" in self.list:
            self.list["rasengans"].draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_pause_text(self):
        pause_font = pygame.font.SysFont(None, 72)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
        text_rect = pause_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(pause_text, text_rect)

    def loop(self):
        self.show_start_screen()
        clock = pygame.time.Clock()
        dt = 16

        while self.run:
            elapsed = clock.tick(1000 // dt)
            self.handle_events()

            if not self.paused:
                self.actors_update(dt)
                self.manage(elapsed)

                if self.score >= 30 and not self.win_shown:
                    self.win_shown = True
                    self.actors_draw()
                    pygame.display.flip()
                    if self.show_text_screen("YOU WIN", (0, 255, 0)):
                        self.reset_game()


                if not self.naruto_hit:
                    collisions = pygame.sprite.spritecollide(
                        self.list["player"], self.list["enemies"], dokill=True, collided=pygame.sprite.collide_mask
                    )
                    if collisions:
                        self.naruto_hit = True
                        self.list["player"].morto = True
                        self.actors_draw()
                        pygame.display.flip()
                        if self.show_text_screen("GAME OVER", (255, 0, 0)):
                            self.reset_game()

            else:
                self.show_pause_text()

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
