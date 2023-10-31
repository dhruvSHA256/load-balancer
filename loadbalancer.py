import socket

HOST = "127.0.0.1"
PORT = 5431


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Listening on port: {PORT}")
        while True:
            conn, addr = sock.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = "HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello, World!"
                    conn.sendall(response.encode())


if __name__ == "__main__":
    main()
