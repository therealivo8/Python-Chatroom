import socket
import threading
import sys
from argparse import ArgumentParser, Namespace

parser = ArgumentParser()
#parser.add_argument('filename', help = 'filename of the program')
parser.add_argument('-join', action='store_true')
parser.add_argument('-host', type = str)
parser.add_argument('-port', type = int)
parser.add_argument('-username', type = str)
parser.add_argument('-passcode', type = str)

args: Namespace = parser.parse_args()

host = args.host
passcode = args.passcode
port = args.port
username = args.username

#start
#username = input("Choose a username:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", port))
def run_server():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "USER":
                client.send(username.encode("ascii"))
            else:
                print(message)
            
        except:
            print("An error occurred")
            sys.stdout.flush()
            client.close()
            break

def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=run_server)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()