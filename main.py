import socket
import threading

HOST = '127.0.0.1'
PORT = 6379

# In-memory data store for key-value pairs
data_store = {}


def connection():

    try:
        soc = socket.create_server((HOST, PORT), reuse_port=True, backlog=1)
        while True:
            conn, addr = soc.accept()
            print("Connected to", addr)
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.daemon = True
            client_thread.start()

    except socket.error as msg:
        print("Error", msg)


def handle_client(conn):
    with conn:
        conn.send(b'+OK\r\n')
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                lines = data.split(b'\r\n')

                if lines[0].startswith(b'*'):
                    # This is an array. First element is the command followed by arguments.
                    no_of_elems = int(lines[0][1:])
                    elems = []
                    index = 1
                    for _ in range(no_of_elems):
                        if lines[index].startswith(b'$'):
                            elems.append(lines[index + 1])
                            index += 2
                        else:
                            return ValueError("Something went wrong")
                    if elems[0].decode('ascii').lower() == 'ping':
                        conn.send(b'+PONG\r\n')
                    elif elems[0].decode('ascii').lower() == 'echo':
                        if len(elems) == 2:
                            echo_message = elems[1].decode('ascii')
                            conn.send(f'+{echo_message}\r\n'.encode('ascii'))
                        else:
                            conn.send(b'-ERR wrong number of arguments for echo command\r\n')
                    elif elems[0].decode('ascii').lower() == 'set':
                        if len(elems) == 3:
                            key = elems[1].decode('ascii')
                            value = elems[2].decode('ascii')
                            data_store[key] = value
                            conn.send(b'+OK\r\n')
                        else:
                            conn.send(b'-ERR wrong number of arguments for set command\r\n')
                    elif elems[0].decode('ascii').lower() == 'get':
                        if len(elems) == 2:
                            key = elems[1].decode('ascii')
                            value = data_store.get(key)
                            if value is not None:
                                conn.send(f'+{value}\r\n'.encode('ascii'))
                            else:
                                conn.send(b'$-1\r\n')  # Redis nil response
                        else:
                            conn.send(b'-ERR wrong number of arguments for get command\r\n')
                    else:
                        continue
                else:
                    continue
            except ValueError:
                conn.send(b'-ERR invalid request\r\n')
            except ConnectionResetError:
                print("Connection reset by peer")


if __name__ == "__main__":
    connection()

# Bind to port -- Done
# Ping response -- Done
# Concurrent ping response -- Done
# Echo response -- Done
# SET and GET -- Done
