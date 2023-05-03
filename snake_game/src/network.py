import socket
import pickle
from .config import BYTES_RECV

class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555  # Choose an appropriate port number
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)

    def get_player_id(self):
        player_id = self.recv_data()
        return int(player_id)

    def get_game_state(self):
        try:
            self.send_data(('request_game_state',))
            return self.recv_data()
        except socket.error as e:
            print(e)


    def send_data(self, data):
        try:
            message = pickle.dumps(data)
            message_length = len(message)
            self.client.send(message_length.to_bytes(4, 'big'))
            self.client.send(message)
        except socket.error as e:
            print(e)

    def recvall(self, length):
        data = b''
        while len(data) < length:
            more = self.client.recv(length - len(data))
            if not more:
                raise EOFError('Socket closed before receiving all data')
            data += more
        return data

    def recv_data(self):
        message_length = int.from_bytes(self.recvall(4), 'big')
        data = self.recvall(message_length)
        return pickle.loads(data)

