import socket
import threading
import os
from time import sleep

class Client():

    name = ""
    host_address = ""
    
    port = 2000
    o_clients = []
    server_sock = ""
    client_sock = ""

    def __init__(self, name = "Client", port=2000):
        self.set_name(name)
        self.set_port(port)
        self.host_address = self.get_host()

    def run(self):
        self.server_descriptor = self.detect_server(self.port)
        # --- Layout ---
        # Find server by sending REG signal (Registration)
        # Once received an ACK signal, store server socket then do handshake (Verification)
        # Monitor external and internal immediate change signals (Monitoring)
        # For internal changes, transmit broadcast signal through the server (Synchronization)
        pass

    def detect_server(self, port):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_sock.bind((self.host_address, self.port))
        self.client_log("Client running at "+self.host_address+":"+str(self.port))
        print("Looking for active server...")
        


        return 0

    def set_name(self, name):
        self.name = name

    def set_port(self, port):
        self.port = port

    def get_host(self):
        return socket.gethostbyname(socket.gethostname())

    def client_log(self, message):
        print("["+self.name+"] "+message)

if __name__ == "__main__":
    client = Client("Syncnet Client", 2000)
    client.run()