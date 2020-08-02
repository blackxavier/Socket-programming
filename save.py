#create a function to accept connection
#socket must be listening before a connection can be accepted
def socket_accept():
    #function for accepting data
    conn,address = s.accept()#returns to parameters an object and a list of the ip address and a port
    print("Connection established. " + "\n" + "IP is " +address[0] + "port number "+ str(address[1]))
    send_commands(conn)#this code is used to initiate a command
    conn.close()#closes the connection

#sending commands once connection is created
def send_commands(conn):#add the send command from the accept fucntion
    while True:#infinite loop statement
    #this statement is used to continiously send commaand to client computer
    #cls
        cmd = input()#this line takes input from me the sender
        if cmd =='qiut':#if i input 'quit' the prograam should
            conn.close()#close connection
            s.close()#close socket
            sys.exit()#and exit commaand prompt

        if len(str.encode(cmd)) > 0:#the command input must be more than 0
            conn.send(str.encode(cmd))#encodes the connection,this connection dosent send in string but bits
#the code below would be what we would get fro the user,encoded in chunks of 1024 bits and an encoding of ft-8

            client_response = str(conn.recv(1024),"utf-8")            
            print(client_response,end="")#then this code prints the recieved message and goes to the next line




#now create a function that calls all the functions
def main():
    create_socket()
    bind_socket()
    socket_accept()
#the send command function is not called because it is being called above in the send_command fucntion
main()               