import socket
import threading
from argparse import ArgumentParser, Namespace
import sys


# create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"

parser = ArgumentParser()
parser.add_argument('-start', action='store_true')
parser.add_argument('-port', type = int)
parser.add_argument('-passcode', type = str)

args: Namespace = parser.parse_args()

server_passcode = args.passcode
port = args.port

# bind the socket to a specific address and port
server.bind((server_ip, port))
# listen for incoming connections
server.listen()
print(f"Server started on port {port}. Accepting connections")
sys.stdout.flush()

clients = []
usernames = []

# broadcast message to all clients except for sender
def broadcast(message, client): 
    for a in clients:
        if (a != client):
            a.send(message)

# handle for client messages
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == ":Exit":
                index = clients.index(client) # which client failed
                broadcast(f"{username} left the chatroom".encode("utf-8"), client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                usernames.remove(username)
                break
            index = clients.index(client)
            name = usernames[index]
            broadcast(f"{message}".encode("utf-8"), client)
            print(f'{message}')
            sys.stdout.flush()
        except: # error while receiving message
            index = clients.index(client) # which client failed
            username = usernames[index]
            broadcast(f"{username} left the chatroom".encode("utf-8"), client)
            clients.remove(client)
            client.close()
            usernames.remove(username)
            break
            

def run_server():
    while True:
        client, address = server.accept() # server is accepting all of the connections
        client.send("PASS".encode("utf-8")) # Send PASS to client
        passcode = client.recv(1024).decode("utf-8") # receive the passcode from the client
        if passcode != server_passcode: # close connection if passcode is incorrect
            client.send("Incorrect passcode".encode("utf-8"))
            client.close()
            break
        client.send("USER".encode("utf-8"))
        username = client.recv(1024).decode("utf-8") #receive the username of client
        usernames.append(username)
        clients.append(client)

        print(f"{username} joined the chatroom")
        sys.stdout.flush()
        client.send(f"Connected to {server_ip} on port {port}".encode("utf-8"))
        broadcast(f"{username} joined the chatroom".encode("utf-8"), client)

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()
        
        
sys.stdout.flush()
run_server()


