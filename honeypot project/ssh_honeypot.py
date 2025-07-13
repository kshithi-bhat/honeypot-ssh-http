#doing this on windows rn ,  modified firewall rules to allow traffic to port 2223 remember to change it back later pls use "New-NetFirewallRule -DisplayName "SSH Honeypot" -Direction Inbound -LocalPort 2223 -Protocol TCP -Action Allow" to allow.

#libraries 
import logging 
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import threading
import time
#constants
logging_format = logging.Formatter('%(message)s') #how we want the messages to be formatted in the log file 
SSH_BANNER = "SSH-2.0-MySSHServer_1.0" #when an incoming connection or client is trying to connect over ssh protocol it sends back metadata(version,where its running) ab the ssh server

#host_key = 'server.key' #secret key,local file ONLY
host_key = paramiko.RSAKey(filename='server.key')

#loggers and logging files 


#naming the logger, get logger, there are multiple log levels
funnel_logger = logging.getLogger('FunnelLogger') #gonna capture username passwords an ip addresses
funnel_logger.setLevel(logging.INFO)
#setting the handler, set where we are going to log to(the file where logging will be there here the file is audits.log)
funnel_handler = RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler) #when ran an audit file is created.

#ones needed for capturing ip addresses, usernames and passwords  and another one is needed to capture the emulated shell(what commands the bots/hackers are using )during the honeypot session
creds_logger = logging.getLogger('CredsLogger') 
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)



#emulating shells
#create the emulating shells and setting up the ssh server w paramiko(library in python)
def emulated_shell(channel, client_ip): #channel - our way of communicating or sending dialogue messages or strings over the ssh connection, remote shell session
    channel.send(b"corporate-jumpbox2$ ") # $ - normal user permissions nothing elevated 
    command = b""   #everytime we send this we also need to be listening to be  receiving those commands , listening to user input 
    #trying to create a loop, going to loopthrough the shell env, whenever user enters exit connection is closed
    #what we want to do is basically append each of the char inputted into the shell as a cmd, when enter is hit the chars are put together to form a string and based of this string you can evaluate the logic 
    while True:
        char = channel.recv(1) #listening to user input 
        channel.send(char) #going to send it in char to remote terminal/input stream
        if not char:
            channel.close()

        command += char 
            #evaluate
        if char == b"\r": #whenever you press enter it valuates the following conditions ,carriage return character (moves cursor to new line)
            if command.strip() == b'exit': #leading and trailing whitespaces bytes removed, raw input no formatting
                response = b"\n Goodbye!\n"
                channel.close()
            elif command.strip() == b'pwd': #print working directory
                response = b"\n" + b"\\usr\\local" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            elif command.strip() == b'whoami':
                response = b"\n" + b"corpuser1" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            elif command.strip() == b'ls':
                response = b"\n" + b"jumpbox1.conf" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            elif command.strip() == b'cat jumpbox1.conf':
                response = b"\n" + b"Go to deeboodah.com." + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            else: # anything else being the input will just echo back to them
                response = b"\n" + bytes(command.strip()) + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')

            #repopulate our default dialogue box as well as listen to next command 
            channel.send(response)
            channel.send(b"corporate-jumpbox2$ ") #mimics a real corp jump server(hardened entry point users login here first then ssh their way into systems) fake shell prompt, $-non root shell
            command = b""  

    

#SSH server + socket 
#Paramiko- pure python implementation of SSHv2 protocol, provides both client server functionality 
#remote shell cmds and file transfering, C & Rust
# we will be using server implementation, lot of this is boilerplate (standardized, resusable ) 

class Server(paramiko.ServerInterface): #setup ssh connection 

    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event() #open the initial function because we are adding a threading capabilty, calc or create a new event
        self.client_ip = client_ip #assigning to local variables
        self.input_username = input_username
        self.input_password = input_password


    #function: channel type
    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == 'session': #if channel type is session then we can open the connection up
           return paramiko.OPEN_SUCCEEDED
        else:
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    #authentication
    def get_allowed_auths(self, username):
        return "password"
    

    
    def check_auth_password(self, username, password):
        #starting off with logging user name and password supplied by the bots/ta.
        funnel_logger.info(f'Client {self.client_ip} attempted connection with ' + f'username: {username},' + f'password: {password}')
        creds_logger.info(f'{self.client_ip}, {username}, {password}')
        #custom user name and password wont be hardcoding it, hardcode -> only that usrname and pswd will be accepted rest rejected 
        #as u can see in init default is None so anything would return successful
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL


            
    
    def check_channel_shell_request(self, channel): #callback/handler method that gets called when ssh client req a session
        self.event.set() # threading event , set: req accepted proceed!
        return True #allow shell session

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        command = str(command) #handle the commands that are being input
        return True

