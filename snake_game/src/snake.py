import pygame

class Snake:
    def __init__(self, color=(0, 255, 0), start_pos=(400, 300), block_size= 10, start_speed = 1):
        self.color = color
        self.block_size = block_size
        self.body = [start_pos]
        self.direction = (1, 0)
        self.speed = start_speed
        self.growth = 0

    def change_direction(self, new_direction):
        if self.direction[0] * new_direction[0] + self.direction[1] * new_direction[1] == 0:
            self.direction = new_direction

    def update(self):
        if self.direction == (0, 0):
            return

        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * self.speed / 5, head_y + self.direction[1] * self.speed / 5)
        self.body.insert(0, new_head)
        self.speed += 0.0005
        if self.growth > 0:
            self.growth -= 1
        else:
            self.body.pop()

    def grow(self, growth=1):
        self.growth += growth

    def speed_up(self):
        # Increase the snake's speed by a factor of choice
        self.speed *= 1.2

    def slow_down(self, slow_rate = 0.9):
        # Decrease the snake's speed by a factor of choice
        self.speed *= slow_rate

    def check_collision(self, position):
        for segment in self.body:
            if position == segment:
                return True
        return False

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            segment_rect = pygame.Rect(segment[0] - self.block_size // 2, segment[1] - self.block_size // 2, self.block_size, self.block_size)
            if i == 0:  # Head
                pygame.draw.rect(screen, self.color, segment_rect, border_radius=1)
            else:  # Body
                pygame.draw.rect(screen, self.color, segment_rect)

    def reset(self, start_pos=(400, 300)):
        self.body = [start_pos]
        self.direction = (1, 0)
        self.growth = 0

