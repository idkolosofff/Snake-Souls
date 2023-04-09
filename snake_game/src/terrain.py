import pygame


class Terrain:
    def __init__(self, position, terrain_type = "add_points"):
        self.type = terrain_type
        self.position = position
        self.size = Terrain.terrain_sizes.get(self.type, 15)  # Default size is 20 if type not in terrain_sizes

    # Dictionary that maps terrain types to their sizes
    terrain_sizes = {
        "speed_up": 35,
        "wall": 50,
        "slow_down": 25
    }

    def draw(self, screen):
        # Define colors for different terrain types
        terrain_colors = {
            "speed_up": (0, 200, 200), # cyan
            "wall": (255, 255, 255),
            "slow_down": (204, 102, 0) #light_brown
        }

        color = terrain_colors.get(self.type, (0, 0, 0))
        terrain_rect = pygame.Rect(self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, color, terrain_rect)