# allow server to bind to a certain port & address allowing clients to come and connect to our server 
#maintain the connection
def client_handle(client, addr, username, password): #socket method/construct thatll pass the ip address for us
    client_ip = addr[0]
    print(f"{client_ip} has connected to the server.")


    try:
        
        #initialize a new transport object, handling low level ssh session 
        transport = paramiko.Transport(client) #pass client connection in the object
        transport.local_version = SSH_BANNER #set banner version for the transport object, custom banner is a constant
        #lets create instance of the server
        server = Server(client_ip=client_ip, input_username=username, input_password=password)
        #pass in the ssh session into the server class
        transport.add_server_key(host_key) #supply a host key its a public pvt key pair, allows clients to verify the if the server is who they claim to be, we will gen our own key pair using ssh key gen
            #ssh-keygen -t rsa -b 2048 -f server.key, no passphrase
            # Your identification has been saved in server.key
            #Your public key has been saved in server.key.pub can be made public

        transport.start_server(server=server)

        channel = transport.accept(100) 
        #channel = transport.accept(5000)
        # print("Channel accepted:", channel)#waits for the client  to open a channel, shell, system req, commandline exec, gives 100ms for the client to req the channel
        #is channel opens successfully its going to return a  bidirectional tunnel for comms
        if channel is None: #if connection est failed
            print("No channel was opened")

        #send another ssh banner ,gets  printed  onto the screen when you attempt to ssh into the server/honeypot file 

        standard_banner = "Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-94-generic x86_64)\r\n\r\n" #a welcome message 
        channel.send(standard_banner) #send the banner to the channel and then send an instance of the emulated shell which will no allow us to capture the incoming commands 
        emulated_shell(channel, client_ip=client_ip)


    except Exception as error:
        print(error) #this will print the error basically capture what has gone wrong if the try block hasnt been effectively executed  
        print("!! Error !!")
        
    finally:
        try:
            transport.close()
        except Exception as error:
            print(error)
            print("!!! Error !!!") # obviously needs a better exception handling in a real world production env 
        client.close()

    #now we need to create a way for our server to listen on an ip address and bind to a specific port 
    # we have a client handle but how do we actually get all the info from the client handle to an IP address port
    # we will be using sockets: will listen on specific ip and port , once socket has been opened and the client is attempting to connect then we can pass in the client handle which will send in that info( such as transport object which is the SSH session handling that channel making sure webare adding in host key and starting the SSH server)


#provision ssh-based honeypot

#this is going to be the main function that we are gonna be interfacing from 
#when you want to deploy the SSH honeypot we are gonna call this instance
def honeypot(address, port, username, password):


    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: says that the address is ipv4, socket lib and socket method, socket.SOCK_STREAM establishes that we will be listening using the TCP port (its a connection port and is stateful)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #1 enables these 2 options
    socks.bind((address, port))

    socks.listen(100) #how many connections can we handle, setting hard limit as 100, > wait or refuse
    print(f"SSH server is listening on port {port}.")

    #build logic, listen on ip&port -> accept new connection -> hand the connection off to client handle 
    while True:
        try:     # gather client ip address and port 
            client, addr = socks.accept() #implement threading, start a new thread, we want to handle concurrent connections making sure our server isnt locked in one session at a time using standard threading python lib  
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password)) #create new thread , have target as client handle and client handle takes in specific args
            ssh_honeypot_thread.start() #start new thread
        except Exception as error:
            print("!!! Exception - Could not open new client connection !!!")
            print(error)



#honeypot('127.0.0.1', 2223, 'username', 'password')      # loopback address, if comp is listeneing to ssh its better to use a higher port, if you want specific credentials then specify it if you want any login to be successful set them to none
honeypot('127.0.0.1', 2223, username=None, password=None)     
