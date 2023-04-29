import pygame
from threading import Thread
import socket
import sys
import json
from .network import Network
from . import config

import threading
from .game_multiplayer import GameMultiplayer

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((config.SERVER_IP, config.SERVER_PORT))
        self.socket.listen()
        self.clients = []
        self.game = None
        self.running = False

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.run)
        thread.start()

    def stop(self):
        self.running = False
        self.socket.close()
        for client in self.clients:
            client.close()

    def run(self):
        while self.running:
            # Accept incoming connections
            try:
                client_socket, client_address = self.socket.accept()
                self.clients.append(client_socket)
            except OSError:
                pass

            # Handle incoming messages from clients
            try:
                for client_socket in self.clients:
                    data = client_socket.recv(config.BUFFER_SIZE)
                    if data:
                        # Handle the message based on its type
                        message_type, message_data = self.decode_message(data)
                        if message_type == 'player_input':
                            # Update the game state with the player input
                            player_number, player_input = message_data
                            self.game.handle_input(player_number, player_input)
                            # Send the updated game state to all clients
                            self.send_all(self.encode_game_state(self.game.get_game_state()))
            except ConnectionResetError:
                self.stop()

            # Update the game state
            self.game.update()

            # Send the updated game state to all clients
            self.send_all(self.encode_game_state(self.game.get_game_state()))

        # Game over, send the final game state to all clients
        self.send_all(self.encode_game_state(self.game.get_game_state()))

    def encode_message(self, message_type, message_data):
        pass

    def decode_message(self, message_data):
        pass

    def send_all(self, data):
        pass


class ServerPlayer:
    def __init__(self, client_socket, player_number):
        self.client_socket = client_socket
        self.player_number = player_number

    def send_message(self, message_type, message_data):
        pass

    def receive_message(self):
        pass
