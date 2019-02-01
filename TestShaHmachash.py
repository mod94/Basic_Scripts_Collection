import hashlib
import argparse
import sys
import Crypto
import hmac


counter = 1
hcounter = 1
str_output = ""
hmac_out = ""

inputWord = str(sys.argv)

hash_object = hashlib.sha256(b''.join(inputWord))
hex_dig = hash_object.hexdigest()


#for loop to seperate hex_dig
for c in hex_dig:
    if counter != 5:
        str_output += c
        counter +=1
    elif counter >= 5:
        str_output += c + " "
        counter = 1
        
def hmac_sha256(key, msg):
    hash_obj = hmac.new(key, msg, hashlib.sha256)
    return hash_obj.hexdigest()

hd = hmac_sha256('titan',inputWord)
#for loop for hmac
for h in hd:
    if hcounter != 5:
        hmac_out += h
        hcounter +=1
    elif hcounter >= 5:
        hmac_out += h + " "
        hcounter = 1


print "original:\n86B46 47350 B0A7C 50C68 079A0 65A89 29Cf7 03582 EEf91 BA6BF 11092 B6B03 2BD4"

print "hmac:\n" + hmac_out.upper()

print "sha256:\n" + str_output.upper()
