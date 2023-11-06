import socket
from threading import Thread
from typing import Dict, List, Tuple
from backend.BackendServer import BackendServer
from algo import Algo, select_server
from algo.roundrobin import RoundRobin
from algo.leastconnection import LeastConnection
from config.config import load_config, CONFIG_FILE
from health.health import check_health

# housekeeping
config: Dict = load_config(CONFIG_FILE)
servers_list: List[Dict] = config["server"]
HOST: str = config.get("host", "127.0.0.1")
PORT: int = config.get("port", 5432)
servers: List[BackendServer] = []
for server in servers_list:
    servers.append(BackendServer(int(server["id"]), server["host"], int(server["port"])))


def main():
    rr: Algo = RoundRobin()
    lc: Algo = LeastConnection()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threads: List[Thread] = check_health(servers)
    try:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Listening on port: {PORT}")
        while True:
            sock_conn: Tuple[socket.socket, socket.AddressInfo] = sock.accept()
            client_conn, client_addr = sock_conn
            with client_conn:
                print(f"Connected by {client_addr}")
                # backend: BackendServer = select_server(lc, servers)
                backend: BackendServer = select_server(rr, servers)
                if backend:
                    backend.reverse_proxy(client_conn)
                    print(backend.num_connections)
    finally:
        sock.close()
        map(lambda t: t.join(), threads)


if __name__ == "__main__":
    main()
