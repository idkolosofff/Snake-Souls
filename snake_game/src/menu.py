import pygame
from drawing import draw_menu
import config

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.title_font = pygame.font.Font(None, config.TITLE_FONT)
        self.caption_font = pygame.font.Font(None, config.MENU_FONT)
        self.font = pygame.font.Font(None, config.MENU_FONT)

    def draw(self):
        draw_menu(self.screen, config.MENU_OPTIONS, self.title_font, self.caption_font, self.font)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return 'Quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    return 'Start'
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    return 'Records'
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    return 'Colors'
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4 or event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return 'Quit'

    def run(self):
        while self.running:
            self.draw()
            action = self.handle_input()
            if action:
                return action
