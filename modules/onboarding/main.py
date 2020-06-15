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
import re
import time
import codecs
import random
import rollbar
import datetime
import requests
import warnings
import configparser
from func_timeout.StoppableThread import StoppableThread
from modules.onboarding.introduction import Introduction
from personality import *
from personality import get_state_bullet
from colorama import Fore
from modules.responses import *
from lxml import html
from modules.persistence import db_handler as persistence
from modules.display_manager import main as display_manager
from prompt_toolkit.shortcuts import prompt

config = configparser.ConfigParser()
config.read('modules/persistence/db.ini')


def suggested_reading():
    titles = persistence.fetch_reading_list()
    print(beam + '\nSuggested Reading:\n' + beam)
    for title in titles:
        print(title)
    print(beam)
    time.sleep(1)


def initialize():
    now = datetime.datetime.now()
    state_bullet = get_state_bullet()
    print(state_bullet + str(now))
    banners = ['banner1.py']
    banner = random.choice(banners)
    os.system('python3 ./resources/banners/%s' % banner)
    time.sleep(1)

    # only fetch quotes if last extraction time is >= 24hours
    try:
        if (config['defaults']['find_quotes'] == 'True'):
            logging.info(f'Beginning quote extraction with {persistence.count_quotes()} persisted quotes')
            quote_thread = StoppableThread(target=get_quotes)
            quote_thread.daemon = True
            quote_thread.start()
        display_manager.output_prompt(); sprint(persistence.fetch_quote())
        logging.info('Initialisation complete, exception free.')
        user = identify_user()
        return  user

    except Exception as e:
        rollbar.report_exc_info()
        logging.warn(str(e))
        logging.info('Post exception initialisation complete.')
        display_manager.output_prompt(); sprint(persistence.fetch_quote())
        user = identify_user()
        return user


def get_quotes():
    """Gets quotes from brainyquote.com and stores them (in the presence of internet).
       Gracefully returns if offline.
    """ 
    topics = [
        'war',
        'learning',
        'leadership',
        'knowledge',
        'technology',
        'nature',
        'great',
        'inspirational'
    ]
    for topic in topics:
        try:
            page = requests.get('https://www.brainyquote.com/topics/{}'.format(topic))
            tree = html.fromstring(page.content)
            q = tree.xpath('//a[@title="view quote"]/text()')
    
            for quote in q:
                try:
                    insertion_res = persistence.insert_quote(quote)
                    logging.info(insertion_res)
                except ValueError as e:
                    logging.debug(quote)
                    pass
        except Exception as e:
            rollbar.report_exc_info()
            logging.error(str(e))
            return
    database_cleanse = StoppableThread(target=clean_db, args=(True,))
    database_cleanse.daemon = True
    database_cleanse.start()
    

def clean_db(void=False):
    """Cleans the database of quotes which include specified stopwords."""
    logging.info('Cleaning database.')
    result = persistence.clean_quotes()
    logging.info(result)
    return


def identify_user():
    """Identifies user and greets them accordingly. If a user is logging in for the
       first time a full on introduction is provided. 
    """
    logging.info('Identifying user')

    try:
        known_users = persistence.get_known_users()
        
        user_name = prompt('\n                                              Code Name:').strip()
        if (len(user_name) == 0):
            user_name = 'USER'

        if user_name == os.getenv("PRIUSER"):
            set_user(user_name)
            time.sleep(1)
            display_manager.output_prompt(); sprint(f'{time_conscious_greeting()}commander.')

        elif user_name.lower() in known_users:
            set_user(user_name)
            display_manager.output_prompt(); sprint(f'{time_conscious_greeting()}{user_name} {random.choice(greetings_for_known_users)}')

        else:
            persistence.insert_new_user(user_name)
            set_user(user_name)
            display_manager.output_prompt(); sprint(f'{time_conscious_greeting()}{user_name}. My name is Luna.')
            try:
                introduction = Introduction()
                sprint(introduction.run())
            except KeyboardInterrupt:
                pass

        # k.setPredicate("name", user_name)
        logging.info('User identified as %s' % user_name)
        return user_name

    except KeyboardInterrupt:
        logging.info('Session terminated by user')
        logging.debug('shutting down')
        exit()


def set_user(user_name):
    global user_input_tag
    user_input_tag = create_prompt(user_name)
    os.environ['LUNA_USER'] = user_name.upper()
    return    


def create_prompt(name):
    """Creates the users prompt tag."""
    return '\n[' + Fore.LIGHTBLACK_EX + name.upper() + Fore.RESET + '] '


def time_conscious_greeting():
    """Evaluates current time and issues a time-correct greeting."""
    time = datetime.datetime.now()
    time_string = str(time)
    pattern = r'([0-9]+):([0-9]+):[0-9][0-9]'
    target_string = re.search(pattern, time_string)
    target_substring = target_string.group()
    hour = int(target_substring[:2])

    if hour < 12:
        return random.choice(greetings_for_the_new_day)
    elif hour >= 18:
        return random.choice(greetings_for_those_who_have_survived_the_day)
    else:
        return random.choice(greetings_for_the_afternoon)
