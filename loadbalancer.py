import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 5432
CONFIG_FILE = "config.json"


def get_config(config_file):
    config_obj = {}
    with open(config_file) as f:
        config_obj = json.load(f)
    return config_obj


# load server config from json file
# make objects of server
# server:
#   add : (host, port)
#   alive: Bool true/false
# servers: [server]

# health check
# in a seperate thread ping server and check if they are alive or not and set server.alive to true/false
# lb algo need to only consider servers which are alive

# get target server selected by LB algo
# for a particular client request we need to make sure we are sending the all packets to the same server


class BackendServer:
    def __init__(self, id_, host, port):
        self.id = id_
        self.host = host
        self.port = port
        self.alive = True

    def connect(self):
        self.backend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.backend_conn.connect((self.host, self.port))

    # client_conn -> lb <- backend_conn
    def reverse_proxy(self, client_conn):
        def forward_request(source, destination):
            print(f"Sending data from {source.getsockname()} to {destination.getsockname()}")
            try:
                while True:
                    data = source.recv(1024)
                    if len(data) == 0:
                        break
                    destination.send(data)
            finally:
                source.close()
                destination.close()

        c2b_thread = threading.Thread(target=forward_request, args=(client_conn, self.backend_conn))
        b2c_thread = threading.Thread(target=forward_request, args=(self.backend_conn, client_conn))
        c2b_thread.start()
        b2c_thread.start()
        c2b_thread.join()
        b2c_thread.join()


class RoundRobin:
    def __init__(self, servers_):
        self.idx = 0
        self.servers = servers_

    def next(self):
        self.idx += 1
        self.idx %= len(self.servers)
        return self.servers[self.idx]


def select_server(algo):
    return algo.next()


def main():
    rr = RoundRobin(servers)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Listening on port: {PORT}")
        while True:
            client_conn, client_addr = sock.accept()
            with client_conn:
                print(f"Connected by {client_addr}")
                # whenever we accept new client connection
                # we will load balance it
                # select_server will make sure server is healthy
                backend = select_server(rr)
                backend.connect()
                backend.reverse_proxy(client_conn)

    finally:
        sock.close()


# to test
# run backend servers
# run load balancer
# make a connection to load balancer

if __name__ == "__main__":
    config = get_config(CONFIG_FILE)
    servers_list = config["server"]
    servers = []
    for s in servers_list:
        servers.append(BackendServer(int(s["id"]), s["host"], int(s["port"])))
    main()
