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
import PIL
import json
import time
import rollbar
import warnings
# from personality import *
from colorama import Fore
from functions.responses import sprint
from datetime import date
from PIL import Image
from email.header import Header, decode_header, make_header
from requests.exceptions import ConnectionError
from persistence import index as persistence
from functions.utils import main as utils
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter

warnings.filterwarnings("ignore", category=UserWarning, module='PIL')
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

def input_prompt():
    return prompt(
        get_prompt_tokens=get_prompt_tokens,
        style=prompt_style,
        history=FileHistory('history.txt'),
        auto_suggest=AutoSuggestFromHistory()
    )


def output_prompt(prompt=None):
    if prompt:
        print(prompt, end='')
        return
        
    print(utils.standard_output_prompt, end='');
    time.sleep(0.2)
    return


def terminal_session():
    """
    Provides access to bash.
    """
    try:
        print(Fore.BLUE + '\n' + f'{os.environ["LUNA_USER"].lower()}@blueterm' + Fore.RESET + ':' + Fore.LIGHTBLACK_EX + '~' + Fore.RESET + '$ ', end='')
        cmd = prompt('', history=FileHistory('terminal_history.txt'), auto_suggest=AutoSuggestFromHistory())
        if cmd != 'exit':
            os.system(cmd)
            terminal_session()
        else:
            output_prompt(); sprint('Terminal terminated.')

    except KeyboardInterrupt:
        rollbar.report_exc_info()
        logging.warn('terminal session was interrupted by user.')
        print('\n'); output_prompt; sprint('Terminal terminated.')


# migrate implementation to Postgres
# def quote_search:
#     """Searches quote database for substring.
#     """
#     output_prompt; sprint('Enter search term')
#     term = input(user_input_tag)
#     found = False
#     for file in files.find():
#         if term.lower() in file['payload'][0].lower():
#             print(Fore.BLUE + solid_semi + Fore.RESET + '\n\n' + file['payload'][0])
#             found = True
#     if not found:
#         sprint("Could'nt find anything related to that")
#     return

def is_image_supported(image):
    return image.endswith('.jpg') or image.endswith('.png')

def fetch_images(entity, image_urls):
    """Downloads and displays images. Can be called directly or from a parallel thread by 
       the informant() function.
    """
    if not utils.is_online():
        return

    logging.info('Running image extraction in background thread')
    entity = entity.replace(' ', '_').replace('(', '').replace(')', '').replace("'","").lower()
    basewidth = 400  # This value controls the width of images displayed. Edit as needed.

    try:
        valid_images = list(filter(is_image_supported, image_urls))
        logging.info(f'Images selected for extraction: {valid_images}')
        valid_images.reverse()

        for image in valid_images[:5]:
            os.system('wget -b -P ./downloads/%s/ %s >/dev/null 2>&1' % (entity, image))

        time.sleep(10)
        os.system('rm wget-log* >/dev/null 2>&1')

        display_list = os.listdir('./downloads/%s/' % entity)
        logging.info(f'About to display images: {display_list}')
        
        for image in display_list:
            try:
                # to remove this monstrosity, relabel downloaded images to {entity}_{n}.jpg
                logging.info(f'Rendering: {json.dumps(image)}')
            except Exception as e:
                logging.warn(e)

            img = Image.open('./downloads/%s/%s' % (entity, image))
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            img.show()

        time.sleep(20)
        os.system('rm -r ./downloads/%s --force' % entity)
        return
    except (OSError, FileNotFoundError):
    	pass
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(e)
        return