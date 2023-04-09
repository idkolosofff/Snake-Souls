import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE
import json
import random

from .snake import Snake
from .bonus import Bonus
from .terrain import Terrain
from .highscore import Highscore
from .food import Food


class Game:
    def __init__(self, screen, highscore, level):
        self.screen = screen
        self.highscore = highscore
        self.running = True
        self.game_over = False
        self.width, self.height = screen.get_size()
        self.panel_height = 30
        self.clock = pygame.time.Clock()
        self.foods = []
        self.snake = Snake()
        self.level_number = level
        self.points = 0
        self.start_time = pygame.time.get_ticks()
        self.bonus_spawn_timer = 0
        self.bonus_spawn_interval = 20000  # Time in milliseconds between bonus spawns
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
            terrain = Terrain(terrain_data["position"], terrain_data["type"])
            self.terrains.append(terrain)

        # Initialize other game elements
        self.spawn_food()
        self.bonuses = []

    def spawn_food(self):
        while True:
            x = random.randint(20, self.width - 30)
            y = random.randint(20, self.height - 50)
            food_position = (x, y)

            if not (self.check_collision(food_position, Food.size) or self.check_collision_with_terrain(food_position, Food.size)):
                break

        food = Food(food_position)
        self.foods.append(food)

    def spawn_bonus(self):
        while True:
            x = random.randint(20, self.width - 30)
            y = random.randint(20, self.height - 50)
            bonus_position = (x, y)
            bonus_type = random.choice(self.possible_bonus_types)
            bonus_size = Bonus.bonus_sizes[bonus_type]

            if not (self.check_collision(bonus_position, bonus_size) or self.check_collision_with_terrain(bonus_position, bonus_size)):
                break

        bonus = Bonus(bonus_position, bonus_type)
        self.bonuses.append(bonus)

    def check_collision(self, obj_position, obj_size, increment = 0):
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)
        for segment in self.snake.body[increment:]:
            segment_rect = pygame.Rect(segment[0] - self.snake.block_size // 2, segment[1] - self.snake.block_size // 2, self.snake.block_size, self.snake.block_size)
            if obj_rect.colliderect(segment_rect):
                return True

        return False
    
    def check_collision_with_terrain(self, obj_position, obj_size):
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)

        for terrain in self.terrains:
            terrain_rect = pygame.Rect(terrain.position[0] - terrain.size // 2, terrain.position[1] - terrain.size // 2, terrain.size, terrain.size)
            if obj_rect.colliderect(terrain_rect) and terrain.type == "wall":
                return True

        return False

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
        if self.game_over:
            return
        head_x, head_y = self.snake.body[0]
        screen_width, screen_height = self.screen.get_size()

        # Check if the snake reaches the edge of the screen
        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height - self.panel_height - 2:
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
        self.highscore.add_score(self.points)
        self.screen.fill((0, 0, 0))

        self.show_game_over()

        self.screen.fill((0, 0, 0))
        self.running = False
    
    def show_game_over(self):
        self.screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.delay(1000)  # Show the "Game Over" text for 2 seconds

    def update(self):
        self.snake.update()

        self.game_over = self.check_collision(self.snake.body[0], self.snake.block_size, int(200 // self.snake.speed)) #Check if Head collides with the tail

        for food in self.foods:
            if self.check_collision(food.position, food.size):
                self.snake.grow(10)
                self.points += 1
                self.foods.remove(food)
                self.spawn_food()

        # Spawn a bonus after a certain time
        current_time = pygame.time.get_ticks() - self.start_time
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
            if self.check_collision(terrain.position, terrain.size):
                if terrain.type == "slow_down":
                    self.snake.slow_down(0.999)
                elif terrain.type == "speed_up":
                    self.snake.speed_up(1.001)
                elif terrain.type == "wall":
                    self.game_over = True
                break

        self.game_over_check()
        if self.game_over:
            self.handle_game_over()
        pygame.time.delay(5)

    def apply_bonus_effect(self, bonus):
        if bonus.type == "speed_up":
            self.snake.speed_up()
        elif bonus.type == "add_points":
            self.points += 5
        elif bonus.type == "slow_down":
            self.snake.slow_down()
    
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
        length_text = font.render(f"Length: {len(self.snake.body) // 10}", True, text_color)
        speed_text = font.render(f"Speed: {self.snake.speed:.2f}", True, text_color)
        time_passed = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = font.render(f"Time: {time_passed}s", True, text_color)

        # Position the text elements on the panel
        self.screen.blit(points_text, (10, panel_y + self.panel_height // 2 - points_text.get_height() // 2))
        self.screen.blit(length_text, (150, panel_y + self.panel_height // 2 - length_text.get_height() // 2))
        self.screen.blit(speed_text, (290, panel_y + self.panel_height // 2 - speed_text.get_height() // 2))
        self.screen.blit(time_text, (430, panel_y + self.panel_height // 2 - time_text.get_height() // 2))

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        for terrain in self.terrains:
            terrain.draw(self.screen)
        self.snake.draw(self.screen)
        for food in self.foods:
            food.draw(self.screen)
        for bonus in self.bonuses:
            bonus.draw(self.screen)
        self.draw_panel()
        # Draw other game elements (e.g., score, lives)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(120)

