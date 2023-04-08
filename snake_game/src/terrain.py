import pygame

class Terrain:
    def __init__(self, terrain_type, tiles):
        self.type = terrain_type
        self.tiles = tiles

    def draw(self, screen, tile_size):
        # Define colors for different terrain types
        terrain_colors = {
            "slow_down": (150, 150, 150),
            "speed_up": (0, 255, 0)
        }

        color = terrain_colors.get(self.type, (0, 0, 0))

        # Draw terrain tiles
        for tile_position in self.tiles:
            tile_rect = pygame.Rect(tile_position[0] * tile_size, tile_position[1] * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, tile_rect)
