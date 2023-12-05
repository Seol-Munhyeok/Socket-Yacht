import socket
from _thread import *
import pickle

server = "172.18.1.107"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, Server started.")


def thread_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)
            conn.sendall(str.encode(reply))

        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    """ continuously look for connections """
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(thread_client, (conn,))

