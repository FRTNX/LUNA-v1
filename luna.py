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
import json
import rollbar
import random
import warnings
import requests
import wikipedia
# from personality import *
from rasa_nlu.model import Interpreter
from functions.responses import *
from persistence import index as persistence
from functions.utils import main as utils
from functions.weather import main as weather
from functions.informant import main as intel_handler
from functions.onboarding import main as onboarding
from functions.display_manager.main import output_prompt as H
from functions.display_manager import main as display_manager
from functions.command_handler.main import command_handler
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from func_timeout.StoppableThread import StoppableThread
from func_timeout import func_timeout, FunctionTimedOut

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

prompt_style = style_from_dict({
    Token: '#F5F5F5',
    Token.OpenBrace: '#F5F5F5',
    Token.UserName: '#545454',
    Token.CloseBrace: '#F5F5F5'
})

def get_prompt_tokens(cli):
    return [
        (Token.OpenBrace, '\n['),
        (Token.UserName, os.environ['LUNA_USER']),
        (Token.CloseBrace, '] ')
    ]

def handle_user_input(user_input):
    processed = intent_and_entity_rerouter(user_input);
    if processed:
        return
    command_handler(user_input)
    return

def prompt_handler():
    while True:
        try:
            # LunaCompleter = WordCompleter(persistence.fetch_title_suggestions(), ignore_case=True) # get wordlist instead?
            user_input = prompt(
                get_prompt_tokens=get_prompt_tokens,
                style=prompt_style,
                history=FileHistory('history.txt'),
                # todo: auto suggest from titles in db, split into words, filtered for duplicates
                auto_suggest=AutoSuggestFromHistory(),
                # completer=LunaCompleter,
            )
            handle_user_input(user_input)
        except Exception as e:
            logging.error(f'Error processing user input: {e}')
            pass

# todo: move to config file
nlu_ignore = ['extract ', 'list ', 'pin ', 'merge ', 'whats in the ', 'convert ', 'search ']

def nlu_parser(text):
    parsed_text = requests.post('http://localhost:5000/parse', data=json.dumps({ 'q': text }))
    return json.loads(parsed_text.text)

def intent_and_entity_rerouter(text):
    logging.info('Intent classifier received: %s' % text)
    for ignorable in nlu_ignore:
        if (text.lower().startswith(ignorable)):
            command_handler(text)
            return True

    THRESHOLD = 0.75

    try:
        nlu_response = func_timeout(1, nlu_parser, args=(text,))
    except (FunctionTimedOut, Exception) as e:
        logging.error(f'Error getting NLU data: {e}')
        return False
        
    logging.debug('Intent classifier response: %s' % nlu_response)
    if nlu_response['intent']['confidence'] >= THRESHOLD:
        intent = nlu_response['intent']['name']
        entities = nlu_response['entities']

        has_entities = isinstance(entities, list) and len(entities) > 0 

        if intent == 'get_weather':
            logging.info('Weather request acknowledged. Sending through designated path.')
            if entities:
                weather.get_weather(False, False, *[entities[0]['value']])
            else:
                weather.get_weather()
            return True

        elif intent == 'find_info' and has_entities:
            # TODO: consider how to make images and local lookup optional
            # possible intents: toggle_image_display (translated entities: on/off); toggle_air_gap (grants or removes Luna's access to the internet,
            # and, more importantly, the internets access to Luna)
            action = intel_handler.informant(entities[0]['value'].title(), True, 0, False)
            logging.info(f'Caller received action: {action}')
            if action:
                handle_user_input(action)
            return True

        elif intent == 'find_images':
            if utils.is_online():
                entity = entities[0]['value']
                try:
                    image_urls = wikipedia.page(entity).images
                    render_images = StoppableThread(target=display_manager.fetch_images, args=(entities[0]['value'], image_urls,))
                    render_images.daemon = True
                    render_images.start()
                    H(); sprint(random.choice(pending_image_search_responses))
                except Exception as e:
                    logging.error(e);
                    H(); sprint('For some reason I could not comply.')
            else:
                H(); sprint('I need an internet connection to comply.')
            return True            

        elif intent == 'find_related_info' and has_entities:
            utils.find_related(entities[0]['value'])
            return True

        elif intent == 'directions' and has_entities:
            origin = None
            destination = None
            for entity in entities:
                if entity['entity'] == 'source':
                    origin = entity['value']
                elif entity['entity'] == 'destination':
                    destination = entity['value']
            logging.info('Parsing direction query with destination: %s and origin: %s' % (destination, origin))
            if destination:
                utils.directions(destination, origin)
            else:
                H(); sprint('No destination found.')
            return True

        elif intent == 'find_location' and has_entities:
            utils.find_location(entities[0]['value'])
            return True

        elif intent == 'find_more_info' and has_entities:
            action = intel_handler.informant(entities[0]['value'].title(), False, 0, True)
            logging.info(f'Caller received action: {action}')
            if action:
                handle_user_input(action)
            else:
                return True

        else:
            return False
            
    return False


if __name__ == '__main__':
    logging.debug('Initialising')
    onboarding.suggested_reading()
    user = onboarding.initialize()
    logging.info(f'Got user back from identifier: {user}')
    while True:
        try:
            # check for pending user messages
            # display if present
            prompt_handler()
        except KeyboardInterrupt as e:
            # todo: verify action
            H(); sprint(random.choice(farewell_responses))
            logging.info('Session terminated by user')
            logging.warn('Shutting down')
            exit()
