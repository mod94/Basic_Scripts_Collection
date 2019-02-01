from __future__ import print_function
import os
import sys
import passlib.hash

HASH="$apr1$GDBY7mKy$otQYfmnQX8zRGXW96Y6ff0"
PASS_FILE="/root/rockyou.txt"
SALT="test"
COUNT=0

with open(PASS_FILE) as passes:
    for passwd in passes:
        COUNT+=1
        passwd=passwd.rstrip()
        result = passlib.hash.apr_md5_crypt.encrypt(passwd, salt=SALT)
        print("Hashes Tested: {}".format(COUNT), end='\r')
        sys.stdout.flush()
        if result == HASH:
            print("Password Found: {}".format(passwd))
            break


print("DONE!")
