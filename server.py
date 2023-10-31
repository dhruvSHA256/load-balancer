import socket
import sys

HOST = "127.0.0.1"
if len(sys.argv) <= 1:
    PORT = 5001
else:
    PORT = int(sys.argv[1])


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
                data = client_conn.recv(1024)
                if not data:
                    break
                response = f"Hello from {HOST}:{PORT}"
                http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{response}"
                client_conn.send(http_response.encode())
    finally:
        sock.close()


if __name__ == "__main__":
    main()
