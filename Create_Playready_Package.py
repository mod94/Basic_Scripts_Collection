#!/usr/bin/python
import os
import sys
import argparse
import subprocess
import shlex

''' INFO
 S0n = 16X9
 S5n = 4X3
 
 1: S01/S51 = Audio Only
 2: S02/S52 = 150k
 3: S03/S53 = 250k
 4: S04/S54 = 500k
 5: S05/S55 = 800k
 6: S06/S56 = 1000mbit
 7: S07/S57 = 1200mbit
 8: S09/S58 = 1500mbit

'''

LICENCE="/etc/usp.lic"
SOURCE_DIR_PATH = "/mnt/source_media/"
PACKAGED_PATH = "/mnt/output_package/"


class PackageRequest(object):
    def __init__(self):
        self._parse_options()
        self._check_source_files_exist()
        
    
    def _parse_options(self):
        parser = argparse.ArgumentParser(description="Playready Packaging Script.")
        parser.add_argument('--materialID', type=str, required=True)
        parser.add_argument('--source_dir', type=str, required=True)
        parser.add_argument('--output_dir', type=str, required=True)
        parser.add_argument('--renditions', nargs='+', type=str, required=True)
        parser.add_argument('--platform', type=str, required=True)
        parser.add_argument('--timescale', type=str, required=True)
        parser.add_argument('--fragment_duration', type=str, required=True)
        parser.add_argument('--kid', type=str, required=True)
        parser.add_argument('--encKey', type=str, required=False)
        parser.add_argument('--keySeed', type=str, required=False)
        parser.add_argument('--keyIV', type=str, required=False)
        parser.add_argument('--license_server_url', type=str, required=True)
        self.args = parser.parse_args()
        
    
    def _check_source_files_exist(self):
        tmpDir = ''.join(SOURCE_DIR_PATH + self.args.materialID)
        #print tmpDir
        if not os.path.exists(tmpDir):
            return False
        else:
            os.chdir(tmpDir)
            for _file in self.args.renditions:
                if os.path.isfile(''.join(tmpDir + "/" + _file)):
                   return True
                else:
                   print "File {0} Not Found?".format(_file)
                   return False
                   

    
    def _create_pr_package(self):
        cmd_list=[]
        working_dir=self.args.output_dir
        cmd_list.append(''.join("mkdir -p " + working_dir))
        
        mp4SPLIT= "mp4split --license-key {0} " \
                  "--timescale={1} --fragment_duration={2} " \
                  "--iss.key={3}:{4} --iss.license_server_url={5}".format(LICENCE,
                                                                          self.args.timescale,
                                                                          self.args.fragment_duration,
                                                                          self.args.kid,
                                                                          self.args.encKey,
                                                                          self.args.license_server_url
                                                                          )
        
        cmd_args = ''.join(" -o " + working_dir + self.args.materialID) 
        
        for rendition in self.args.renditions:
            _source = ''.join(self.args.source_dir + rendition)

            if "AudioRendition" in rendition:
                cmd_list.append(''.join(
                                        mp4SPLIT + cmd_args + "_AudioOnly.isma " + _source + " --track_id 2"
                                       )
                               )
            elif ("S04" in rendition) or ("S54" in rendition):
                cmd_list.append(''.join(
                                        mp4SPLIT + cmd_args + "_500.ismv " + _source + " --track_id 1"
                                       )
                               )
            elif ("S05" in rendition) or ("S55" in rendition):
                cmd_list.append(''.join(
                                        mp4SPLIT + cmd_args + "_800.ismv " + _source + " --track_id 1"
                                       )
                               )
            elif ("S06" in rendition) or ("S56" in rendition):
                cmd_list.append(''.join(
                                        mp4SPLIT + cmd_args + "_1000.ismv " + _source + " --track_id 1"
                                       )
                               )
            elif ("S07" in rendition) or ("S57" in rendition):
                cmd_list.append(''.join(
                                        mp4SPLIT + cmd_args + "_1200.ismv " + _source + " --track_id 1"
                                       )
                               )
            elif ("S09" in rendition) or ("S58" in rendition):
                cmd_list.append(''.join(
                                        mp4SPLIT + cmd_args + "_1500.ismv " + _source + " --track_id 1"
                                       )
                               )
        
        # build main manifest in correct order
        _manifest = ''.join(mp4SPLIT + cmd_args + ".ism " \
                            + working_dir + self.args.materialID + "_500.ismv " \
                            + working_dir + self.args.materialID + "_800.ismv " \
                            + working_dir + self.args.materialID + "_1000.ismv " \
                            + working_dir + self.args.materialID + "_1200.ismv " \
                            + working_dir + self.args.materialID + "_1500.ismv " \
                            + working_dir + self.args.materialID + "_AudioOnly.isma"
                            )
        
        cmd_list.append(_manifest)
        # add h264 codec setting to ismc
        _ismc_setting = ''.join(mp4SPLIT + cmd_args + ".ismc " + working_dir + self.args.materialID + ".ism?H264")
        cmd_list.append(_ismc_setting)
        
        changeAVCI = ''.join("sed -i \"s/AVC1/H264/\" " + working_dir + self.args.materialID + ".ism")
        cmd_list.append(changeAVCI)
        #start packaging
        self._start_packaging(cmd_list)
        
        
    
    def _start_packaging(self, pr_args):
         
        for cmd in pr_args:
            process = subprocess.Popen(shlex.split(cmd),
                                       shell=False,
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE)

            output, stderr = process.communicate()
            ret_code = process.wait()
            #print ret_code
            if(ret_code != 0):
                raise subprocess.CalledProcessError(returncode=ret_code, cmd=cmd)
                
            
    
    def _exit_program(self, msg):
        print msg
        sys.stdout.flush()
        exit(self._exit_code)
        
    
    
    def main(self):
        #Check the package exists on disk, else fail
        if self._check_source_files_exist() == False:
            self._exit_code = 1
            self._exit_program("ERROR: Package {0} Does not Exist!".format(self.args.materialID))
        else:
            #change to package dir as working path
            os.chdir(SOURCE_DIR_PATH)
            #create smooth package
            self._create_pr_package()
            print "PlayReady Package: {} Completed Successfully!".format(self.args.materialID)
            
        

def main():
    start_packaging = PackageRequest()
    start_packaging.main()
    

if __name__ == "__main__":
    main()
    

    
