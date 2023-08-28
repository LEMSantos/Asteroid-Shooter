import os
import sys

import pygame

from src.core.timer import Timer
from src.sprites.ship import Ship
from src.sprites.laser import Laser
from src.sprites.asteroid import Asteroid
from src.sprites.background import Background
from src.ui.score import Score


class Game:
    """Classe que representa o jogo inteiro, e organiza os elementos
    de forma que façam sentido para o player.

    Game(): return Game

    O jogo roda a partir da execução da função Game.run()
    """

    def __init__(self):
        __dimensions = (
            int(os.environ['WINDOW_WIDTH']),
            int(os.environ['WINDOW_HEIGHT']),
        )

        pygame.init()
        pygame.display.set_mode(__dimensions)
        pygame.display.set_caption(os.environ['GAME_TITLE'])

        self.__clock = pygame.time.Clock()
        self.__display_surface = pygame.display.get_surface()

        self.__groups = self.__init_groups()
        self.__sprites = self.__init_default_sprites(self.__groups)
        self.__timers = self.__init_timers()
        self.__sounds = self.__init_sounds()

        self.__asteroid_timer = pygame.event.custom_type()

        pygame.time.set_timer(
            self.__asteroid_timer,
            int(os.environ['ASTEROID_RESPAWN_TIME'])
        )

    def __init_groups(self) -> dict[str, Score | pygame.sprite.Group]:
        """Inicializa os grupos utilizados no jogo.

        Returns:
            dict[str, Score | pygame.sprite.Group]: dicionário de
                grupos inicializados.
        """
        return {
            'background_group': pygame.sprite.GroupSingle(),
            'score': Score(),
            'laser_group': pygame.sprite.Group(),
            'asteroid_group': pygame.sprite.Group(),
            'spaceship_group': pygame.sprite.GroupSingle(),
        }

    def __init_default_sprites(
        self,
        groups: dict[str, pygame.sprite.Group],
    ) -> dict[str, pygame.sprite.Sprite]:
        """Inicializa os sprites padrão do jogo.

        Args:
            groups (dict[str, pygame.sprite.Group]): grupos em que os
                sprites serão colocados.

        Returns:
            dict[str, pygame.sprite.Sprite]: dicionário de sprites
                inicializados.
        """
        Background(groups['background_group'])

        return {
            'ship': Ship(self.__laser_shoot_action, groups['spaceship_group']),
        }

    def __init_timers(self) -> dict[str, Timer]:
        """Inicializa os timers do jogo.

        Returns:
            dict[str, Timer]: dicionário com os timers inicializados.
        """
        return {
            'shoot_timer': Timer(500)
        }

    def __init_sounds(self) -> dict[str, pygame.mixer.Sound]:
        """Inicializa os sons do jogo.

        Returns:
            dict[str, pygame.mixer.Sound]: dicionário de sons
                inicializados e com o volume ajustado.
        """
        sounds =  {
            'laser': pygame.mixer.Sound('sounds/laser.ogg'),
            'explosion': pygame.mixer.Sound('sounds/explosion.wav'),
            'music': pygame.mixer.Sound('sounds/music.wav'),
        }

        sounds['laser'].set_volume(0.2)
        sounds['explosion'].set_volume(0.2)
        sounds['music'].set_volume(0.1)

        return sounds

    def __draw_groups(self) -> None:
        """Desenha os sprites de todos os grupos.
        """
        for group in self.__groups.values():
            group.draw(self.__display_surface)

    def __update_groups(self, dt: float) -> None:
        """Atualiza todos os sprites de todos os grupos.

        Args:
            dt (float): Fator de correção do tempo da animação.
        """
        for group in self.__groups.values():
            if hasattr(group, 'update'):
                group.update(dt=dt)

    def __update_timers(self) -> None:
        """Atualiza todos os timers que foram definidos.
        """
        for timer in self.__timers.values():
            timer.update()

    def __laser_shoot_action(self) -> None:
        """Ação que gera um novo laser na tela caso o cooldown tenha
        sido finalizado. O laser gerado aparece no topo da posição
        atual da nave.
        """
        if not self.__timers['shoot_timer'].active:
            Laser(
                self.__sprites['ship'].rect.midtop,
                self.__groups['laser_group'],
            )

            self.__timers['shoot_timer'].activate()
            self.__sounds['laser'].play()

    def __handle_events(self):
        """Lida com os eventos principais gerados no jogo.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.__asteroid_timer:
                Asteroid(self.__groups['asteroid_group'])

    def __handle_collisions(self) -> None:
        """Lida com as possíveis colisões geradas entre os elementos
        presentes no jogo.
        """
        if pygame.sprite.groupcollide(self.__groups['spaceship_group'],
                                      self.__groups['asteroid_group'],
                                      False,
                                      False,
                                      pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

        collided = pygame.sprite.groupcollide(
            groupa=self.__groups['laser_group'],
            groupb=self.__groups['asteroid_group'],
            dokilla=True,
            dokillb=True,
            collided=pygame.sprite.collide_mask
        )

        if collided:
            self.__sounds['explosion'].play()
            self.__groups['score'].increment(len(collided))

    def run(self) -> None:
        """Loop principal do jogo.
        """
        self.__sounds['music'].play(-1)

        while True:
            self.__handle_events()

            dt = self.__clock.tick() / 1000

            self.__handle_collisions()

            self.__draw_groups()

            self.__update_timers()
            self.__update_groups(dt)


            pygame.display.update()
