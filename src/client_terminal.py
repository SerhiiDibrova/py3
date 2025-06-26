import threading
import socket

client = socket.socket()
client.connect(('localhost' , 12451))

def recv():
    while True:
        try:
            data_get = client.recv(1024)
            if not data_get:
                break
            print(data_get.decode('utf-8', errors='replace'))
        except ConnectionResetError:
            print("Connection reset by peer")
            break
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    client.close()

def send():
    while True:
        try:
            text = input(">>")
            client.send(text.encode('utf-8', errors='replace'))
        except ConnectionResetError:
            print("Connection reset by peer")
            break
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    client.close()

threading.Thread(target=send).start()
threading.Thread(target=recv).start()