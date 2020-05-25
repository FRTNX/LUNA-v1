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


import os
import sys
import getopt
import random
import time
import uuid
import json
import wikipedia
import psycopg2.extras
import psycopg2.errors
from func_timeout.StoppableThread import StoppableThread
from colorama import Fore
from persistence import index as persistence

READ_ONLY_TABLES = ['texts', 'intelligence', 'archive', 'session_data', 'users', 'weather_location_default']

beam = '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

def extract_interests(interests, prev_state=[0,0], current_state=[0,0], homogeneous_states=0, init_call=True):
    print(f'[+] Homogeneous states: {homogeneous_states}')
    try:
        if (homogeneous_states > 10):
            print(f'[+] {beam}')
            print('[*] Detected state cluster. Terminating extraction.')
            return # return only when len(interests) == 0;

        for interest in interests:
            temp_db = interest.lower().replace(' ', '_').replace('-', '_')
            if (temp_db not in READ_ONLY_TABLES):
                if init_call:
                    persistence.create_database(temp_db)
                    persistence.extract_and_insert_initial(temp_db, interest)
                extraction_count, source_count = persistence.prepare_listing(temp_db)
                persistence.parallel_extraction(temp_db)

        prev_state = current_state
        current_state = [extraction_count, source_count]
        print(f'[+] New state: {current_state}, Previous state: {prev_state}')

        if (prev_state != current_state):
            homogeneous_states = 0
            extract_interests(interests, prev_state, current_state, homogeneous_states, False)
        else:
            # remove interest from interests when complete. terminate when len(interests) == 0
            homogeneous_states += 1
            extract_interests(interests, prev_state, current_state, homogeneous_states, False)

    except Exception as e:
        raise RuntimeError(e)


def consolidate_and_clean(interests):
    print('[+] Consolidating tables')
    persistence.consolidate_dbs(interests)
    print('[+] Tables consolidated')
    print('[+] Cleaning up temporary tables')
    persistence.cleanup(interests)
    print('[+] Cleanup complete')


def termination_message():
    print('[+] Extraction complete')
    print(f'[+] {beam}')


# todo: assign different color to each topic in log output
if True:
    args = sys.argv
    interests = args[1:]
    print(f'[+] Received extraction list: {interests}')

    try:
        persistence.load_state()
        extract_interests(interests)
        consolidate_and_clean(interests)
        termination_message()
    except KeyboardInterrupt:
        print('[+] Process terminated by user.')
        consolidate_and_clean(interests)
        termination_message()
    except Exception as e:
        print('[-] ' + Fore.RED + 'FATAL' + Fore.RESET + f': {e}')
        consolidate_and_clean(interests)

    time.sleep(60)
