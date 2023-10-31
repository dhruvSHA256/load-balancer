import threading
import socket


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
