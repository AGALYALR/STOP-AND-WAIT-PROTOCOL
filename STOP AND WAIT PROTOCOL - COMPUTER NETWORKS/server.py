import socket
import struct
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Server is listening on port 12345")

conn, addr = server_socket.accept()
print("Connected by", addr)

d = json.loads(conn.recv(1024).decode())
p = struct.unpack('!i', conn.recv(4))[0]

for i in range(p + 1):
    if i in d:
        print(f"Packet {i} dropped")
        continue
    data = struct.unpack('!i', conn.recv(4))[0]
    if data == -2:
        break
    print(f"Packet {data} received, sending acknowledgment...")
    conn.send(struct.pack('!i', data))

print("Closing connection")
conn.close()
