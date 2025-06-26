import socket
import threading
from tkinter import *

client = socket.socket()
try:
    client.connect(('localhost', 63453))
except ConnectionRefusedError:
    print("Connection refused. Please check the server status.")
    exit()

root = Tk()

def send():
    data_send = get_message.get()
    if data_send != "":
        data_send = str(data_send)
        try:
            client.send(data_send.encode())
        except ConnectionResetError:
            print("Connection reset. Please check the server status.")
            exit()
        lbl = Label(root, text=data_send, bg="red", fg="white")
        get_message.delete(0, END)
        lbl.pack(fill="x", side="top")

def recv():
    while True:
        try:
            data_recv = client.recv(1024)
            if data_recv != b"":
                lbl = Label(root, text=data_recv.decode(), bg="blue", fg="white")
                lbl.pack(fill="x", side="top")
        except ConnectionResetError:
            print("Connection reset. Please check the server status.")
            break

get_message = Entry(root)
send_message = Button(root, text="Send", command=send)

send_message.pack(fill="x", side="bottom")
get_message.pack(fill="x", side="bottom")

threading.Thread(target=recv, daemon=True).start()

root.title("Chat Client")
root.geometry("500x700")
root.resizable(width=False, height=False)

root.mainloop()