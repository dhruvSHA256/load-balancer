import socket
import sys
from time import sleep

HOST = "127.0.0.1"
if len(sys.argv) <= 1:
    PORT = 5001
else:
    PORT = int(sys.argv[1])

server_address = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
request = f"GET / HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
client_socket.send(request.encode())
response = ""
data = client_socket.recv(1024)
response += data.decode()

print(response)
sleep(10)
client_socket.close()
