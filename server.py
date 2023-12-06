import socket
import threading
from _thread import *

server = "192.168.124.155"
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, Server started.")

# 클라이언트의 연결 객체를 저장하는 딕셔너리
client_connections = {}

# 클라이언트의 데이터를 저장하는 딕셔너리
client_messages = {}

def thread_client(conn, addr):
    client_id = addr[0] + ":" + str(addr[1])
    client_connections[client_id] = conn
    client_messages[client_id] = ""

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
                # 데이터를 client_messages 딕셔너리에 저장
                client_messages[client_id] = reply
                print(client_messages)
                # 다른 클라이언트에게 데이터를 전달
                for other_id, other_conn in client_connections.items():
                    if other_id != client_id:
                        try:
                            other_conn.sendall(str.encode(reply))
                        except Exception as e:
                            print("Failed to send data to", other_id)
                            print(e)
        except Exception as e:
            print(e)
            break

    # 연결 종료 시 딕셔너리에서 해당 클라이언트 제거
    del client_connections[client_id]
    del client_messages[client_id]
    print("Lost connection")
    conn.close()

while True:
    """ continuously look for connections """
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(thread_client, (conn, addr))

