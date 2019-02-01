import sys
import socket
import time

target_addr = "ip to fuzz"
target_port = "its port"
lengths = [127,128,129,255,256,257,511,512,513,1023,1024,1025,2047,2048,2049,4095,4096,4097,8192,8193,16384,16385,32768,32769,65536,65537,131072,131073]

for length in lengths:
    fuzz = "A" * length #set fuzz to a different length of 'A's each loop
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a TCP socket
    sock.connect((target_addr, target_port))
    
    
