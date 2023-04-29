import socket
import json

class Network:
    def __init__(self, server_ip, server_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.addr = (server_ip, server_port)
        self.player_id = self.connect()
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.client.recv(1024).decode()
            return int(data)
        except:
            pass
        
    def send(self, data):
        try:
            self.client.send(str.encode(json.dumps(data)))
            reply = self.client.recv(2048).decode()
            return json.loads(reply)
        except socket.error as e:
            print(e)
            
    def disconnect(self):
        self.client.close()
