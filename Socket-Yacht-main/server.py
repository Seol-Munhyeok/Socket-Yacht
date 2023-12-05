import socket
import threading
from _thread import *

server = "192.168.124.145"
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, Server started.")

# 클라이언트 간의 데이터를 저장하는 딕셔너리
client_data = {}


def thread_client(conn, addr):
    # 클라이언트 식별자를 생성
    client_id = addr[0] + ":" + str(addr[1])
    client_data[client_id] = conn  # Store the connection, not an empty string

    conn.send(str.encode("Connected"))
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                # 받은 데이터를 저장
                try:
                    client_data[client_id] = reply
                except:
                    print("충돌")
                # 다른 클라이언트에게 데이터를 전달
                for other_id, other_conn in client_data.items():
                    if other_id != client_id:
                        try:
                            other_conn.sendall(str.encode(reply))
                        except e:
                            # Handle potential exceptions when sending data to other clients
                            print("Failed to send data to", other_id)
                            print(e)
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    """ continuously look for connections """
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(thread_client, (conn, addr))

