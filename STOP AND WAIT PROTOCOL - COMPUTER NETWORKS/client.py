import socket
import time
import struct
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
sock.connect(server_address)

print()
print("---------------------  S T O P   A N D   W A I T  ---------------------")
print()
p = int(input("Enter the total number of packets: "))
arr = list(map(int, input("Enter the packets to be dropped: ").split()))
d = {k: True for k in arr}

sock.sendall(json.dumps(d).encode())
sock.send(struct.pack("!i", p - 1))
sock.settimeout(4)

i = 0
while i < p:
    try:
        sock.send(struct.pack("!i", i))
        print("Packet %d sent.." % i)
        b = struct.unpack('!i', sock.recv(4))[0]
        if b == i:
            print("Acknowledgment", b, "received..")
            i += 1
        else:
            print("Acknowledgment", b, "received (duplicate)...")
        time.sleep(2)
    except socket.timeout:
        print("***** Session Timed Out *****")
        print("Retransmitting the last message...")
        time.sleep(2)

sock.send(struct.pack("!i", -2))
sock.close()
