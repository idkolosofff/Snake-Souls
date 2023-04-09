import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.options = [("1", "Start New Game"), ("2", "Show Personal Records"), ("3", "Quit")]
        self.title_font = pygame.font.Font(None, 48)
        self.caption_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.title_font.render("Snake Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title, title_rect)

        caption = self.caption_font.render("Press the button", True, (255, 255, 255))
        caption_rect = caption.get_rect(center=(self.screen.get_width() // 2, 160))
        self.screen.blit(caption, caption_rect)

        for i, option in enumerate(self.options):
            number, text = option
            combined_text = f"{number}: {text}"
            option_text = self.font.render(combined_text, True, (255, 255, 255))
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60 + i * 40))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()

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
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3 or event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return 'Quit'

    def run(self):
        while self.running:
            self.draw()
            action = self.handle_input()
            if action:
                return action
