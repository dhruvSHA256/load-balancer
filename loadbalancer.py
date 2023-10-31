import socket
import threading

HOST = "127.0.0.1"
PORT = 5432

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


def select_server():
    return "127.0.0.1", 5001


def reverse_proxy(client_conn, backend_conn):
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

    c2b_thread = threading.Thread(target=forward_request, args=(client_conn, backend_conn))
    b2c_thread = threading.Thread(target=forward_request, args=(backend_conn, client_conn))
    c2b_thread.start()
    b2c_thread.start()
    c2b_thread.join()
    b2c_thread.join()


def main():
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
                backend_host, backend_port = select_server()
                backend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                backend_conn.connect((backend_host, backend_port))
                # so now client_conn -> lb <- backend_conn
                # we need to redirect requests
                # first make sort of a reverse proxy
                reverse_proxy(client_conn, backend_conn)

    finally:
        sock.close()


# to test
# run backend servers
# run load balancer
# make a connection to load balancer

if __name__ == "__main__":
    main()
