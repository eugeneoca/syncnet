import socket
import threading
import os
from time import *

SILENT_MODE = 0
if SILENT_MODE:
    def print(*args):
        pass

    def sleep(*args):
        pass


class Server():

    name = ""
    host_address = ""
    client_listener_sock = ""
    port = 2000
    o_clients = []

    ttl = 0

    def __init__(self, name="Network-Based Server", port=5000):
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
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host_address, self.port))
        self.server_sock.setblocking(False)

        s_Listener = threading.Thread(target=self.server_listener)
        s_Listener.daemon = True
        s_Listener.start()

        s_Stabilizer = threading.Thread(target=self.connection_stabilizer)
        s_Stabilizer.daemon = True
        s_Stabilizer.start()

        self.server_log("Server running at " +
                        self.host_address+":"+str(self.port))

        try:
            while True:
                pass
        except:
            print("Server terminated.")
        """
        #self.clear_log()
        self.server_log("Server running at " +
                        self.host_address+":"+str(self.port))
        
        
        print("Active Clients: "+str(len(self.o_clients)))
        print(
            "-------------------------------------------------------------------------")
        print("ID\t|\tIP ADDRESS\t|\tPORT\t|\t DATABASE")
        for i, client in enumerate(self.o_clients):
            print(str(i)+"\t|\t"+client[0] +
                    "\t|\t"+str(client[1])+"\t|\t"+"{}")
        """

    def server_listener(self):
        while True:
            try:

                data, address = self.server_sock.recvfrom(1024)

                # Register new client (REG => Register)
                if data.decode("UTF-8") == "REG" and (address not in self.o_clients):
                    self.o_clients.append(address)
                    self.server_sock.sendto("ACK".encode(), address)

                # Unregister client (URG => Unregister)
                if data.decode("UTF-8") == "URG" and (address in self.o_clients):
                    self.o_clients.remove(address)

                # Accept data from client (TSS => Transmitted State Status)
                if data.decode("UTF-8").split(':')[0] == "TSS" and len(data.decode("UTF-8")) > 4:
                    source = address[0]
                    content = data.decode("UTF-8")[4:]  #
                    print(content)
            except:
                pass

    def connection_stabilizer(self):
        pass
        """
        # Check connection and remake client list
        local_clients = []
        for client in self.o_clients:
            self.server_sock.sendto("CHK".encode(), client)
            for _ in range(1):
                # Twenty waits of activity
                try:
                    data, address = self.server_sock.recvfrom(1024)
                    if data.decode("UTF-8") == "LIV":
                        if address not in local_clients:
                            local_clients.append(address)
                        else:
                            continue
                except:
                    pass

        self.o_clients = local_clients

        """

    def set_name(self, name):
        self.name = name

    def set_port(self, port):
        self.port = port

    def get_host(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        addr = s.getsockname()[0]
        s.close()
        return addr

    def clear_log(self):
        os.system("cls")

    def server_log(self, message):
        print("["+self.name+"] "+message)


if __name__ == "__main__":
    server = Server("Syncnet Server", 5000)
    server.run()
