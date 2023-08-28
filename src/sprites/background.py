from pygame.sprite import Sprite
from pygame.image import load as load_image


class Background(Sprite):
    """Classe que representa o background do jogo.

    Background(*groups): return Background

    O background não possui nenhum comportamento especial e nem
    qualquer animação dentro do jogo.
    """

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = load_image('graphics/background.png').convert()
        self.rect = self.image.get_rect(topleft=(0, 0))
