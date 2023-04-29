from .snake import Snake
from .bonus import Bonus
from .terrain import Terrain
from .highscore import Highscore
from .food import Food
from .drawing import draw_game
from . import config
import pygame
from .game import Game
from .network import encode_player_input, decode_game_state

class GameMultiplayer:
    def __init__(self, screen, highscore, level, snake_color, server):
        self.screen = screen
        self.highscore = highscore
        self.level = level
        self.snake_color = snake_color
        self.server = server
        self.game_over = False
        self.game = Game(screen, highscore, level, snake_color)
        self.player_number = None

    def run(self):
        # Get the player number from the server
        self.player_number = self.server.receive_player_number()

        while not self.game_over:
            # Handle events and player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    player_input = self.get_player_input(event)
                    self.send_player_input(player_input)

            # Receive game state updates from the server
            game_state = self.server.receive_game_state()
            self.update_game_state(game_state)

            # Render the game
            self.game.render()

            # Check for game over condition
            if self.game.check_game_over():
                self.game_over = True

        # Display game over message and high score
        self.game.display_game_over_message()
        self.game.display_high_score()

    def get_player_input(self, event):
        pass

    def send_player_input(self, player_input):
        pass

    def update_game_state(self, game_state):
        pass
