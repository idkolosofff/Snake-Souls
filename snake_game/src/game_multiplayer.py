from .snake import Snake
from .bonus import Bonus
from .terrain import Terrain
from .food import Food
from .drawing import draw_game_multiplayer
from .drawing import show_end_screen
from . import config
import pygame
from .game import Game
from .client import Client
from . import drawing

class GameMultiplayer:
    def __init__(self, screen, client, snake_color):
        self.screen = screen
        self.client = client
        self.snake_color = snake_color
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True
        self.game_over = False

        while self.running and not self.game_over:
            self.client.request_game_state()
            game_state = self.client.game_state
            if not self.client.handle_input():
                show_end_screen(self.screen, "Game Over, press any key")
                pygame.time.delay(config.GAME_OVER_DELAY)
                self.running = False
                break
                
            

            if game_state is not None:
                if game_state ==  {'end_reason': 'server_closed'} or game_state ==  {'end_reason': 'game_over'}:
                    show_end_screen(self.screen, "Game Over")
                    pygame.time.delay(config.GAME_OVER_DELAY)
                    self.running = False
                    break
                terrains_data = game_state['terrains']
                snakes_data = game_state['snakes']
                foods_data = game_state['foods']
                bonuses_data = game_state['bonuses']
                points_to_complete = game_state['points_to_complete']
                start_time = game_state['start_time']

                foods = [Food(food_data['position']) for food_data in foods_data]
                bonuses = [Bonus(bonus_data['position'], bonus_data['type']) for bonus_data in bonuses_data]
                terrains = [Terrain(terrain_data['position'], terrains_data['type']) for terrain_data in terrains_data]
                snakes = {client_id: Snake.from_data(snake_data) for client_id, snake_data in snakes_data.items()} 

                draw_game_multiplayer(self.screen, terrains, snakes, foods, bonuses, points_to_complete, start_time, self.client.player_id)
            self.clock.tick(config.CLOCK_TICK)
            pygame.display.flip()

