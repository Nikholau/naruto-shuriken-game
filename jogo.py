# -*- coding: utf-8 -*-

###############################################################################
#
# Mudanças em relação à versão anterior:
#    - classe GameObject: representa objetos do jogo (inimigos, tiros, jogador)
#    - classe Ship: base para todas as naves do jogo
#    - classe Enemy: presença de inimigos na tela
#
###############################################################################

import os, sys
import getopt

# E importaremos o pygame tambem para esse exemplo
import pygame
from pygame.locals import *

images_dir = os.path.join( "..", "imagens" )

# O random será muito útil para esse jogo, ele ajuda o jogo a perder
# a monotonia
import random as Random


class GameObject( pygame.sprite.Sprite ):
    """
    Esta é a classe básica de todos os objetos do jogo.
    
    Na verdade as caixas de texto e o seu contador de vida não são desta
    classe, mas seria overkill utilizar uma classe pra fazer aquilo e neste
    caso, elas poderiam ser desta classe.

    Para não precisar se preocupar com a renderização, vamos fazer a
    classe de forma que ela seja compatível com o RenderPlain, que já possui
    uma função otimizada para renderização direta sobre a tela. Para isso,
    temos que ter três coisas nesta classe:
    
    1) Ser derivada de Sprite, isto é uma boa coisa, pois a classe Sprite
       cria várias facilidades para o nosso trabalho, como poder ser removida
       dos grupos em que foi colocada, inclusive o de Render, através de
       uma chamada a self.kill()
       
    2) Ter self.image. Uma vez que precisamos carregar uma imagem, isto só
       nos define o nome que daremos a imagem a ser renderizada.
       
    3) Ter self.rect. Esse retângulo conterá o tamanho da imagem e sua posição.
       Nas formas:
           rect = ( ( x, y ), ( width, height ) )
       ou
           rect = ( x, y, width, height )
       e ainda nos fornece algumas facilidades em troca, como o rect.move que
       já desloca a imagem a ser renderizada com apenas um comando.
    """
    def __init__( self, image, position, speed=None ):
        pygame.sprite.Sprite.__init__( self )
        self.image = image
        if isinstance( self.image, str ):
            self.image = os.path.join( images_dir, self.image )
            self.image = pygame.image.load( self.image )

        self.rect  = self.image.get_rect()
        screen     = pygame.display.get_surface()
        self.area  = screen.get_rect()
        
        self.set_pos( position )
        self.set_speed( speed or ( 0, 2 ) )
        self.mask = pygame.mask.from_surface(self.image)
    # __init__()


    
    def update( self, dt ):
        move_speed = ( self.speed[ 0 ] * dt / 16,
                       self.speed[ 1 ] * dt / 16 )
        self.rect  = self.rect.move( move_speed )
        if ( self.rect.left > self.area.right ) or \
               ( self.rect.top > self.area.bottom ) or \
               ( self.rect.right < 0 ):
            self.kill()
        if ( self.rect.bottom < - 40 ):
            self.kill()
    # update()


    
    def get_speed( self ):
        return self.speed
    # get_speed()



    def set_speed( self, speed ):
        self.speed = speed
    # set_speed()

    

    def get_pos( self ):
        return ( self.rect.center[ 0 ],
                 self.rect.bottom )
    # get_pos()
    


    def set_pos( self, pos ):
        self.rect.center = ( pos[ 0 ], pos[ 1 ] )
    # get_pos()



    def get_size( self ):
        return self.image.get_size()
    # get_size()
# GameObject



class Ship( GameObject ):
    def __init__( self, position, lives=0, speed=[ 0, 0 ], image=None ):
        self.acceleration = [ 3, 3 ]
        if not image:
            image = "nave.png"
        GameObject.__init__( self, image, position, speed )
        self.set_lives( lives )
    # __init__()

    

    def get_lives( self ):
        return self.lives
    # get_lives()



    def set_lives( self, lives ):
        self.lives = lives
    # set_lives()
# Ship


class NarutoPlayer(Ship):
    def __init__(self, position):
        super().__init__(position, lives=3, speed=[0, 0], image="Nstanding.png")

        # Sprites para animações
        self.standing = pygame.image.load(os.path.join(images_dir, "Nstanding.png")).convert_alpha()
        self.left_frames = [
            pygame.image.load(os.path.join(images_dir, f"NL{i}.png")).convert_alpha()
            for i in range(1, 5)
        ]
        self.right_frames = [
            pygame.image.load(os.path.join(images_dir, f"NR{i}.png")).convert_alpha()
            for i in range(1, 5)
        ]
        self.dead = pygame.image.load(os.path.join(images_dir, "Nd.png")).convert_alpha()

        self.current_frame = 0
        self.direction = "standing"
        self.speed_x = 5

    def move_left(self):
        if hasattr(self, "morto") and self.morto:
            return
        self.direction = "left"
        self.rect.x -= self.speed_x

    def move_right(self):
        if hasattr(self, "morto") and self.morto:
            return
        self.direction = "right"
        self.rect.x += self.speed_x

    def stop(self):
        if hasattr(self, "morto") and self.morto:
            return
        self.direction = "standing"


    def update(self, dt):
        if hasattr(self, "morto") and self.morto:
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

        # Limitar movimento dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right



