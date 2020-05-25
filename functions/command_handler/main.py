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


from annoyances import *

import os
import aiml
import inflect
import rollbar
from func_timeout.StoppableThread import StoppableThread
import random
import wolframalpha
# from personality import *
from colorama import Fore, Style
from functions.responses import *
from persistence import index as persistence
from functions.utils import main as utils
from functions.informant import listing_handler
from functions.informant import nc_handler
from functions.onboarding import main as onboarding
from functions.display_manager.main import output_prompt as H
from functions.display_manager import main as display_manager
from functions.data_management import main as data_manager

client = wolframalpha.Client(os.getenv('WOLFRAM'))

num_word_transform = inflect.engine()

kernel = aiml.Kernel()
spine = './brain/'

try:
    brn = os.listdir(spine)
    kernel.loadBrain(spine + brn[0])
except Exception as e:
    rollbar.report_exc_info()
    logging.error(e)
    logging.error("I'm brainless.")

load_character = StoppableThread(target=utils.character_loader, args=(kernel,))
load_character.daemon = True
load_character.start()

coords = StoppableThread(target=utils.get_coords)
coords.daemon = True
coords.start()

def resolveListOrDict(variable):                           
    if isinstance(variable, list):             
        return variable[0]['plaintext']                                                                  
    else:                                    
        return variable['plaintext']

def search_wolfram(command):                                       
    res = client.query(command)                   
    if res['@success'] == 'false':           
        H(); sprint(kernel.respond(command))
        result = persistence.insert_session_data(command)
        logging.info(result)             
    else:                                                                   
        result = ''              
        pod0 = res['pod'][0]                                  
        pod1 = res['pod'][1]                            
        if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):                        
            result = resolveListOrDict(pod1['subpod']) 
            H(); sprint(result.replace('\n', ' '))
            return  
        else:                     
            H(); sprint(kernel.respond(command))
            result = persistence.insert_session_data(command)
            logging.info(result)
            return

def wolfram(init=True):
    if init:
        H(); sprint('Game face activated')

    command = display_manager.input_prompt()
    if command.lower() != 'exit':
        search_wolfram(command)
        wolfram(False)
    else:
        H(); sprint('Normal operations resumed')

    return

# todo: result should be object with boolean property 'success' and string property 'message'
def handle_persistence_response(result, void=False):
    logging.debug(result)
    if not void:
        if (result.startswith('Success')):
            H(); sprint('Done.')
        else:
            H(); sprint('Negative contact. Check the logs.')
    return

