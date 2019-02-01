#!/usr/local/bin/python2.7
import os
import boto3
import sys

s3bucket='SomeBucket'
s3basekey='SomeKey'
s3asset=sys.argv[1]

def Download_From_S3():
    try:
        session = boto3.Session(profile_name='s3prod')
        dl_client = session.client('s3')
            
        print("[+] Attempting download of s3 media file")
            
        dl_client.download_file(Bucket=s3bucket, 
                                Key=''.join(s3basekey + s3asset), 
                                Filename=s3asset)
        print("[+] Successfully downloaded s3 media file: %s" % s3asset)
        return "Success"
    except Exception as ds3_ex:
        print("[-] Error Downloading media from S3, Error message: {0}".format(ds3_ex))



Download_From_S3()
