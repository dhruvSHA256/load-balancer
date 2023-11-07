import socket
from threading import Thread
from typing import Dict, List, Tuple
from backend.BackendServer import BackendServer
from algo import Algo, select_server
from algo.roundrobin import RoundRobin
from algo.leastconnection import LeastConnection
from config.config import config
from health.health import check_health

servers_list: List[Dict] = config["server"]
HOST: str = config.get("host", "127.0.0.1")
PORT: int = config.get("port", 5432)
servers: List[BackendServer] = []
for server in servers_list:
    servers.append(BackendServer(
        int(server["id"]), server["host"], int(server["port"])))


def main():
    algo = None
    match config.get("algo", "RoundRobinn"):
        case "RoundRobin": algo = RoundRobin()
        case "LeastConnection": algo = LeastConnection()
    if not algo:
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    health_threads: List[Thread] = check_health(servers)
    proxy_threads: List[Thread] = []
    try:
        sock.bind((HOST, PORT))
        sock.listen(1000)
        print(f"Listening on port: {PORT}")
        while True:
            sock_conn: Tuple[socket.socket, socket.AddressInfo] = sock.accept()
            client_conn, client_addr = sock_conn
            print(f"Connected by {client_addr}")
            backend: BackendServer = select_server(algo, servers)
            if backend:
                proxy_thread = Thread(
                    target=backend.reverse_proxy, args=(client_conn,))
                proxy_threads.append(proxy_thread)
                proxy_thread.start()
    finally:
        sock.close()
        map(lambda t: t.join(), health_threads)
        map(lambda t: t.join(), proxy_threads)


if __name__ == "__main__":
    main()
