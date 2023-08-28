import os
import random

from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.image import load as load_image
from pygame.transform import scale as scale_image
from pygame.transform import rotozoom as rotate_surface
from pygame.mask import from_surface as mask_from_surface


class Asteroid(Sprite):
    """Classe que representa um asteroide como objeto do jogo.

    Asteroid(*groups): return Asteroid

    Um asteroide possui rotação, um ponto de respawn aleatório,
    um tamanho aleatório, uma direção aleatória e uma velocidade
    de rotação aleatória.

    O sprite do asteroide é destruido quando atingido pelo laser, ou é
    descartado após ultrapassar dos limites da tela.
    """

    def __init__(self, *groups):
        super().__init__(*groups)

        __sprite_pos = (
            random.randint(-100, int(os.environ['WINDOW_WIDTH']) + 100),
            random.randint(-150, -50),
        )

        __random_scale_ratio = random.uniform(0.5, 1.5)

        self.scaled_surface = load_image('graphics/meteor.png').convert_alpha()
        self.scaled_surface = scale_image(self.scaled_surface, (
            __random_scale_ratio * self.scaled_surface.get_width(),
            __random_scale_ratio * self.scaled_surface.get_height(),
        ))

        self.image = self.scaled_surface
        self.rect = self.image.get_rect(center=__sprite_pos)
        self.mask = mask_from_surface(self.image)
        self.pos = Vector2(self.rect.topleft)
        self.speed = random.randint(400, 600)
        self.direction = Vector2(random.uniform(-0.5, 0.5), 1)
        self.rotation = 0
        self.rotation_speed = random.randint(20, 50)

    def __rotate(self, dt: int) -> None:
        """Gera a animação de rotação do asteroide.

        Args:
            dt (int): Fator de correção do tempo da animação.
        """
        self.rotation += self.rotation_speed * dt
        self.image = rotate_surface(self.scaled_surface, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = mask_from_surface(self.image)

    def update(self, dt: float) -> None:
        """Faz o update dos estados do asteroide ao interagir dentro
        do jogo.

        Args:
            dt (float): Fator de correção do tempo da animação.
        """
        self.pos += self.direction * round(self.speed * dt)
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        self.__rotate(dt)

        if self.rect.midtop[1] >= int(os.environ['WINDOW_HEIGHT']):
            self.kill()
