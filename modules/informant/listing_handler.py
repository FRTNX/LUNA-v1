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


import requests
import datetime, time
import json
import uuid
import gc
from lxml import html
import rollbar
from colorama import Fore
from func_timeout import func_timeout, FunctionTimedOut
from func_timeout.StoppableThread import StoppableThread
from modules.persistence import db_handler as persistence
from modules.responses import *
from annoyances import *


output_prompt = '\n[' + Fore.LIGHTBLACK_EX + 'LUNA' + Fore.RESET + '] '

def H(*n):
    if not n:
        print(output_prompt, end='');
    else:
        print(n[0], end='')
    time.sleep(0.2)

def list_search_results(search_term):
    list_table(filter_key=search_term)


def list_table(table='intellience', filter_key=None):
    """Lists the contents of selected table."""
    logging.info(f'Running in target with tabel {table} and filter key {filter_key}')
    try:
        tag = table.replace(' ', '_')

        # todo: refactor implementation
        excluded_tags = ['random', 'archives']
        if not filter_key:
            if tag not in persistence.fetch_distinct_tags() and tag not in excluded_tags:
                H(); sprint(f'I currently have no explicit {table.title()} intel. Would you like me to extract some?')
                return
                # directive = input(user_input_tag).lower()
                # if directive == 'yes': # todo: read yes,no + alternatives from nlu (intents:affirm,negate)
                #     H(); sprint('Extracting.') # add alternative responses
                #     os.system('gnome-terminal -e "python functions/extractor/extractor.py \'%s\'"' % table)
                #     return
                # else:
                #     controlCentre(*[directive])
        
        H();
        if (table != 'random' and not filter_key):
            sprint(f'Listing {table.title()} related intel.')

        db_banners = ['db_banner3.py', 'db_banner3.py', 'db_banner3.py'] # for posterity: add other database banners here
        os.system('python3 ./resources/banners/%s' % random.choice(db_banners))

        logging.info('Compiling table.')
        start = time.time()

        if (table == 'archives'):
            titles = persistence.fetch_archive_list()
        else:
            if filter_key:
                titles = persistence.find_occurances(filter_key)
            else:
                titles = persistence.list_titles_by_tag(tag)

        temp, temp2 = prepare_listing(titles)
        end = time.time()
        temp.sort(); temp2.sort()
        logging.info('Finished loading %s database. latency is at %s seconds.' % (tag, str(end-start)))
        logging.debug('len(temp) = %s' % len(temp))
        logging.debug('len(temp2) = %s' % len(temp2))

        file_count = len(temp)+len(temp2)

        a_space = 40
        b_space = 40

        # Extra bit of code ensures neat presentation, overengineered, I admit.
        a_sequence = []
        b_sequence = []
        a = 0
        b = 1
        while (a < len(temp) and b < len(temp)):
            a_sequence.append(temp[a])
            b_sequence.append(temp[b])
            a += 3
            b += 3

        tri_release = []

        if len(temp) > 3:
            for i in temp:
                tri_release.append(i)
                if len(tri_release) == 3:
                    aSpace = a_space-len(tri_release[0])+2
                    bSpace = b_space-len(tri_release[1])+2
                    print("%s%s%s%s%s" % (tri_release[0], ' '* aSpace,
                                            tri_release[1], ' '* bSpace,
                                            tri_release[2]))
                    tri_release.clear()
                    time.sleep(0.01)
        else:
            if len(temp) == 2:
                aSpace = a_space-len(tri_release[0])+2
                print("%s%s%s" % (tri_release[0], ' '* aSpace,
                                    tri_release[1]))
            else:
                print(tri_release[0])

        if temp2 != []:
            print(beam)
            for title in temp2:
                print(title)
                time.sleep(0.01)
        print(beam + '%s distinct files' % str(file_count))
        return
    except KeyboardInterrupt as e:
        print(beam + '%s distinct files' % str(file_count))
        H(); sprint('Aborted.')
        return
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(str(e))
        H(); sprint('Mine is a troubled mind. Check the logs and console me.')
        return
    gc.collect()


def prepare_listing(titles):
    """confessional() helper function. 
    """
    temp = []
    temp2 = []

    for title in titles:
        if len(title) < 40:
            temp.append(title.strip().replace('\n', ''))
        else:
            temp2.append(title.strip().replace('\n', ''))

    return temp, temp2
