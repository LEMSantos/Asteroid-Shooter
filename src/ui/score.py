import os
from pygame import Surface
from pygame.font import Font
from pygame.draw import rect as draw_rect


class Score:
    """Classe que representa o elemento score da interface.

    Score(): return Score

    O Score controla internamente a pontuação e segue a interface
    da classe pygame.sprite.Group() para permitir que ambas sejam
    intercambiáveis e facilitar o desenho e as atualizações da ui.
    """

    def __init__(self):
        self.__font = Font('graphics/subatomic.ttf', 50)
        self.__score = 0
        self.__score_position = (
            int(os.environ['WINDOW_WIDTH']) / 2,
            int(os.environ['WINDOW_HEIGHT']) - 80
        )

    def draw(self, surface: Surface) -> None:
        """Desenha o score na tela, com um texto padrão e uma borda
        branca.

        Args:
            surface (Surface): superfície em que o score será desenhado
        """
        score_text = f'Score: {self.__score}'

        text_surface = self.__font.render(score_text, True, 'white')
        text_rect = text_surface.get_rect(midbottom=self.__score_position)

        surface.blit(text_surface, text_rect)
        draw_rect(surface, 'white', text_rect.inflate(30, 30), 4, 5)

    def increment(self, value: int):
        """Incrementa o valor interno do score.

        Args:
            value (int): valor de incremento
        """
        self.__score += value
