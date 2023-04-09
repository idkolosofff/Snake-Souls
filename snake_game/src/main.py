import os
import sys

import pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.game import Game
from src.highscore import Highscore
from src.level_selection import LevelSelection
from src.menu import Menu


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")

    menu = Menu(screen)
    highscore = Highscore()

    while True:
        action = menu.run()

        if action == "Start":
            level_selection = LevelSelection(screen)
            level = level_selection.run()
            if level == 'escape':
                continue
            elif level:
                game = Game(screen, highscore, level)
                game.run()

        elif action == 'Records':
            highscore.show_personal_records(screen)

        elif action == 'Quit':
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


