import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE
import json
import random
import os
from .snake import Snake
from .bonus import Bonus
from .terrain import Terrain
from .highscore import Highscore
from .food import Food

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.width, self.height = screen.get_size()
        self.panel_height = 30
        self.clock = pygame.time.Clock()
        self.foods = []
        self.snake = Snake()
        self.highscore = Highscore()
        self.level_number = 1
        self.points = 0
        self.bonus_spawn_timer = 0
        self.bonus_spawn_interval = 25000  # Time in milliseconds between bonus spawns
        self.load_level(self.level_number)

    def load_level(self, level_number):
        level_file = f"snake_game/levels/level_{level_number}.json"
        with open(level_file, "r") as file:
            level_data = json.load(file)

        # Load snake
        snake_data = level_data["snake"]
        self.snake = Snake(start_pos = snake_data["initial_position"], start_speed = snake_data["initial_speed"])

        # Load points to complete and possible bonus types
        self.points_to_complete = level_data["points_to_complete"]
        self.possible_bonus_types = level_data["possible_bonus_types"]

        # Load terrains
        self.terrains = []
        for terrain_data in level_data["terrains"]:
            terrain = Terrain(terrain_data["type"], terrain_data["tiles"])
            self.terrains.append(terrain)

        # Initialize other game elements
        self.spawn_food()
        self.bonuses = []

    def spawn_food(self):
        x = random.randint(1, self.width - 30)
        y = random.randint(1, self.height - 30)
        food_position = (x, y)

        while self.snake.check_collision(food_position):
            x = random.randint(1, self.width - 30)
            y = random.randint(1, self.height - 30)
            food_position = (x, y)

        food = Food(food_position)
        self.foods.append(food)

    def spawn_bonus(self):
        x = random.randint(1, self.width - 30)
        y = random.randint(1, self.height - 30)
        bonus_position = (x, y)
        #bonus_type = random.choice(self.possible_bonus_types)

        while self.snake.check_collision(bonus_position):
            x = random.randint(1, self.width - 30)
            y = random.randint(1, self.height - 30)
            bonus_position = (x, y)

        bonus = Bonus(bonus_position)
        self.bonuses.append(bonus)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)
                elif event.key == K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)
                elif event.key == K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)
                elif event.key == K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)
                elif event.key == K_ESCAPE:
                    self.game_over = True

    def game_over_check(self):
        head_x, head_y = self.snake.body[0]
        screen_width, screen_height = self.screen.get_size()

        # Check if the snake reaches the edge of the screen
        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height - self.panel_height - 2:
            self.game_over = True
            return

        # Check if the snake collides with itself
        if self.snake.check_self_collision():
            self.game_over = True
            return
        
        if self.points >= self.points_to_complete:
            self.game_over = True
            return

        self.game_over = False
    
    def handle_game_over(self):
        self.foods = []
        self.bonuses = []
        self.snake.body = []
        self.screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))
        self.screen.blit(text, text_rect)

        options = ["Restart", "See Personal Records", "Quit"]
        option_texts = []
        for i, option in enumerate(options):
            option_text = font.render(f"{i+1}. {option}", True, (255, 255, 255))
            option_text_rect = option_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 40))
            self.screen.blit(option_text, option_text_rect)
            option_texts.append((option_text, option_text_rect))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.restart_game()
                        return
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.show_personal_records()
                        return
                    elif event.key in (pygame.K_3, pygame.K_KP3, pygame.K_ESCAPE, pygame.K_q):
                        self.running = False
                        return
                elif event.type == pygame.QUIT:
                    self.running = False
                    return

    def restart_game(self):
        # Reset the game state and load the current level
        self.snake.reset()
        self.points = 0
        self.bonus_spawn_timer = pygame.time.get_ticks()
        self.load_level(1)

    def show_personal_records(self):
        personal_records = self.highscore.get_personal_records()

        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Display personal records
        font = pygame.font.Font(None, 36)
        title = font.render("Personal Records", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        for i, record in enumerate(personal_records):
            record_text = font.render(f"{i + 1}. {record}", True, (255, 255, 255))
            record_text_rect = record_text.get_rect(x = 100, y = 100 + i * 40)
            self.screen.blit(record_text, record_text_rect)

        prompt = font.render("Press any key to return", True, (255, 255, 255))
        prompt_rect = prompt.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(prompt, prompt_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_game_over()
                    return
                elif event.type == pygame.QUIT:
                    self.running = False
                    return
                
    def check_collision(self, obj_position, obj_size):
        snake_head_rect = pygame.Rect(self.snake.body[0][0] - self.snake.block_size // 2, self.snake.body[0][1] - self.snake.block_size // 2, self.snake.block_size, self.snake.block_size)
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)
        return snake_head_rect.colliderect(obj_rect)

    def update(self):
        self.snake.update()
        #self.bonus.update()
        #self.terrain.update()
        for food in self.foods:
            if self.check_collision(food.position, food.size):
                self.snake.grow()
                self.points += 1
                self.foods.remove(food)
                self.spawn_food()

        # Spawn a bonus with a certain probability
        current_time = pygame.time.get_ticks()
        if current_time - self.bonus_spawn_timer > self.bonus_spawn_interval:
            self.spawn_bonus()
            self.bonus_spawn_timer = current_time

        # Check if the snake has collected a bonus, apply the bonus effect and remove it from the list
        for bonus in self.bonuses:
            if self.check_collision(bonus.position, bonus.size):
                self.apply_bonus_effect(bonus)
                self.bonuses.remove(bonus)
                break

        # Check if the snake is on a terrain tile and apply the terrain effect
        for terrain in self.terrains:
            for tile_position in terrain.tiles:
                if self.check_collision(tile_position, 1.2):
                    if terrain.type == "slow_down":
                        self.snake.slow_down()
                    elif terrain.type == "speed_up":
                        self.snake.speed_up()
                    break

        self.game_over_check()
        if self.game_over:
            self.highscore.add_record(self.points)
            self.handle_game_over()
        pygame.time.delay(5)

    def apply_bonus_effect(self, bonus):
        if bonus.type == "speed_up":
            self.snake.speed_up()
        elif bonus.type == "add_points":
            self.points += 5
    
    def draw_panel(self):
        panel_y = self.height - self.panel_height
        panel_bg_color = (50, 50, 50)
        border_color = (255, 255, 255)
        border_thickness = 2

        # Draw the panel background
        pygame.draw.rect(self.screen, panel_bg_color, (0, panel_y, self.width, self.panel_height))
        pygame.draw.line(self.screen, border_color, (0, panel_y), (self.width, panel_y), border_thickness)

        # Set the font and color for the text
        font = pygame.font.Font(None, 20)
        text_color = (255, 255, 255)

        # Display the current points, length, speed, and time passed
        points_text = font.render(f"Points: {self.points}/{self.points_to_complete}", True, text_color)
        length_text = font.render(f"Length: {len(self.snake.body)}", True, text_color)
        speed_text = font.render(f"Speed: {self.snake.speed:.2f}", True, text_color)
        time_passed = pygame.time.get_ticks() // 1000
        time_text = font.render(f"Time: {time_passed}s", True, text_color)

        # Position the text elements on the panel
        self.screen.blit(points_text, (10, panel_y + self.panel_height // 2 - points_text.get_height() // 2))
        self.screen.blit(length_text, (150, panel_y + self.panel_height // 2 - length_text.get_height() // 2))
        self.screen.blit(speed_text, (290, panel_y + self.panel_height // 2 - speed_text.get_height() // 2))
        self.screen.blit(time_text, (430, panel_y + self.panel_height // 2 - time_text.get_height() // 2))

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.snake.draw(self.screen)
        for food in self.foods:
            food.draw(self.screen)
        for bonus in self.bonuses:
            bonus.draw(self.screen)
        self.draw_panel()
        #self.terrain.draw(self.screen)
        # Draw other game elements (e.g., score, lives)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(120)

