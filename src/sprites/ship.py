import os
from typing import Callable

from pygame.sprite import Sprite
from pygame.image import load as load_image
from pygame.mouse import get_pos as get_mouse_pos
from pygame.mouse import get_pressed as get_mouse_pressed
from pygame.mask import from_surface as mask_from_surface


class Ship(Sprite):
    """Classe que representa o elemento controlável do jogo.

    Ship(laser_shoot_action: Callable, *groups): return Ship

    A nave é controlada através do movimento do mouse. O botão
    esquerdo do mouse gera a ação de atirar o laser.

    Quando há uma colisão entre um asteroide e a nave o jogo é
    finalizado.
    """

    def __init__(self, laser_shoot_action: Callable, *groups):
        super().__init__(*groups)

        __sprite_pos = (
            int(os.environ['WINDOW_WIDTH']) / 2,
            int(os.environ['WINDOW_HEIGHT']) / 2
        )

        self.image = load_image('graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=__sprite_pos)
        self.mask = mask_from_surface(self.image)

        self.__laser_shoot_action = laser_shoot_action

    def __mouse_input(self):
        """Atualiza a posição do centro da nave de acordo com a posição
        do mouse.
        """
        self.rect.center = get_mouse_pos()

    def __laser_shoot(self):
        """Executa a ação de atirar o laser se o botão esquerdo do mouse
        for pressionado.
        """
        pressed_right, _, _ = get_mouse_pressed()

        if pressed_right:
            self.__laser_shoot_action()

    def update(self, dt: float) -> None:
        """Faz o update dos estados da nave ao interagir dentro do jogo.

        Args:
            dt (float): Fator de correção do tempo da animação.
        """
        self.__mouse_input()
        self.__laser_shoot()
