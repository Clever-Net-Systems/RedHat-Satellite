#!/usr/bin/python
# coding: utf-8
#########################################################################################
#   Clever Net Systems [~]                                                     		    
#   Clément Hampaï <clement.hampai@clevernetsystems.com>                       		    
#   Hammer csv import script        			               		                    
#											                                            
#	This program is free software: you can redistribute it and/or modify	   	        
#	    it under the terms of the GNU General Public License as published by   	        
#	    the Free Software Foundation, either version 3 of the License, or	   	        
#	    (at your option) any later version. 					                        
#											                                            
#	    This program is distributed in the hope that it will be useful,		            
#	    but WITHOUT ANY WARRANTY; without even the implied warranty of		            
#	    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   
#	    GNU General Public License for more details. 				                    
# 											                                            
#	    You should have received a copy of the GNU General Public License 	   	        
#	    along with this program.  If not, see <http://www.gnu.org/licenses/>.  	        
#########################################################################################

import argparse, csv, subprocess
from argparse import Namespace
import commands

# Args management --------------------------------------------------------------
def handle_args():
    parser = argparse.ArgumentParser(description='[~] Hammer csv import script')
    parser.add_argument('-f', '--function', nargs=1, choices=['host-collection', 'repositories'], help='what would you like to import in Sat6 ?',required=True)
    parser.add_argument('-c', '--csv-file', help='spacewalk export csv file path',required=True)
    parser.add_argument('-d', '--dry-run', help='display hammer commands without running them', action='store_true', required=False)
    args = parser.parse_args()
    return args
#-------------------------------------------------------------------------------

# Select the right import function ---------------------------------------------
def launch_function(args):
    if args.function != None and args.csv_file != None:
        function = args.function[0]
        csv_path = args.csv_file
        if function == "host-collection":
            import_host_collection(csv_path, args)
        if function == "repositories":
            import_repositories(csv_path, args)
#-------------------------------------------------------------------------------

# Import Host-collection in Satellite6 -----------------------------------------
def import_host_collection(csv_path, args):
    print_top_menu("Importing host-collection...")
    print_second_menu("file: "+csv_path)
    csv_content_array = read_csv_file(csv_path)
    for host_collection in csv_content_array:
    	host_collection_label = host_collection[1]
    	organization_id = host_collection[3]
    	tmp_args = Namespace(dry_run=False)
    	organization_label = get_organisation_by_id(organization_id, tmp_args)[2]
        bash_command = "hammer host-collection create --organization-label "+organization_label+" --name "+host_collection_label
        hammer_creation_return = launch_bash_command(bash_command, args)
        display_bash_result(hammer_creation_return)
#-------------------------------------------------------------------------------

# Import RPM repositories in Satellite6 ----------------------------------------
def import_repositories(csv_path, args):
    print_top_menu("Importing repositories...")
    print_second_menu("file: "+csv_path)
    csv_content_array = read_csv_file(csv_path)
    for repository in csv_content_array:
        repo_url = repository[5]
        repo_name = repository[3]
        repo_type = repository[4]
        prod_name = repository[2]
        organization_id = repository[0]
        bash_command = "hammer repository create --organization-id "+str(organization_id)+" --product \""+str(prod_name)+"\" --content-type "+str(repo_type)+" --publish-via-http true --url \""+str(repo_url)+"\" --name \""+str(repo_name)+"\""
        hammer_creation_return = launch_bash_command(bash_command, args)
        display_bash_result(hammer_creation_return)
#-------------------------------------------------------------------------------

# Get organization by id -------------------------------------------------------
def get_organisation_by_id(id, args):
    bash_command = "hammer organization list | grep ^"+id+"\  | sed 's~[[:blank:]]~~g'"
    return launch_bash_command(bash_command, args).split("|")
#-------------------------------------------------------------------------------

# Launch a bash command --------------------------------------------------------
def launch_bash_command(bash_command, args):
    if args.dry_run:
        print_message(bash_command)
        return (0 ,"")
    else:
        print_message(bash_command)
        output = commands.getstatusoutput(str(bash_command))
        return output
#-------------------------------------------------------------------------------

# Display bash command result in color -----------------------------------------
def display_bash_result(bash_result):
    return_code = bash_result[0]
    message = bash_result[1]
    if return_code == 0:
        if message !="":
            print_success(message)
    else:
        if message !="":
            print_failure(message)
#-------------------------------------------------------------------------------

# Read csv file content from path ----------------------------------------------
def read_csv_file(csv_path):
    csv_array = []
    with open(csv_path, 'rb') as csvfile:
        csv_content = csv.reader(csvfile)
        for line in csv_content:
            csv_array.append(line)
    csv_array.pop(0)
    return csv_array
#-------------------------------------------------------------------------------

# Printing misc ----------------------------------------------------------------
def print_success(message):
    print('             \x1b[0;32;40m' + str(message) + '\x1b[0m')

def print_failure(message):
    print('             \x1b[0;31;40m' + str(message) + '\x1b[0m')

def print_message(message):
    print('         \x1b[2;33;40m' + message + '\x1b[0m')

def print_top_menu(menu):
    print(' \x1b[0;36;40m[~] ' + menu + '\x1b[0m')

def print_second_menu(menu):
    print('     ' + menu)
#-------------------------------------------------------------------------------

# MAIN -------------------------------------------------------------------------
args = handle_args()
launch_function(args)
# ------------------------------------------------------------------------------
