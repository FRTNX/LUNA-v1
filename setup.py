##################################################################################################

###########
###########
###########
###########
###########
###########                   ########            ##########################                     ######
###########                   ########            ###########################                   ########
###########                   ########            ############################                 ##########
###########                   ########            #######           ###########               ############
###########                   ########            #######           ###########              #####    #####
###########                                       #######           ###########             #####      #####
###########                   ########            #######           ###########            #######    #######
###########                   ########            #######           ###########           ####################
###########                                       #######           ###########          ######################
###########                   ########            #######           ###########         ########################
###########                   ########            #######           ###########        ########          ########
###########                   ########            #######           ###########       ########            ########
###########                   ########            #######           ###########      ########              ########
###########                   ########            #######           ###########     ########                #######
#####################         ########            #######           ###########    ########                  ######
#############################  ########           #######           ###########   ########                    #####
############################### ########          #######           ###########  ########                      ####
##############################   ################ #######           ###########    #####                        ###
#############################     ###############    ####           ############ ######                          ##
#############################       ################ ####            ########### ##########                 #######


##################################################################################################


# Greetings.

#     Copyright (c) FRTNX [Busani P. Ndlovu]

# All rights reserved under the 3-clause BSD License:

#  Redistribution and use in source and binary forms, with or without modification, are permitted
#  provided that the following conditions are met:

#   * Redistributions of source code must retain the above copyright notice, this list of conditions
#     and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice, this list of
#     conditions and the following disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name FRTNX nor Busani P. Ndlovu nor any other moniker nor the names of any present
#     or future contributors may be used to endorse or promote products derived from this software
#     without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CONTINUUM ANALYTICS, INC. BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import getpass
import os
import subprocess
import logging
# from annoyances import rootLogger


def launcher():
    cwd = os.getcwd()
    conf = ['#!/bin/sh\n\n',
            '',
            'chmod +x luna.sh\n',
            'export EMAILPWD="OCO-2"\n',
            'export MYEMAIL="SHIZUKU"\n',
            'export LUNADDR="Aqua"\n',
            'export SHADOW="CALIPSO"\n',
            'export PRIUSER="Aura"\n',
            'git stash\n',
            'git pull >> ./logs/luna.log\n',
            './luna.sh "$@"\n',]
    conf[1] = 'cd %s\n' % cwd
    if not os.path.isdir("/usr/local/bin/"):
        os.makedirs("/usr/local/bin/")
    filewrite = open("luna", "w")
    filewrite.write(''.join(conf))
    filewrite.close()
    os.system('sudo mv luna /usr/local/bin/luna')
    subprocess.Popen("sudo chmod +x /usr/local/bin/luna", shell=True).wait()
    logging.info('successfully created launcher.')

launcher()
os.system('bash install_dependencies.sh')
os.system('make train-nlu')
os.system('luna')
"""
def pwd_manager():
    print('Enter the password for the email you created for the program ')
    emailpwd = getpass.getpass()
    print('Confirm password')
    emailpwd2 = getpass.getpass()
    if emailpwd == emailpwd2:
        return emailpwd
    else:
    	print('Passwords dont match. Try again.')
    	pwd_manager()

print('Welcome to the Luna setup wizard.\nBefore continuing please make to have created'+
	  ' a new gmail account and allowed access from less secure apps.'+
	  '\nNOTE:This is a crucial step so please make sure to get it right.\nNOTE:Mess this up and you may need to'+
	  ' do a complete reinstallation. No pressure.')
response = input("Enter 'yes' if you have completed this step. Enter 'no' to exit the setup wizard.\n[yes/no]: ")
if 'yes' in response.lower():
    try:
        primary_user = input('Choose a code name: ')
        email = input('Give the program the gmail account you created for it: ')
        pwd = pwd_manager()
        user_mail = input('Enter an email address you would like to recieve emails from the program from.\nyour email: ')
        print('code name: %s\nemail: %s\npassword: %s' % (primary_user, email, pwd))
        try:
            os.system('mkdir .access')
        except:
        	pass
        file = open('.access/keys', 'w')
        data = ['#!/bin/sh\n\nexport EMAILPWD="%s"\nexport MYEMAIL="%s"\nexport LUNADDR="%s"\nexport SHADOW="%s"\nexport PRIUSER="%s"\n' % (pwd, user_mail, email, pwd, primary_user)]
        print(data[0])
        file.write(data[0])
        file.close()
        print('Settings saved.')

    except Exception as e:
        print(str(e))
else:
	os.system('exit')
"""
