import pygame
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

