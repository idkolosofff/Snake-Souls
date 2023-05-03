import json
import random
import pygame
import pickle
import socket
import threading
from threading import Lock
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE
from .snake import Snake
from .bonus import Bonus
from .terrain import Terrain
from .highscore import Highscore
from .food import Food
from .drawing import draw_game
from . import config

class Server:
    def __init__(self, ip='localhost', port=5555):
        self.clients = {}
        self.client_id_counter = 0
        self.running = True
        self.game_over = False
        self.width, self.height = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.panel_height = config.PANEL_HEIGHT
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.foods = []
        self.terrains = []
        self.bonus_spawn_timer = 0
        self.grail_spawn_timer = 0
        self.shroom_spawn_timer = 0 # Time in milliseconds between bonus spawns
        self.bonus_spawn_interval = config.BONUS_SPAWN_INTERVAL  
        self.load_level(config.DEFAULT_LEVEL)
        self.clients_to_remove = {}

        self.game_state_lock = Lock()
        self.addr = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.server.listen(config.WAIT_LIST_SIZE)
        self.accept_connections_thread = threading.Thread(target=self.accept_connections)
        self.accept_connections_thread.start()

        self.ticks = 1

    def accept_connections(self):
        print("Server is listening for connections...")
        while self.running:
            try:
                conn, addr = self.server.accept()
                print(f"New connection from {addr}")
                # Handle the new connection (e.g., add the client to the clients list)
                self.add_client(conn, addr)
            except:
                break
        print("Server stopped listening for connections.")

    def send_data(self, connection, data):
        message = pickle.dumps(data)
        message_length = len(message)
        connection.send(message_length.to_bytes(4, 'big'))
        connection.send(message)

    def recvall(self, connection, length):
        data = b''
        while len(data) < length:
            more = connection.recv(length - len(data))
            if not more:
                raise EOFError('Socket closed before receiving all data')
            data += more
        return data

    def recv_data(self, connection):
        message_length = int.from_bytes(self.recvall(connection, 4), 'big')
        data = self.recvall(connection, message_length)
        return pickle.loads(data)

    def add_client(self, connection, address):
        client_id = self.client_id_counter
        start_y = random.randint(2 * config.SNAKE_SIZE, config.SCREEN_HEIGHT - config.SNAKE_SIZE)
        start_x = 2 * config.SNAKE_SIZE

        # Send client's id
        self.send_data(connection, client_id)
        self.client_id_counter += 1

        self.clients[client_id] = {
            'connection': connection,
            'address': address,
            'snake': Snake(start_pos=(start_x, start_y)),
            'end_reason' : '',
        }
        print(f"Client {client_id} connected: {address}")
        print(self.clients)
        handle_messages_thread = threading.Thread(target=self.handle_client_messages, args=(client_id,))
        handle_messages_thread.start()

    def disconnect_client(self, client_id):
        client_data = self.clients[client_id]
        #self.send_data(client_data['connection'], {'end_reason': 'game_over'})
        self.clients_to_remove[client_id] = True

    def remove_client(self, client_id):
        print(f"removing {client_id} client ...")
        if client_id in self.clients:
            del self.clients[client_id]
        if client_id in self.clients_to_remove:
            del self.clients_to_remove[client_id]
        print(f"Client {client_id} disconnected")

    def prepare_game_state(self):
        with self.game_state_lock:
            game_state = {
                'terrains': [terrain.get_terrain_data() for terrain in self.terrains],
                'snakes': {client_id: client_data['snake'].get_snake_data() for client_id, client_data in self.clients.items() if not client_data['snake'].lost},
                'foods': [food.get_food_data() for food in self.foods],
                'bonuses': [bonus.get_bonus_data() for bonus in self.bonuses],
                'points_to_complete': self.points_to_complete,
                'start_time': self.start_time,
            }
            return game_state
        

    def handle_client_messages(self, client_id):
        client_data = self.clients[client_id]
        connection = client_data['connection']

        while self.running and not client_data['snake'].lost:
            try:
                message = self.recv_data(connection)
                if message[0] == 'update_direction':
                    new_direction = message[2]
                    client_data['snake'].direction = new_direction
                elif message[0] == 'request_game_state':
                    game_state = self.prepare_game_state()
                    self.send_data(connection, game_state)
                elif message[0] == 'disconnecting':
                    client_data['snake'].lost = True
            except socket.error as e:
                print(e)
                break
            except EOFError:
                print(f"Client {client_id} is disconnecting ...")
                break
        
        print(f"removing {client_id} client ...")
        # If the loop is broken, remove the client
        if client_data['snake'].lost:
            client_data['end_reason'] = 'lost'
        self.remove_client(client_id)

    def load_level(self, level_number):
        level_file = f"snake_game/levels/level_{level_number}.json"
        with open(level_file, "r") as file:
            level_data = json.load(file)

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

    # (The rest of the methods from game.py should be included here, with necessary modifications)
    def spawn_food(self):
        while True:
            x = random.randint(config.SCREEN_EDGE_SIZE, self.width - config.SCREEN_EDGE_SIZE)
            y = random.randint(config.SCREEN_EDGE_SIZE, self.height - config.SCREEN_EDGE_SIZE - self.panel_height)
            food_position = (x, y)

            if not (self.check_collision(food_position, Food.size) or self.check_collision_with_terrain(food_position, Food.size)):
                break

        food = Food(food_position)
        self.foods.append(food)

    def spawn_bonus(self):
        while True:
            x = random.randint(config.SCREEN_EDGE_SIZE, self.width - config.SCREEN_EDGE_SIZE)
            y = random.randint(config.SCREEN_EDGE_SIZE, self.height - config.SCREEN_EDGE_SIZE - self.panel_height)
            bonus_position = (x, y)
            bonus_type = random.choice(self.possible_bonus_types)
            bonus_size = config.BONUS_SIZES[bonus_type]

            if not (self.check_collision(bonus_position, bonus_size) or self.check_collision_with_terrain(bonus_position, bonus_size)):
                break

        bonus = Bonus(bonus_position, bonus_type)
        self.bonuses.append(bonus)

    def grow_mushroom(self):
        # Find all mushroom terrain
        mushroom_size = config.TERRAIN_SIZES["mushroom"]
        mushroom_terrains = [terrain for terrain in self.terrains if terrain.type == "mushroom"]

        # If no mushroom terrain, do nothing
        if not mushroom_terrains:
            return

        # Choose a random mushroom terrain
        mushroom = random.choice(mushroom_terrains)

        # Calculate adjacent positions
        adjacent_positions = [
            (mushroom.position[0] + mushroom_size, mushroom.position[1]),
            (mushroom.position[0] - mushroom_size, mushroom.position[1]),
            (mushroom.position[0], mushroom.position[1] + mushroom_size),
            (mushroom.position[0], mushroom.position[1] - mushroom_size),
        ]

        # Filter out positions outside the screen
        adjacent_positions = [
            pos for pos in adjacent_positions
            if (0 <= pos[0] <= self.width) and (0 <= pos[1] <= self.height - self.panel_height)
            and not self.is_position_occupied_by_mushroom(pos)
        ]

        # Choose a random adjacent position
        if not adjacent_positions:
            return
        new_mushroom_position = random.choice(adjacent_positions)

        # Check if the new position collides with existing terrain
        if not self.check_collision_with_terrain(new_mushroom_position, mushroom_size):
            # Create a new mushroom terrain at the chosen position
            new_mushroom = Terrain(new_mushroom_position, "mushroom")
            self.terrains.append(new_mushroom)

    def move_grail(self):
        x = random.randint(config.SCREEN_EDGE_SIZE, self.width - config.SCREEN_EDGE_SIZE)
        y = random.randint(config.SCREEN_EDGE_SIZE, self.height - config.SCREEN_EDGE_SIZE - self.panel_height)
        grail_position = (x, y)
        for terrain in self.terrains:
            if terrain.type == "holy_grail":
                terrain.position = grail_position

    def is_position_occupied_by_mushroom(self, position):
        for terrain in self.terrains:
            if terrain.type == "mushroom" and terrain.position == position:
                return True
        return False

    def check_collision(self, obj_position, obj_size, increment=0, self_id=-1):
        collisions = {}
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)
        for client_id, client_data in self.clients.items():
            if client_id == self_id:
                continue
            snake = client_data['snake']
            for segment in snake.body[increment:]:
                segment_rect = pygame.Rect(segment[0] - snake.block_size // 2, segment[1] - snake.block_size // 2, snake.block_size, snake.block_size)
                if obj_rect.colliderect(segment_rect):
                    collisions[client_id] = True

        return collisions
    
    def check_collision_with_terrain(self, obj_position, obj_size):
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)

        for terrain in self.terrains:
            terrain_rect = pygame.Rect(terrain.position[0] - terrain.size // 2, terrain.position[1] - terrain.size // 2, terrain.size, terrain.size)
            if obj_rect.colliderect(terrain_rect) and terrain.type == "wall":
                return True

        return False

    def check_snake_head_collisions(self):
        collisions = {}
        for client_id, client_data in self.clients.items():
            head_snake = client_data['snake']
            head_position = head_snake.body[0]
            head_size = head_snake.block_size

            collided = self.check_collision(head_position, head_size, self_id=client_id)# or self.check_edge_collision(head_position, head_size) TODO
            if collided:
                collisions[client_id] = True
        return collisions
    # ...
    def check_edge_collision(self, obj_position, obj_size):  #TODO, ACTS INSANE
        pos_x, pos_y = obj_position
        screen_width, screen_height = config.SCREEN_WIDTH, config.SCREEN_HEIGHT

        # Check if the obj reaches the edge of the screen
        if pos_x < 0 or pos_x >= screen_width or pos_y < 0 or pos_y >= screen_height - self.panel_height:
            print("Wall got hit")
            return True
        return False

    def check_end_conditions(self):
        # Check if a player has reached the points limit
        for client_id, client_data in self.clients.items():
            if client_data['snake'].points >= self.points_to_complete:
                return {'end_reason': 'win', 'winner_id': client_id}

        # Check if all players have lost

        # Return None if there are no end conditions met
        return None

    def update(self):
        with self.game_state_lock:
            for client_id, client_data in self.clients.items():
                #print(f"Snake {client_id} is here")
                snake = client_data["snake"]
                snake.update()

            for food in self.foods:
                food_collisions = self.check_collision(food.position, food.size)
                if food_collisions:
                    first_key = next(iter(food_collisions))  # host advantage hehe
                    self.clients[first_key]['snake'].grow(config.SNAKE_GROWTH_RATE)
                    self.clients[first_key]['snake'].points += 1
                    self.foods.remove(food)
                    self.spawn_food()

            # Check if the snake has collected a bonus, apply the bonus effect and remove it from the list
            for bonus in self.bonuses:
                bonus_collision = self.check_collision(bonus.position, bonus.size)
                if bonus_collision:
                    first_key = next(iter(bonus_collision))  # host advantage fr
                    if bonus.type == "speed_up":
                        self.clients[first_key]['snake'].speed_up()
                    elif bonus.type == "add_points":
                        self.clients[first_key]['snake'].points += config.BONUS_POINTS
                    elif bonus.type == "slow_down":
                        self.clients[first_key]['snake'].slow_down()  #PAUSED HERE
                    self.bonuses.remove(bonus)

            # Check if the snake is on a terrain tile and apply the terrain effect
            for terrain in self.terrains:
                terrain_collision = self.check_collision(terrain.position, terrain.size)
                for collision_id in terrain_collision:
                    curr_snake = self.clients[collision_id]['snake']
                    if terrain.type == "slow_down":
                        curr_snake.slow_down(config.TERRAIN_SLOW_RATE)
                    
                    if terrain.type == "speed_up":
                        curr_snake.speed_up(config.TERRAIN_SPEEDUP_RATE)
                    
                    if terrain.type == "wall":
                        curr_snake.lost = True
                    
                    if terrain.type == "mushroom":
                        curr_snake.trip()
                    
                    if terrain.type == "holy_grail":
                        curr_snake.points += config.HOLY_GRAIL_ADD

            current_time = pygame.time.get_ticks() - self.start_time
            if current_time - self.grail_spawn_timer > config.GRAIL_CHANGE_TIME:
                self.move_grail()
                self.grail_spawn_timer = current_time
            
            if current_time - self.shroom_spawn_timer > config.MUSHROOM_GROW_TIME:
                self.grow_mushroom()
                self.shroom_spawn_timer = current_time

            # Spawn a bonus after a certain time
            if current_time - self.bonus_spawn_timer > self.bonus_spawn_interval:
                self.spawn_bonus()
                self.bonus_spawn_timer = current_time

            collisions = self.check_snake_head_collisions()
            for client_id, client_lost in collisions.items():
                print (f"Player {client_id} is smashed")
                self.clients[client_id]['snake'].lost = client_lost
        

    def run(self):
        while self.running:
            self.update()
            self.clock.tick(config.CLOCK_TICK)
        self.shutdown()

    def shutdown(self):
        self.running = False
        self.server.close()
        for client_data in self.clients.values():
            client_data['connection'].close()
        self.accept_connections_thread.join()