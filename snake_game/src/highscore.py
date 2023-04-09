import pygame
import os
import json


class Highscore:
    def __init__(self, filename='snake_game/records/highscores.json'):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)

    def add_score(self, score):
        scores = self.get_scores()
        scores.append(score)
        scores.sort(reverse=True)
        scores = scores[:10]  # Keep only the top 10 scores

        with open(self.filename, 'w') as file:
            json.dump(scores, file)

    def get_scores(self):
        with open(self.filename, 'r') as file:
            scores = json.load(file)
        return scores

    def show_personal_records(self, screen):
        scores = self.get_scores()
        font = pygame.font.Font(None, 36)
        running = True

        while running:
            screen.fill((0, 0, 0))

            for i, score in enumerate(scores):
                text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 160 + i * 40))
                screen.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_q):
                        running = False


