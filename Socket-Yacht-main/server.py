import socket
from _thread import *
import pickle

server = "192.168.124.184"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, Server started.")


def thread_client(conn, player):
    conn.send(pickle.dumps(player))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            player[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = player[0]
                else:
                    reply = player[1]

                print("Recieved: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    """ continuously look for connections """
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(thread_client, (conn, currentPlayer))
    currentPlayer += 1
