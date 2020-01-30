import socket
from threading import Thread
import time
import json

server = ('localhost',5555)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('',0))

code = 0

def encrypt(text):


    return text

def reciever():
    while True:
        try:
            data = sock.recv(1024)
            data = data.decode('utf-8')
            data = json.loads(data)
            print(f"[{data[0]}] {data[1]}")
        except:
            pass

flow = Thread(target=reciever)
flow.start()

sock.sendto("Hello server!".encode('utf-8'), server)

while True:
    msg = input()
    if msg.startswith("/code"):
        _, code = msg.split(" ", maxsplit=1)
        continue
    msg = msg.encode('utf-8')
    sock.sendto(msg, server)
