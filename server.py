import socket
import threading
import os

# creating socket
PORT = 65432

sock = socket.socket()
sock.bind(("", PORT))

# printing & writing to file server address info
print("Server was started on", socket.gethostbyname(socket.gethostname()), "port", PORT)
with open("/bhome/part3/03/vh48541/kotfind.oquendo.ru/www/index.html", "w") as file:
	file.write(socket.gethostbyname(socket.gethostname()) + ":" + str(PORT) + "\n")

# quit by command
def quit_func():
    while 1:
        try:
            input()
        except EOFError:
            for conn in clients:
                conn.close()
            os.abort()

quit_func_thread = threading.Thread(target=quit_func)
quit_func_thread.start()

# accepting clients
sock.listen(1024)
clients = []

def accept_clients():
    while 1:
        conn, addr = sock.accept()
        clients.append(conn)
        print(conn.getpeername()[0], ":", conn.getpeername()[1], " connected.", sep="")
accept_clients_thread = threading.Thread(target=accept_clients)
accept_clients_thread.start()

# listening messages
while 1:
    for conn in clients:
        data = conn.recv(1024)
        dataStr = data.decode("utf-8")

        # send data to others
        print(conn.getpeername()[0], ":", conn.getpeername()[1], "> ", dataStr, sep="")
        for connto in clients:
            connto.send((conn.getpeername()[0] + ":" + str(conn.getpeername()[1]) + "> " + dataStr).encode("utf-8"))

        # if client disconnected
        if not data:
            conn.close()
            clients.remove(conn)
