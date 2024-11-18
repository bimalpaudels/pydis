import socket
import threading

HOST = '127.0.0.1'
PORT = 6379


def connection():

    try:
        soc = socket.create_server((HOST, PORT), reuse_port=True, backlog=1)
        while True:
            conn, addr = soc.accept()
            conn.send("Connected to the server\r\n".encode('utf-8'))
            print("Connected to", addr)
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.daemon = True
            client_thread.start()

    except socket.error as msg:
        print("Error", msg)


def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data:
                continue
            if data.upper() == "PING":
                conn.send("PONG\r\n".encode('utf-8'))
            if data.upper() == "EXIT":
                break
            else:
                continue


def echo():
    pass


if __name__ == "__main__":
    connection()

# Bind to port -- Done
# Ping response -- Done
# Concurrent ping response -- Done
# Echo response -- Todo
# SET and GET -- Todo
