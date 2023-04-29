import socket
import threading
from . import config
from .game import Game

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game = None
        self.running = False

    def connect(self):
        self.socket.connect((self.server_ip, self.server_port))
        self.running = True
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def disconnect(self):
        self.running = False
        self.socket.close()

    def send_message(self, message_type, message_data):
        pass

    def receive_messages(self):
        while self.running:
            data = self.socket.recv(config.BUFFER_SIZE)
            if data:
                # Handle the message based on its type
                message_type, message_data = self.decode_message(data)
                if message_type == 'game_state':
                    # Update the game state with the new game state
                    self.game.update_game_state(message_data)

    def encode_message(self, message_type, message_data):
        pass

    def decode_message(self, message_data):
        pass
