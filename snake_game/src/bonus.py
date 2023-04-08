import pygame

class Bonus:
    def __init__(self, position, bonus_type = "add_points"):
        self.type = bonus_type
        self.position = position
        self.size = 20  # The size is 1.2 times the snake's head size

    def draw(self, screen):
        # Define colors for different bonus types
        bonus_colors = {
            "speed_up": (0, 255, 0),
            "add_points": (255, 255, 0)
        }

        color = bonus_colors.get(self.type, (0, 0, 0))
        bonus_rect = pygame.Rect(self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, color, bonus_rect)
