import os, sys
import xml.dom
from xml.dom import minidom
'''
Produces a formatted list of 
Environment ie prod/uat
Workflow GUID
Workflow Name

Usage guide:
1: Open telestream vantage workflow designer
2: Select File -> Export Workflows by Category
3: Select the Prod and UAT workflow headers only, deselecting non required groups
4: Select OK to export the workflows
5: Copy the copy the folders to a system running python (if your awesome then all your systems will be :)
6: Update the paths section below with the correct uat/prod directory paths
7: run the script: python /Path_to/GetVantageWorkflowIDS.py

This iterates each of the workflow xmls and pulls out the name and identifier, this is useful for keeping the 
orchestrator lookup tables in sync.

@Author: Sbridgens
'''


paths  = ["/Users/username/Documents/Production_Workflows", "/Users/username/Documents/UAT_Workflows"]

print "\nEnvironment\t\tWorkflow GUID\t\t    Workflow Name"

def process_workflows(environment, file):
    xmldoc = minidom.parse(file)
    xtag = xmldoc.getElementsByTagName("soa:Procedure")
    output_string = ""
    for element in xtag:
        for elem in element.attributes.values():
            if elem.name == "identifier":
                output_string = ''.join(environment + " - " + str(elem.firstChild.data))
            if elem.name == "name":
                output_string += ''.join( " : " + str(elem.firstChild.data))
    return output_string

print

for current_dir in paths:
    os.chdir(current_dir)
    env = ""
    if "Production" in current_dir:
        env = "Production"
    else:
        print
        env = "UAT"
    files = os.listdir(current_dir)
    for file in files:
        print process_workflows(env, file)

output_string = ""

print
