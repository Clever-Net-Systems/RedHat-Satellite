#!/usr/bin/python
# coding: utf-8
################################################################################
#   Clever Net Systems [~]
#   Clément Hampaï <clement.hampai@clevernetsystems.com>
#   Hammer activation-key generation script
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
################################################################################

import commands

# Printing misc ----------------------------------------------------------------
def display_bash_result(bash_result):
    return_code = bash_result[0]
    message = bash_result[1]
    if return_code == 0:
        if message !="":
            print_success(message)
    else:
        if message !="":
            print_failure(message)

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

# Exec bash command ------------------------------------------------------------
def launch_bash_command(bash_command):
    print_message(bash_command)
    output = commands.getstatusoutput(str(bash_command))
    return output
#-------------------------------------------------------------------------------

content_views = ["rhel5_32", "rhel5_64", "rhel6", "rhel7"]
life_cycle_envs = [["Dev", 2], ["Test", 2], ["Prod", 3], ["Validated", 2]]
org_label = "My-org-name"
key_middle_name = "patching_linux"

def create_activation_key(content_views, life_cycle_envs, middle_name, org_label):
    for content_view in content_views:
        for life_cycle_env in life_cycle_envs:
            life_cycle_env_name = life_cycle_env[0]
            how_many_keys = life_cycle_env[1]
            for num in range(how_many_keys):
                ak_name = content_view+"_"+middle_name+"_"+life_cycle_env_name+"_0"+str(num)
                bash_command = "hammer activation-key create --organization "+str(org_label)+" --name "+str(ak_name)+" --content-view "+str(content_view)+" --lifecycle-environment "+life_cycle_env_name
                hammer_creation_return = launch_bash_command(bash_command)
                display_bash_result(hammer_creation_return)

create_activation_key(content_views, life_cycle_envs, key_middle_name, org_label)
