"""Arquivo que deve ser executado para iniciar o jogo. As variáveis
de ambiente são carregadas por padrão. Caso alguma delas não esteja
presente, o jogo não será executado.
"""

from dotenv import load_dotenv
from src.game import Game

load_dotenv()

game = Game()
game.run()
