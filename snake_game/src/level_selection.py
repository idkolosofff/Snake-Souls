import pygame


class LevelSelection:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.levels = [("1", "Basic"), ("2", "Easy"), ("3", "Good"), ("4", "Better"), ("5", "Medium")]
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, level in enumerate(self.levels):
            number, text = level
            combined_text = f"{number}: {text}"
            level_text = self.font.render(combined_text, True, (255, 255, 255))
            level_rect = level_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60 + i * 40))
            self.screen.blit(level_text, level_rect)

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    return 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    return 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    return 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    return 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    return 5
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return 'escape'

    def run(self):
        while self.running:
            self.draw()
            difficulty = self.handle_input()
            if difficulty:
                return difficulty
