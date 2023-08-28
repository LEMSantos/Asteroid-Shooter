import pygame


class Timer:
    """Classe simples para lidar com os coldowns do jogo

    Timer(duration: int): return Timer

    Elementos que vão utilizar essa classe devem chamar o método
    Timer.update() a cada iteração para que o tempo de especificado
    seja devidamente verificado.
    """

    def __init__(self, duration: int):
        self.__duration = duration
        self.__start_time = 0
        self.active = False

    def activate(self) -> None:
        """Ativa a contagem do timer
        """
        self.active = True
        self.__start_time = pygame.time.get_ticks()

    def deactivate(self) -> None:
        """Desativa a contagem timer
        """
        self.active = False
        self.__start_time = 0

    def update(self) -> None:
        """Verifica se o tempo determinado para a finalização do timer
        já foi atingido. Desativa o timer em caso positivo.
        """
        current_time = pygame.time.get_ticks()

        if (current_time - self.__start_time) >= self.__duration:
            self.deactivate()
