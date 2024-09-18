import threading
import socket

client = socket.socket()
client.connect(('localhost', 12451))

def recv():
    while True:
        data_get = client.recv(1024)
        print(data_get.decode('utf-8'))

def send():
    while True:
        text = input(">>")
        client.send(text.encode('utf-8'))

threading.Thread(target=send).start()
threading.Thread(target=recv).start()