def command_handler(user_input):
    kernel.setPredicate("name", os.environ['LUNA_USER'])

    command = user_input.lower()
    
    try:
        if command == 'lets be serious':
            wolfram()

        if command == 'help':
            utils.help_center()

        elif (command.startswith('what is the distance between ') or command.startswith('distance between')):
            end = command.find(' and ')
            start = command.find(' between ')
            x = command[start + 9 : end]
            y = command[end + 5 : ]
            utils.groundDistance(x,y)
            return

        elif 'resource' in command:
            utils.find_external_resource()
            return

        elif command == 'newscatcher' or command == 'nc':
            nc_handler.main()
            return

        elif command == 'search quotes':
            # display_manager.quote_search()
            return

        elif command.lower().strip().startswith('search '):
            listing_handler.list_search_results(command[7:])

        elif command.lower() == 'insert quote':
            result = data_manager.insert_quote_from_user()
            handle_persistence_response(result, True)
            return

        elif command == 'reading list':
            listing_handler.list_table('random')
            return

        elif command == 'latency':
            render_latency_chart = StoppableThread(target=utils.latency)
            render_latency_chart.daemon = True
            render_latency_chart.start()
            return

        elif command == 'clear':
            os.system('clear')
            return

        elif command.startswith('extract '):
            extraction_list = command[8:]
            targets = extraction_list.split(',')
            formatted_parameters = ''
            for target in targets:
                formatted_parameters += f"'{target.strip()}' "
            os.system(f'gnome-terminal -e "python functions/extractor/extractor.py {formatted_parameters}"')
            return

        # todo: run without tagging. Also find a way to remove entries from text file after extraction.
        # elif command.lower() == 'run passive extraction':
        #     targets = utils.fetch_passive_extraction_list()
        #     os.system(f'gnome-terminal -e "python functions/extractor/extractor.py {targets}"')
        #     return            

        elif command.startswith('play me some '):
            utils.media_player(command[13:])
            return

        elif command == 'data stats':
            H(); sprint('Listing database item counts\n')
            sprint('| ' + f'{ Style.BRIGHT + Fore.YELLOW + "INTEL" + Fore.RESET + Style.RESET_ALL + " (Total: " + str(persistence.get_db_count("intelligence")) + ")"  }')
            tags = persistence.fetch_distinct_tags()
            space = len(sorted(tags, key=len)[-1]) + 10
            for tag in sorted(tags):
                count = persistence.tag_count(tag)[0]
                if count > 1 and tag != 'intelligence':
                    print('  - %s%s: %s' % (tag.title().replace('_', ' '), (' ' * (space - len(tag))), count))
            sprint('| ' + f'{ Style.BRIGHT + Fore.YELLOW + "FILES"  + Fore.RESET + Style.RESET_ALL + " (Total: " + str(persistence.get_db_count("texts")) + ")" }')
            sprint('| ' + f'{ Style.BRIGHT + Fore.YELLOW + "ARCHIVES"  + Fore.RESET + Style.RESET_ALL + " (Total: " + str(persistence.get_db_count("archive")) + ")" }')
            return

        elif command.startswith('how do i pronounce'):
            try:
                transformed = num_word_transform.number_to_words(command[19:])
                H(); sprint(transformed)
                return
            except Exception as e:
                H(); sprint(str(e))
            return

        elif command == 'banner':
            banners = ['db_banner2.py', 'db_banner3.py'] # for future: add other banners here
            os.system('python3 ./resources/banners/%s' % random.choice(banners))
            return

        elif command.startswith('find the') and 'root' in command:
            utils.find_root(command)
            return

        elif command.lower().startswith('list '):
            table = command[5:].strip(' ')
            listing_handler.list_table(table)
            return

        # todo: complete and refine implementation
        elif command == 'merge all relations':
            H(); sprint('Merging all unprotected intel relations. This may take a while.')
            result = persistence.merge_all_relations_by_tag()
            logging.debug(result)
            handle_persistence_response(result)
            return

        elif (command.lower().startswith('merge ') and command.lower() != 'merge all relations'):
            tag = command[6:].replace(' ', '_')
            result = persistence.merge_relation_by_tag(tag)
            handle_persistence_response(result)
            return

        elif command.lower().startswith('pin'):
            table = 'intelligence'
            tag = 'PIN_TO_START'
            document_to_be_tagged = command[4:].strip(' ')
            result = persistence.update_doc_flags(table, document_to_be_tagged, tag)
            handle_persistence_response(result)
            return

        elif command.lower() == 'clear pins':
            result = persistence.clear_all_pins()
            handle_persistence_response(result)
            return

        elif 'population density' in command:
            utils.population_density()
            return

        elif 'terminal' in command:
            H(); sprint('Terminal open.')
            display_manager.terminal_session()
            return

        elif command == 'htop':
            os.system('htop')
            return

        elif command == 'clean swap':
            logging.info('attempting to transfer swap memory to RAM')
            print(''); os.system('sudo swapoff -a && sudo swapon -a')
            logging.info('Swap cleansed.')
            H(); sprint('Swap cleansed.')
            return

        elif command == 'clean db':
            onboarding.clean_db()
            return

        elif 'network diagnostic' in command or command == 'netdog':
            print('')
            os.system('sudo nmcli radio wifi off')
            logging.debug('Turning wifi off.')
            os.system('nmcli radio wifi on')
            logging.debug('Turning wifi on.')
            os.system('sudo service network-manager restart')
            logging.debug('Restarting network manager.')
            H(); sprint('Diagnosis complete. Counter-measures deployed.')
            return

        elif command == 'whats my ip':
            H(); os.system('dig +short myip.opendns.com @resolver1.opendns.com')
            return

        elif 'all systems shutdown' in command:
            if os.environ['LUNA_USER'] == 'FRTNX':
                try:
                    os.system('sudo shutdown now')
                except KeyboardInterrupt:
                    return
                except Exception as e:
                    H();print(e)
                    return

            else:
                H(); sprint(random.choice(DoA))
                return

        elif command.startswith('convert'):
            utils.converter(command)
            return

        elif 'reboot all systems' in command:
            # refine condition to only execute when called by primary user
            if os.environ['LUNA_USER'] == 'FRTNX':
                try:
                    os.system('sudo reboot now')
                except KeyboardInterrupt:
                    return

                except Exception as e:
                    H(); print(e)
                    return
            else:
                H(); sprint(random.choice(DoA))
                return

        elif command.startswith('show me all '):
            utils.nearby(command[12:])
            return

        elif command.startswith('dict'):
            utils.dictionary()
            return

        elif 'fibonacci' in command:
            utils.laFibonacci()
            return

        elif 'koan' in command:
            utils.zen()
            return

        elif command == 'history':
            print('')
            os.system('sudo python3 herodotus.py')
            return

        elif 'exit' in command:
            H(); sprint(random.choice(farewell_responses))
            logging.warn('shutting down...')
            exit()

        else:
            H(); sprint(kernel.respond(command))
            result = persistence.insert_session_data(command)
            logging.info(result)
            return

    except Exception as e:
        rollbar.report_exc_info()
        H(); print(e)
        return