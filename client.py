import socket
import os
from time import sleep, time
import random

class Client():

    name = ""
    client_address = ""
    o_clients = []
    client_sock = ""
    client_port = 2001
    
    server_address = ""
    server_port = 2000

    finder_sock = ""

    ttl = 0

    def __init__(self, name = "Client", port = 5000):

        self.server_port = port
        port = random.randint(port+1, 10000) # Set random port
        self.name = name
        self.client_port = port
        self.client_address = self.get_host()

    def run(self):
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_sock.bind((self.client_address, self.client_port))
            self.client_sock.setblocking(False)
        except:
            self.client_log('Existing server or client using the socket.')
            exit(0)
        self.client_log("Client running at "+self.client_address+":"+str(self.client_port))

        # --- Layout ---
        # Find server by sending REG signal (Registration) - DONE
        # Once received an ACK signal, store server socket then do handshake (Verification) - DONE
        # Monitor external and internal immediate change signals (Monitoring)
        # For internal changes, transmit broadcast signal through the server (Synchronization)

        self.ttl = time()
        new_connection = True
        while True:
            if self.server_address=="":
                self.server_address = self.detect_server(self.server_port)

            if new_connection==True and self.server_address is not "":
                self.ttl = time()
                new_connection = False

            try:
                data, address = self.client_sock.recvfrom(100)
                if data.decode("UTF-8")=="CHK":
                    self.client_sock.sendto("LIV".encode(), address)
                    self.ttl = time()
            except Exception as error:
                if (time()-self.ttl)>10 and self.server_address is not "":
                    print(str(self.server_address) + " died. Waiting for new server...")
                    self.server_address=""
                    new_connection = True

    def detect_server(self, port):

        base_address = self.get_base_address()
        for last_octet in range(0,255):
            candidate_address = base_address+"."+str(last_octet)
            
            try:
                self.client_sock.sendto("REG".encode(), (candidate_address, port))
                data, sck = self.client_sock.recvfrom(1024)
                if data.decode("UTF-8")=="ACK":
                    print("Registered successfully on server "+sck[0]+":"+str(sck[1]))
                    return sck
            except:
                pass
        return "" # Return NULL String

    def get_base_address(self):
        return '.'.join(self.client_address.split('.')[:-1])

    def get_host(self):
        return socket.gethostbyname(socket.gethostname())

    def client_log(self, message):
        print("["+self.name+"] "+message)

if __name__ == "__main__":
    client = Client("Syncnet Client", 5000)
    client.run()