import socket
from backend.BackendServer import BackendServer
from algo import select_server
from algo.roundrobin import RoundRobin
from config.config import load_config, CONFIG_FILE
from health.health import check_health

# housekeeping
config = load_config(CONFIG_FILE)
servers_list = config["server"]
HOST = config.get("host", "127.0.0.1")
PORT = config.get("port", 5432)
servers = []
for s in servers_list:
    servers.append(BackendServer(int(s["id"]), s["host"], int(s["port"])))


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
    main()
