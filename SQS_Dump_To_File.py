#!/usr/bin/python
 
import sys
import boto3
import json
import uuid
import time
from optparse import OptionParser
 
# Get the service resource
sqs = boto3.resource('sqs')
 
parser = OptionParser()
parser.add_option("-p", "--profile", dest="profile", help="override the default AWS profile", metavar="PROFILE", default="default")
parser.add_option("-q", "--queue", dest="queue", help="queue name to dump from")
(options, args) = parser.parse_args()
 
sqs = boto3.session.Session(profile_name=options.profile).resource('sqs')
queue = sqs.get_queue_by_name(QueueName=options.queue)
 
while True:
    for message in queue.receive_messages():
        x = uuid.uuid4()
        file = "msg_{}.json".format(x)
 
        with open(file, 'w') as outfile:
             json.dump(message.body, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
 
        print "Dumped message to file {}".format(file)
        message.delete()
    time.sleep(1)
