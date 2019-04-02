import socket
import threading
import os
from time import sleep

class Client():

    name = ""
    host_address = ""
    client_listener_sock = ""
    port = 2000
    o_clients = []

    def __init__(self, name = "Client", port=2000):
        self.set_name(name)
        self.set_port(port)
        self.host_address = self.get_host()

    def run(self):
        # TEST
        # --- Layout ---
        # Find server by sending REG signal (Registration)
        # Once received an ACK signal, store server socket then do handshake (Verification)
        # Monitor external and internal immediate change signals (Monitoring)
        # For internal changes, transmit broadcast signal through the server (Synchronization)
        pass

    def set_name(self, name):
        self.name = name

    def set_port(self, port):
        self.port = port

    def get_host(self):
        return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    client = Client("Syncnet Client", 2000)
    client.run()