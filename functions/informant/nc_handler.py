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


# todo: add this to README in functions folder
# A quick note on imports: It may puzzle those reading this file to see imports of files that are
# not within this files directory or subdirectory. As I have come to understand, as this file is
# imported by luna.py in the projects top level directory, all imports in any other subdirectory
# must be made as if they were in luna.py. The imports below make sense if you imagine them being called
# from luna.py. This has certain advantages, like a shared persistence directory, i.e, all files imported by 
# luna.py will have access to the top-level persistence directory.

import time
import os
import PIL
import rollbar
import wikipedia
import warnings
import sys
from PIL import Image
from colorama import Fore
from newscatcher import Newscatcher, describe_url, urls, list_all_urls
from bs4 import BeautifulSoup
from func_timeout import func_timeout, FunctionTimedOut
from func_timeout.StoppableThread import StoppableThread
from persistence import index as persistence
from functions.responses import *
from functions.utils import index as utils
from functions.display_manager import main as display_manager
from annoyances import *


gbullet = Fore.LIGHTBLACK_EX + u"\u269B   " + Fore.RESET
bullet = Fore.GREEN + u"\u269B   " + Fore.RESET
output_prompt = '\n[' + Fore.LIGHTBLACK_EX + 'LUNA' + Fore.RESET + '] '

found = False

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

state_object = {}

supported_topics = ['tech', 'news', 'business', 'science', 'finance', 'food', 'politics',
    'economics', 'travel', 'entertainment', 'music', 'sport', 'world']

supported_countries = ['US', 'GB', 'DE', 'FR', 'IN', 'RU', 'ES', 'BR', 'IT', 'CA', 'AU', 'NL', 'PL', 'NZ', 'PT',
    'RO', 'UA', 'JP', 'AR', 'IR', 'IE', 'PH', 'IS', 'ZA', 'AT', 'CL', 'HR', 'BG', 'HU', 'KR', 'SZ', 'AE', 'EG',
    'VE', 'CO', 'SE', 'CZ', 'ZH', 'MT', 'AZ', 'GR', 'BE', 'LU', 'IL', 'LT', 'NI', 'MY', 'TR', 'BM', 'NO', 'ME', 'SA', 'RS', 'BA']

supported_urls = list_all_urls()

# todo: move to common files
def H(*n):
    if not n:
        print(output_prompt, end='');
    else:
        print(n[0], end='')
    time.sleep(0.2)

def get_page_size(display_object):            
    range_end = 10 if len(display_object) >= 10 else len(display_object)
    return [0, range_end]

def select_option(display_object, display_range, criteria=None):
    global state_object
    for i in range(display_range[0], display_range[1]):
        print(f'{i+1} {display_object[str(i)]}')
        
    # context management
    active_navigation_options = ['99']
    default_navigation_options = ['99', 'b', 'n', 'm', 'c']
    
    if (display_range[0] > 0):
        print('b back  ', end='')
        active_navigation_options.append('b')
    if (display_range[1] + 1 < len(display_object)):
        print('n next')
        active_navigation_options.append('n')
    print('\n99 exit | m main menu | c criteria selection')
    
    displayed_options = [*range(display_range[0] + 1, display_range[1] + 1)]
    logging.info('Got rows on current page: %s' % displayed_options)

    user_input = display_manager.input_prompt()
    print('')
    
    # selection logic
    if (user_input.isnumeric() and int(user_input) in displayed_options):
        index = int(user_input) - 1 # displayed indexes are 1-based, their source object is 0-based
        logging.info('Selected row number: %s' % index)
        logging.info('Applying to object: %s' % display_object)
        state_object = { 'value': display_object[f'{index}'], 'last_displayed': display_range, 'index': index }
        logging.info('State object: %s' % state_object)
        return
     
    # navigation logic
    if (user_input in default_navigation_options):
        if (user_input.lower() == 'n'):
            page_size = 10 if len(display_object) > 10 else len(display_object) -1
            range_start = display_range[0] + page_size
            range_end = display_range[1] + page_size

            if range_end > len(display_object):
                range_end = len(display_object)

            if (user_input in default_navigation_options and user_input not in active_navigation_options):
                range_start = 0
                range_end = 10 if len(display_object) > 10 else len(display_object)
            
            logging.info(f'Requesting pages {range_start} to {range_end}')
            select_option(display_object, [range_start, range_end], criteria)

        if (user_input.lower() == 'b'):
            if (displayed_options[0] == 1):
                logging.info('Return to main menu requested')
                list_urls(criteria)
                return

            range_start = display_range[0] - 10 if display_range[0] > 10 else 0
            range_end = range_start + 10
            logging.info(f'Requesting pages {range_start} to {range_end + 5}')
            select_option(display_object, [range_start, range_end], criteria)

        if (user_input.lower() == 'm'):
            logging.info('Return to main menu requested')
            list_urls(criteria)
            return

        if (user_input.lower() == 'c'):
            logging.info('Return to criteria selection requested')
            main()
            return

        if (user_input == '99'):
            state_object = { 'value': 'exit', 'last_displayed': display_range, 'index': 0 }
            logging.info('Exiting with state: %s' % state_object)
            return 
        return

