import pygame


class Bonus:
    def __init__(self, position, bonus_type = "add_points"):
        self.type = bonus_type
        self.position = position
        self.size = Bonus.bonus_sizes.get(self.type, 15)  # Default size is 20 if type not in bonus_sizes

    # Dictionary that maps bonus types to their sizes
    bonus_sizes = {
        "speed_up": 15,
        "add_points": 10,
        "slow_down": 5
    }

    def draw(self, screen):
        # Define colors for different bonus types
        bonus_colors = {
            "speed_up": (0, 128, 255), # Blue
            "add_points": (252, 252, 20), # Golden
            "slow_down": (51, 25, 0) # Brown
        }

        color = bonus_colors.get(self.type, (0, 0, 0))
        bonus_rect = pygame.Rect(self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, color, bonus_rect)
