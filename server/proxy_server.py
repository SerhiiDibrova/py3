import socket
import select
import threading
import argparse
import configparser
import sys

DEBUG = False

def help():
    print("Usage: proxy_server.py [options]")
    print("Options:")
    print("  -h, --help            show this help message and exit")
    print("  -L, --local=LOCAL     specify local port to listen on")
    print("  -R, --remote=REMOTE   specify remote port to forward to")
    print("  -D, --dynamic         enable dynamic port forwarding")
    print("  -d, --debug           enable debug messages")

def debug(message):
    global DEBUG
    if DEBUG:
        print(f"DEBUG: {message}")

def forward_port_handler(client_socket, remote_host, remote_port):
    debug("Forwarding port handler started")
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        debug("Connected to remote host")
        while True:
            readable, writable, errored = select.select([client_socket, remote_socket], [], [])
            for sock in readable:
                if sock == client_socket:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    remote_socket.sendall(data)
                elif sock == remote_socket:
                    data = remote_socket.recv(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
        client_socket.close()
        remote_socket.close()
    except Exception as e:
        debug(f"Error in forward_port_handler: {e}")
        client_socket.close()

def forward_port(local_host, local_port, remote_host, remote_port):
    debug("Forwarding port started")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((local_host, local_port))
        server_socket.listen(5)
        while True:
            client_socket, address = server_socket.accept()
            debug(f"Client connected from {address}")
            client_handler = threading.Thread(target=forward_port_handler, args=(client_socket, remote_host, remote_port))
            client_handler.start()
    except Exception as e:
        debug(f"Error in forward_port: {e}")

def dynamic_forward_port_handler(client_socket, remote_host, remote_port):
    debug("Dynamic forwarding port handler started")
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        debug("Connected to remote host")
        while True:
            readable, writable, errored = select.select([client_socket, remote_socket], [], [])
            for sock in readable:
                if sock == client_socket:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    remote_socket.sendall(data)
                elif sock == remote_socket:
                    data = remote_socket.recv(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
        client_socket.close()
        remote_socket.close()
    except Exception as e:
        debug(f"Error in dynamic_forward_port_handler: {e}")
        client_socket.close()

def dynamic_forward_port(local_host, local_port, remote_host, remote_port):
    debug("Dynamic forwarding port started")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((local_host, local_port))
        server_socket.listen(5)
        while True:
            client_socket, address = server_socket.accept()
            debug(f"Client connected from {address}")
            client_handler = threading.Thread(target=dynamic_forward_port_handler, args=(client_socket, remote_host, remote_port))
            client_handler.start()
    except Exception as e:
        debug(f"Error in dynamic_forward_port: {e}")

def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("-L", "--local", help="specify local port to listen on")
    parser.add_argument("-R", "--remote", help="specify remote port to forward to")
    parser.add_argument("-D", "--dynamic", action="store_true", help="enable dynamic port forwarding")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug messages")
    parser.add_argument("-H", "--remote-host", help="specify remote host for dynamic port forwarding")
    parser.add_argument("-P", "--remote-port", help="specify remote port for dynamic port forwarding")
    args = parser.parse_args()
    if args.debug:
        DEBUG = True
    if args.local and args.remote:
        if int(args.local) < 0 or int(args.local) > 65535:
            print("Invalid local port")
            return
        if int(args.remote) < 0 or int(args.remote) > 65535:
            print("Invalid remote port")
            return
        forward_port("localhost", int(args.local), "localhost", int(args.remote))
    elif args.dynamic:
        if not args.remote_host or not args.remote_port:
            print("Remote host and port must be specified for dynamic port forwarding")
            return
        if int(args.remote_port) < 0 or int(args.remote_port) > 65535:
            print("Invalid remote port")
            return
        dynamic_forward_port("localhost", 8080, args.remote_host, int(args.remote_port))
    else:
        help()

if __name__ == "__main__":
    main()