class Enemy(Ship):
    def __init__(self, position, lives=0, speed=None, image=None):
        # Carregar os frames de animação da shuriken
        self.frames = [
            pygame.image.load(os.path.join(images_dir, "shuriken.png")).convert_alpha(),
            pygame.image.load(os.path.join(images_dir, "movement-shuriken.png")).convert_alpha(),
        ]
        self.current_frame = 0
        self.frame_delay = 5  # velocidade da animação
        self.frame_counter = 0

        # Define a imagem inicial
        image = self.frames[0]
        super().__init__(position, lives, speed, image)

    def update(self, dt):
        # Chama a lógica de movimentação normal
        super().update(dt)

        # Atualiza animação de rotação
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)






class Background:
    def __init__(self, image="bg.png"):
        if isinstance(image, str):
            image = os.path.join(images_dir, image)
            self.image = pygame.image.load(image).convert()
        else:
            self.image = image

        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()

        # Centraliza a imagem no fundo
        self.rect.center = screen_rect.center


    def __init__(self, image="bg.png"):
        if isinstance(image, str):
            image = os.path.join(images_dir, image)
            self.image = pygame.image.load(image).convert()

        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()
        
        # Redimensiona a imagem para preencher a tela
        self.image = pygame.transform.scale(self.image, screen_rect.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)




    def update(self, dt):
        pass  # Fundo fixo, sem rolagem

    def draw(self, screen):
        screen.blit(self.image, self.rect)
# Background




class Game:
    screen = None
    screen_size = None
    run = True
    list = None
    background = None
    naruto_atingido = False  # Flag para colisão 
    
    def __init__( self, size, fullscreen ):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        actors = {}
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen       = pygame.display.set_mode( size, flags )
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Título da Janela' )
    # init()



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
    # handle_events()



    def actors_update(self, dt):
        self.background.update(dt)
        for key, actor in self.list.items():
            if isinstance(actor, pygame.sprite.Group):
                actor.update(dt)
            else:
                actor.update(dt)

    def actors_draw(self):
        self.background.draw(self.screen)
        for key, actor in self.list.items():
            if isinstance(actor, pygame.sprite.Group):
                actor.draw(self.screen)
            else:
                self.screen.blit(actor.image, actor.rect)




    def manage(self):
        if self.naruto_atingido:
            return  # para de gerar inimigos após colisão

        # código original continua abaixo:
        r = Random.randint(0, 100)
        x = Random.randint(1, self.screen_size[0] // 20)
        if r > (40 * len(self.list["enemies"])):
            enemy = Enemy([0, 0])
            size = enemy.get_size()
            enemy.set_pos([x * size[0], -size[1]])
            self.list["enemies"].add(enemy)
    # manage()


    
    def loop( self ):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background( "bg.png" )

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock         = pygame.time.Clock()
        dt            = 16

        self.list = {
            "enemies": pygame.sprite.RenderPlain(Enemy([120, 0])),
            "player": NarutoPlayer([self.screen_size[0] // 2, self.screen_size[1] - 100]),
        }


        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.actors_update( dt )

            # Faça a manutenção do jogo, como criar inimigos, etc.
            self.manage()

            self.score = 0
            self.font = pygame.font.SysFont(None, 36)

            if not self.naruto_atingido:
            # Verifica colisão entre player e inimigos
                
                colisores = pygame.sprite.spritecollide(
                    self.list["player"], self.list["enemies"], dokill=True, collided=pygame.sprite.collide_mask
                )
                if colisores:
                    self.naruto_atingido = True
                    self.list["player"].morto = True


            
            # Desenhe para o back buffer
            self.actors_draw()
            
            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            print("FPS: %0.2f" % clock.get_fps())
        # while self.run
    # loop()
            

   
# Game


def usage():
    """
    Imprime informações de uso deste programa.
    """
    prog = sys.argv[ 0 ]
    print("Usage:")
    print("\t%s [-f|--fullscreen] [-r <XxY>|--resolution=<XxY>]" % prog)
    print()
# usage()



def parse_opts( argv ):
    """
    Pega as informações da linha de comando e retorna 
    """
    # Analise a linha de commando usando 'getopt'
    try:
        opts, args = getopt.gnu_getopt( argv[ 1 : ],
                                        "hfr:",
                                        [ "help",
                                          "fullscreen",
                                          "resolution=" ] )
    except getopt.GetoptError:
        # imprime informacao e sai
        usage()
        sys.exit( 2 )

    options = {
        "fullscreen":  False,
        "resolution": ( 640, 480 ),
        }

    for o, a in opts:
        if o in ( "-f", "--fullscreen" ):
            options[ "fullscreen" ] = True
        elif o in ( "-h", "--help" ):
            usage()
            sys.exit( 0 )
        elif o in ( "-r", "--resolution" ):
            a = a.lower()
            r = a.split( "x" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( "," )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( ":" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue
    # for o, a in opts
    r = options[ "resolution" ]
    options[ "resolution" ] = [ int( r[ 0 ] ), int( r[ 1 ] ) ]
    return options
# parse_opts()



def main( argv ):
    #primeiro vamos verificar que estamos no diretorio certo para conseguir
    #encontrar as imagens e outros recursos, e inicializar o pygame com as
    #opcoes passadas pela linha de comando
    fullpath = os.path.abspath( argv[ 0 ] )
    dir = os.path.dirname( fullpath )
    os.chdir( dir )

    options = parse_opts( argv )
    game = Game( options[ "resolution" ], options[ "fullscreen" ] )
    game.loop()
# main()
        
# este comando fala para o python chamar o main se estao executando o script
if __name__ == '__main__':
    main( sys.argv )
