import socket
import sys

HOST = "127.0.0.1"
if len(sys.argv) <= 1:
    PORT = 5001
else:
    PORT = int(sys.argv[1])


def get_response(data):
    if data[0] == "GET /health HTTP/1.1":
        return "up"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.settimeout(10)
            sock.bind((HOST, PORT))
            sock.listen()
            print(f"Listening on port: {PORT}")
            while True:
                client_conn, client_addr = sock.accept()
                with client_conn:
                    print(f"Connected by {client_addr}")
                    data = client_conn.recv(1024).decode()
                    if not data:
                        break
                    header = data.split("\r")[0:-2]
                    clean_data = list(map(lambda x: x.lstrip("\n"), header))
                    response = get_response(clean_data) or f"hello from {HOST}:{PORT}"
                    http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{response}"
                    client_conn.send(http_response.encode())
        except KeyboardInterrupt:
            print("Ctrl-C pressed")
        except Exception as e:
            print(f"An exception occurred: {e}")
        finally:
            sock.close()


if __name__ == "__main__":
    main()
