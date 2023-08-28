from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.image import load as load_image
from pygame.mask import from_surface as mask_from_surface


class Laser(Sprite):
    """Classe que representa o laser atirado pela nave.

    Laser(laser_pos: tuple[int, int], *groups): return Laser

    Cada Laser viaja apenas em linha reta. A posição de início é
    definida na hora da instanciação da classe.

    O sprite do laser é destruido ao atingir um asteroide, ou é
    descartado após ultrapassar os limites da tela.
    """

    def __init__(self, laser_pos: tuple[int, int], *groups):
        super().__init__(*groups)

        self.image = load_image('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=laser_pos)
        self.mask = mask_from_surface(self.image)
        self.pos = Vector2(self.rect.topleft)
        self.speed = 600
        self.direction = Vector2(0, -1)

    def update(self, dt: float) -> None:
        """Faz o update dos estados do laser ao interagir dentro do
        jogo.

        Args:
            dt (float): Fator de correção do tempo da animação.
        """
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

        if self.rect.midbottom[1] <= 0:
            self.kill()
