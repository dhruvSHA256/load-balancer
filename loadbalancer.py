import socket
from backend import BackendServer
from algo import RoundRobin, select_server
from config import get_config, CONFIG_FILE
from health import check_health
import sys

HOST = "127.0.0.1"
if len(sys.argv) <= 1:
    PORT = 5432
else:
    PORT = int(sys.argv[1])


def main():
    rr = RoundRobin(servers)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threads = check_health(servers)
    try:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Listening on port: {PORT}")
        while True:
            client_conn, client_addr = sock.accept()
            with client_conn:
                print(f"Connected by {client_addr}")
                backend = select_server(rr)
                if backend:
                    backend.reverse_proxy(client_conn)
    finally:
        sock.close()
        map(lambda t: t.join(), threads)


if __name__ == "__main__":
    config = get_config(CONFIG_FILE)
    servers_list = config["server"]
    servers = []
    for s in servers_list:
        servers.append(BackendServer(int(s["id"]), s["host"], int(s["port"])))
    main()
