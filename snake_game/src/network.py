import socket
import pickle
from .config import BYTES_RECV

class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5432  # Choose an appropriate port number
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.connected = True

    def get_player_id(self):
        player_id = self.recv_data()
        return int(player_id)

    def get_game_state(self):
        try:
            self.send_data(('request_game_state',))
            return self.recv_data()
        except socket.error as e:
            print('Connection lost')
            self.connected = False
            return {'end_reason': 'server_closed'}


    def send_data(self, data):
        if not self.connected:
            return
        try:
            message = pickle.dumps(data)
            message_length = len(message)
            print(f"Sending data: {data}")
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
        try:
            message_length = int.from_bytes(self.recvall(4), 'big')
            data = self.recvall(message_length)
            #print(f"Received data: {pickle.loads(data)}")
            return pickle.loads(data)
        except (pickle.UnpicklingError, ValueError, EOFError, socket.error) as e:
            print(f"Error network receiving data: {e}")
            return None

