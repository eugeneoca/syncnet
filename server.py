import socket
import threading
import os
from time import sleep

class Server():

    name = ""
    host_address = ""
    client_listener_sock = ""
    port = 2000
    o_clients = []

    def __init__(self, name = "Network-Based Server", port=2000):
        self.set_name(name)
        self.set_port(port)
        self.host_address = self.get_host()

    def run(self):

        # --- Layout ---
        # Run Client Listener Thread
        #   - If client received, throw separate thread
        # Run Dead Client Listener Thread

        c_Listener = threading.Thread(target=self.client_listener)
        c_Listener.daemon = True
        c_Listener.start()

        while True:
            self.clear_log()
            self.server_log("Server running at "+self.host_address+":"+str(self.port))
            print("Active Clients: "+str(len(self.o_clients)))
            print("-------------------------------------------------------------------------")
            print("ID\t|\tIP ADDRESS\t|\tPORT")
            for i,client in enumerate(self.o_clients):
                print(str(i)+"\t|\t"+client[0]+"\t|\t"+str(client[1]))
            sleep(1) # Update screen every second only

    def client_listener(self):
        self.client_listener_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_listener_sock.bind((self.host_address, self.port))
        while True:
            data, address = self.client_listener_sock.recvfrom(1024)
            try:
                # Register new client
                if data.decode("UTF-8")=="REG" and (address not in self.o_clients):
                    self.o_clients.append(address)

                # Unregister client
                if data.decode("UTF-8")=="URG" and (address in self.o_clients):
                    self.o_clients.remove(address)

            except Exception as error:
                self.server_log(error)

    def set_name(self, name):
        self.name = name

    def set_port(self, port):
        self.port = port

    def get_host(self):
        return socket.gethostbyname(socket.gethostname())

    def clear_log(self):
        os.system("cls")

    def server_log(self, message):
        print("["+self.name+"] "+message)

if __name__ == "__main__":
    server = Server("Syncnet Server", 2000)
    server.run()