import threading
import socket
import time

server = socket.socket()
server.bind(('localhost', 12451))
server.listen(5)
con, addr = server.accept()

def send_data():
    while True:
        try:
            send = input(">>")
            con.send(send.encode())
            time.sleep(5)
        except Exception as e:
            print(f"Error sending data: {e}")

def recv_data():
    while True:
        try:
            data_recv = con.recv(1024)
            if data_recv:
                print(data_recv.decode())
            time.sleep(5)
        except Exception as e:
            print(f"Error receiving data: {e}")

threading.Thread(target=send_data).start()
threading.Thread(target=recv_data).start()