import pysftp
import sys
import os

local_directory = sys.argv[1]
remote_directory = sys.argv[2]
yt_username = sys.argv[3]
key_pass = sys.argv[4]

try:
    # open the connection
    srv = pysftp.Connection(host="SOME SFTP HOST", username=yt_username, port=19321, private_key="~/.ssh/blah_id_rsa", private_key_pass=key_pass)
    
    dirExists = srv.exists(remote_directory)
    
    if dirExists == False:
        srv.mkdir(remote_directory)
    
    files = [ f for f in os.listdir(local_directory) if os.path.isfile(os.path.join(local_directory,f)) ]
    srv.chdir(remote_directory)
    
    for f in files:
        fExists = srv.exists(f)
        source = str(local_directory + f)
        print fExists
        if fExists == False:
            srv.put(source)
        
    
    #Close the connection
    srv.close()
except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    sys.exit(0)


    #this is the production script!
