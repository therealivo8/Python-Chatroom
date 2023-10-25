import socket
import threading
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime

#pass the in the command line arguments
parser = ArgumentParser()
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
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", port))
def run_server():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "Incorrect passcode":
                print(message)
                sys.stdout.flush()
                client.close()
                break
            elif message == "PASS":
                client.send(passcode.encode("utf-8"))
            elif message == "USER":
                client.send(username.encode("utf-8"))
            else:
                print(message)
                sys.stdout.flush()     
        except:
            client.close()
            break

#Handles the inputs from clients
def write():
    while True:
        try:
            message_in = f'{input("")}'
            if message_in == ":Exit":
                client.send(f':Exit'.encode("utf-8"))
                client.close()
                break
            elif message_in == ":(":
                client.send(f'{username}: [feeling sad]'.encode("utf-8"))
            elif message_in == ":)":
                client.send(f'{username}: [feeling happy]'.encode("utf-8"))
            elif message_in == ":mytime":
                today = datetime.today()
                date_time = today.strftime("%c")
                client.send(f'{username}: {date_time}'.encode("utf-8"))
                print(":mytime")
                sys.stdout.flush()
            elif message_in == ":+1hr":
                today = datetime.today()
                next_hour = today.replace(hour = today.hour + 1)
                date_time = next_hour.strftime("%c")
                client.send(f'{username}: {date_time}'.encode("utf-8"))
                print(":+1hr")
                sys.stdout.flush()
            else:
                message = f'{username}: {message_in}'
                client.send(message.encode("utf-8"))
        except:
            client.close()
            break


receive_thread = threading.Thread(target=run_server)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()