def enumerate_array(array):                   
    return_object = {}                                                  
    for i in range(0, len(array)):                     
        return_object[f'{i}'] = array[i]        
    return return_object

def extract_title(article):                   
    return article['title']

def reset_state():                           
    global state_object                                                       
    state_object = None

def get_urls(criteria):
    result = { 'urls': [], 'type': None }
    if (criteria.lower() in supported_topics):
        result['urls'] = urls(topic = criteria)
        result['type'] = 'topic'
    if (criteria.upper() in supported_countries):
        result['urls'] = urls(country = criteria)
        result['type'] = 'country'
    if (criteria.lower() in supported_urls):
        result['urls'] = [criteria.lower()]
        result['type'] = 'website'
    return result

# todo: split into smaller functions
def list_urls(criteria):
    try:
        global state_object
        reset_state()
        url_object = get_urls(criteria)
        logging.info('Criteria eval resulted in url object: %s' % url_object)
        url_list = url_object['urls']

        if (len(url_list) == 0):
            logging.info('Unsupported topic or country: %s' % criteria)
            return
        
        if (url_object['type'] == 'website'):
            selected_url = url_object['urls'][0]
            logging.info('Selected url: %s' % state_object)
        else:
            logging.info('Got urls: %s' % len(url_list))
            display_object = enumerate_array(url_list)
            logging.info('First item: %s' % display_object['0'])
            range_end = 10 if len(display_object) >= 10 else len(display_object)
            select_option(display_object, [0, range_end], criteria)

            if state_object['value'] == 'exit':
                return

            logging.info('Received state object: %s' % state_object)
            selected_url = state_object['value']

        if (url_object['type'] == 'topic'):
            source = Newscatcher(website = selected_url, topic = criteria)
        else:
            source = Newscatcher(website = selected_url)
        results = source.get_news()
        articles = results['articles']
        reset_state()
        
        titles = list(map(extract_title, articles))
        enumerated_titles = enumerate_array(titles)
        logging.info('Got titles: %s' % enumerated_titles)
        display_size = get_page_size(enumerated_titles)
        select_option(enumerated_titles, display_size, criteria)
        logging.info('Received state object: %s' % state_object)

        if state_object['value'] == 'exit':
            return

        selected_article = state_object
        print('> ', end='')
        print(f'{Fore.LIGHTBLACK_EX + articles[selected_article["index"]]["published"] + Fore.RESET}\n')
        html = articles[selected_article['index']]['summary']
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.get_text())
        print(f'{beam}')


        # todo: refactor
        while state_object['value'] != 'exit': 
            print('')
            select_option(enumerated_titles, state_object['last_displayed'], criteria)
            logging.info('Got state object: %s' % state_object)
            selected_article = state_object
            if selected_article['value'] != 'exit':
                print('> ', end='')
                print(f'{Fore.LIGHTBLACK_EX + articles[selected_article["index"]]["published"] + Fore.RESET}\n')
                html = articles[selected_article['index']]['summary']
                soup = BeautifulSoup(html, 'html.parser')
                print(soup.get_text())
                print(f'{beam}')
            else:
                break

        return state_object

    except KeyboardInterrupt:
        state_object = { 'value': 'exit', 'last_displayed': [], 'index': 0 }
        return
    except Exception as e:
        logging.error('Error: %s' % e)
        return
    
def main():
    try:
        global state_object
        state_object = {
            'value': 'initialise',
            'last_displayed': [],
            'index': 0
        }

        while state_object['value'] != 'exit':
            H(); sprint('Enter a search critria')
            topic = display_manager.input_prompt()
            print('')
            list_urls(topic)

        logging.info('News crawler deactivated')
        return
    except Exception as e:
        logging.error('ERROR: %s' % e)
        state_object = { 'value': 'exit', 'last_displayed': [], 'index': 0 }
        return
