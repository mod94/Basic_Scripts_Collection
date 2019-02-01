#!/usr/bin/env python

import logging
import subprocess
import xmltodict
import shlex
from threading import Thread
from urlparse import urlparse, parse_qs
import requests
from optparse import OptionParser

logging.root.handlers = []
logging.basicConfig(format='%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def parse_manifest(url):
    response = requests.get(url)
    response.raise_for_status()
    LOGGER.info("Fetched {}".format( response.url ) )
    tree =  xmltodict.parse( response.text )
    #LOGGER.info("tree {}".format( tree ))
    return tree

#def construct_media_url(
   

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", help="URL to live origin", metavar="Origin")
(options, args) = parser.parse_args()

url = options.url
LOGGER.info("Scanning smooth stream....")
LOGGER.info("URL : {}".format(url))
manifest = parse_manifest(url)

master_url = urlparse(url)
path_parts = filter(len,master_url.path.split("/")[0:-1])
base_url = "{}://{}/{}".format( master_url.scheme,
                                master_url.netloc,
                                "/".join( path_parts ) )

LOGGER.info("Base URL {}".format( base_url ) )
 
for stream in manifest['SmoothStreamingMedia']['StreamIndex']:
    #LOGGER.info("Stream {}".format( stream ) )
    media_base_url = "{}/{}".format(base_url, stream['@Url'] )
    LOGGER.info("Media Url : {}".format(media_base_url) )

    bitrates = []
    if type( stream['QualityLevel'] ) is not list:
        LOGGER.info(" QL {} ".format( stream['QualityLevel'] ) )
        bitrates.append( stream['QualityLevel']['@Bitrate'] )
    else:
        for ql in stream['QualityLevel']:
            bitrates.append( ql['@Bitrate'] )

    LOGGER.info("Got bitrates {}".format( bitrates ) )

    for bitrate in bitrates:
        # Grab the start time from the first chunk
        if '@t' in stream['c'][0]:
            time_offset = int ( stream['c'][0]['@t'] )
        else:
            time_offset = 0

        for chunk in stream['c'][:-1]:
            time_offset += int ( chunk['@d'] ) 
            fragment_url = media_base_url.replace('{bitrate}',bitrate)
            fragment_url = fragment_url.replace('{start time}', str(time_offset) )
            LOGGER.info("Stream URL : {}".format( fragment_url) )
            response = requests.get(fragment_url)
            response.raise_for_status()
