#!/bin/bash
# author=sbridgens
# common file/dir lists
# http://blog.thireus.com/web-common-directories-and-filenames-word-lists-collection/
# usernames found in /etc/passwd

# local username array
declare -a arr=("d.trump" "paul.ross" "a.jones" "simon.gray" "lulz.sec" "an.onymous" "d.trump.douche")
wordlist="/tmp/commonnames.txt"
ckdir="/data/users"
## now loop through the above array
for u in "${arr[@]}"
do
   cat $wordlist | while read line
   do
       if [ -d "$ckdir/$u/$line" ]; then
           printf "[+] Directory $ckdir/$u/$line exists!\n"
           cat $wordlist | while read fname
           do
                if [ -f "$ckdir/$u/$line/$fname.txt" ]; then
                    printf "[+] FILE: $ckdir/$u/$line/$fname.txt exists\n"
                elif [ -f "$ckdir/$u/$line/$fname" ]; then
                    printf "[+] FILE: $ckdir/$u/$line/$fname exists\n"
                fi
           done
       fi
   done
done
