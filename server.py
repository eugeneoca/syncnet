import socket
import threading
import os
from time import sleep, time

class Server():

    name = ""
    host_address = ""
    client_listener_sock = ""
    port = 2000
    o_clients = []

    ttl = 0

    def __init__(self, name = "Network-Based Server", port=5000):
        self.set_name(name)
        self.set_port(port)
        self.host_address = self.get_host()

    def run(self):

        # --- Layout ---
        # Run Client Listener Thread
        #   - If client received, throw separate thread
        # Run Dead Client Listener Thread
        self.ttl = time()

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.bind((self.host_address, self.port))
        self.server_sock.setblocking(False)

        s_Listener = threading.Thread(target=self.server_listener)
        s_Listener.daemon = True
        s_Listener.start()

        while True:
            self.clear_log()
            self.server_log("Server running at "+self.host_address+":"+str(self.port))
            print("Active Clients: "+str(len(self.o_clients)))
            print("-------------------------------------------------------------------------")
            print("ID\t|\tIP ADDRESS\t|\tPORT\t|\t DATABASE")
            for i,client in enumerate(self.o_clients):
                print(str(i)+"\t|\t"+client[0]+"\t|\t"+str(client[1])+"\t|\t"+"{}")
            sleep(1) # Update screen every second only

    def server_listener(self):
        while True:

            if (time()-self.ttl)>5:
                self.check_connection()
                self.ttl = time()

            try:

                data, address = self.server_sock.recvfrom(1024)

                # Register new client
                if data.decode("UTF-8")=="REG" and (address not in self.o_clients):
                    self.o_clients.append(address)
                    self.server_sock.sendto("ACK".encode(), address)

                # Unregister client
                if data.decode("UTF-8")=="URG" and (address in self.o_clients):
                    self.o_clients.remove(address)

            except:
                pass

    def check_connection(self):
        # Check connection and remake client list
        local_clients = []
        for client in self.o_clients:
            self.server_sock.sendto("CHK".encode(), client)
            for t in range(20):
                # Twenty waits of activity
                try:
                    data, address = self.server_sock.recvfrom(100)
                    if data.decode("UTF-8")=="LIV":
                        local_clients.append(address)
                        break
                except Exception as error:
                    #print(error)
                    pass
        
        self.o_clients = local_clients


    def set_name(self, name):
        self.name = name

    def set_port(self, port):
        self.port = port

    def get_host(self):
        return socket.getfqdn()

    def clear_log(self):
        os.system("clear")

    def server_log(self, message):
        print("["+self.name+"] "+message)

if __name__ == "__main__":
    server = Server("Syncnet Server", 5000)
    server.run()