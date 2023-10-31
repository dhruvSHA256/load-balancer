import socket
from backend import BackendServer
from algo import RoundRobin, select_server
from config import get_config, HOST, PORT, CONFIG_FILE

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
