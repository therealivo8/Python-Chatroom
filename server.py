import socket
import threading
from argparse import ArgumentParser, Namespace
import sys


# create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"
#port = 8007

parser = ArgumentParser()
#parser.add_argument('filename', help = 'filename of the program')
parser.add_argument('-start', action='store_true')
parser.add_argument('-port', type = int)
parser.add_argument('-passcode', type = str)


args: Namespace = parser.parse_args()

serverPasscode = args.passcode
port = args.port



# bind the socket to a specific address and port
server.bind((server_ip, port))
# listen for incoming connections
server.listen()
print(f"Server started on port {port}. Accepting connections")
sys.stdout.flush()

clients = []
usernames = []


# broadcast message to all clients
def broadcast(message): 
    for client in clients:
        client.send(message)

# handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except: # error while receiving message
            index = clients.index(client) # which client failed
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the chatroom".encode("ascii"))
            usernames.remove(username)
            break

def run_server():
    while True:
        client, address = server.accept() # server is accepting all of the connections
        print(f"Connected with {str(address)}")
        sys.stdout.flush()

        client.send("USER".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        usernames.append(username)
        clients.append(client)

        print(f"Username of the client is {username}")
        sys.stdout.flush()
        broadcast(f"{username} joined the chatroom".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print("Server is listening")
sys.stdout.flush()
run_server()


