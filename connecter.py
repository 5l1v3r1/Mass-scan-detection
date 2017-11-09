#!/usr/bin/python

import sys, os, socket, select, subprocess, smtplib, time, datetime

#if (len(sys.argv) < 3):
#    print("Usage: python connector.py <host> <port>")
#    sys.exit()

#host = sys.argv[1]
#port = int(sys.argv[2])

host = '127.0.0.1'
port = 3636

def time_full():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

def connector():
    server = socket.socket(socket.AF_INET)
    server.settimeout(1)

    try:
        server.connect((host, port))

        print('\033[1;92m[ OK ]\033[0m Connected!')
        os.system('clear')
        print '\n\t\t\033[1;92m[ WELCOME ]\033[0m Connected with ' + str(host) + ':' + str(port) + '\n\n'
        print """\033[1m
       \t\t              zz
       \t\t    ! _    zz           _____
       \t\t    |(~} zz         !  [13:37]
       \t\t    |(_/__________..| =========
       \t\t    |  ||:::::::::::|  |_____|\033[0m

       \t\t   \033[1;96mMass-scan Detection by IncSec\033[0m


Listening...
        """
        #sys.stdout.write('#?:$ '); sys.stdout.flush()
    except Exception as e:
        print("\033[1;91m[ ! ]\033[0m Unable to connect to %s on port %s" % (host, port))
        sys.exit()

    while True:
        socket_list = [sys.stdin, server]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == server:
                data = sock.recv(4096)
                if not data:
                    sys.stdout.write("\n\033[1;91m[ ! ]\033[0m Connection has ended\n")
                    sys.exit()
                # Do something when some data is present
                #elif 'random1random2random3random4' in data:
                    sys.stdout.write('\033[1m[' + time_full() + ']\033[0m ' + '\033[1;91m[ WARNING ]\033[0m Slowloris DDOS Vulnerbility Scan Detected!')
                    #sys.stdout.write('#?:$ '); sys.stdout.flush()
                #elif 'HTTP' in data:
                    #sys.stdout.write('\033[1;94m[ INFO ]\033[0m HTTP request recieved: %s' % data)
                #elif 'CONNECTED' in data:
                    sys.stdout.write(data)
                #elif 'DISCONNECTED' in data:
                    sys.stdout.write(data)
                else:
                    #sys.stdout.write('\033[92m' + data + '\033[0m')
                    print("%s" % data)
                    #sys.stdout.write('#?:$ '); sys.stdout.flush()

            #else:
            #    send_data = sys.stdin.readline()
                #s.send(msg)
                #sys.stdout.write('#?:$ '); sys.stdout.flush()

try:
    connector()
except KeyboardInterrupt:
    sys.stdout.write("\n\033[1;91m[ ! ]\033[0m Disconnected\n")
