import pygame

class Food:
    def __init__(self, position):
        self.position = position
        self.size = 20  # The size is 2 times the snake's head size

    def draw(self, screen):
        food_rect = pygame.Rect(self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, (255, 0, 0), food_rect)
