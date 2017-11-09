#!/usr/bin/python
import sys, socket, select, time, datetime

HOST = ''
SOCKET_LIST = []
BLACKLIST = []
PORT = 3636

def time_full():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

def server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # add server socket object to the list of readable connections

    SOCKET_LIST.append(server_socket)

    print "Server started on port " + str(PORT)

    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                if not sock in BLACKLIST:
                    SOCKET_LIST.append(sockfd)
                    print("\033[1;94m[" + time_full() + "]\033[0m " + "\033[1;92m[ CONNECTED ]\033[0m \033[1mSOURCE:\033[0m %s (%s)" % addr)
                else:
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)
                    print("\033[1;94m[" + time_full() + "]\033[0m " + "\033[1;90m[ DENIED ]\033[0m \033[1mSOURCE:\033[0m %s (%s)" % addr)
                    continue

                broadcast(server_socket, sockfd, "\033[1;94m[" + time_full() + "]\033[0m " + "\033[1;92m[ CONNECTED ]\033[0m \033[1mSOURCE:\033[0m %s:%s" % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(4096)

                    if data:
                        # there is something in the socket
                        if 'random1random2random3random4' in data:
                            broadcast(server_socket, sock, "\r" + "\033[1;94m[" + time_full() + "]\033[0m " + str(sock.getpeername()) + ' ' + '\033[1;91m[ WARNING ]\033[0m Slowloris DDOS Vulnerbility Scan Detected!')
                            if sock in SOCKET_LIST:
                                SOCKET_LIST.remove(sock)
                            BLACKLIST.append(sock); print(BLACKLIST)
                            print("\033[1;94m[" + time_full() + "]\033[0m " + "\033[1;90m[ BLACKLISTED ]\033[0m \033[1mSOURCE:\033[0m %s (%s)" % addr)
                            #broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "\033[1;94m[" + time_full() + "]\033[0m " + "\033[1;91m[ DISCONNECTED ]\033[0m \033[1mSOURCE:\033[0m %s (%s)" % addr)
                # exception
                except:
                    broadcast(server_socket, sock, "\033[1;94m[" + time_full() + "]\033[0m " + "\033[1;91m[ DISCONNECTED ]\033[0m \033[1mSOURCE:\033[0m %s (%s)" % addr)
                    continue

    server_socket.close()

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":
    sys.exit(server())
