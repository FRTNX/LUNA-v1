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
import geocoder
import datetime
import requests
import uuid
import threading
from colorama import Fore
# from pymongo import MongoClient
from annoyances import *
from persistence import index as persistence

# client = MongoClient()
# db = client.in_vivo_veritas
# rec_loc = db.recent_location
# config = db.configurations

# TODO: check whether configurations exist in db before running below command.
if 'set' not in os.listdir('conf/'):
    os.system('mongorestore --db in_vivo_veritas conf/configurations.bson >> logs/luna.log')
    f = open('conf/set', 'w'); f.close()
    synonyms_handler = open('models/luna/main_nlu/entity_synonyms.json', 'w')
    synonyms_handler.write('{}'); synonyms_handler.close()


def character_loader(brain):
    # conf = config.find_one({'name': 'luna_predicates'})
    # predicates = conf['bot_predicates']
    predicates = persistence.fetch_bot_predicates()
    logging.info("Setting bot predicates")
    for i in range(len(predicates)):
        key = list(predicates[i])[0]
        brain.setBotPredicate(key, predicates[i][key])
    logging.info("Successfuly set bot predicates.")
    #brain.setBotPredicate("friends", "%s" % str(get_known_users())) # put rude users on revenge list


def guava():
    try:
        fruit_juice = str(geocoder.ip('me'))
        squeeze = fruit_juice[24:len(fruit_juice)-2]
        logging.info(squeeze)
        return squeeze
    except Exception:
        print("offline mode")
        logging.debug("Location unobtainable.")
        return "somewhere on planet Earth"


# def save_model():
#     model_file = open('data/nlu/nlu.json', 'r')
#     data = model_file.read()
#     entry = {
#              '_id': str(uuid.uuid4()),
#              'name': 'nlu_model',
#              'payload': data
#     }
#     config.delete_one({'name': 'nlu_model'})
#     config.insert_one(entry)


def get_state_bullet():
    try:
        requests.get('https://google.com')
        return Fore.GREEN + u"\u25CF " + Fore.RESET
    except:
        return Fore.LIGHTBLACK_EX + u"\u25CF " + Fore.RESET


def promptLoader():
    global h
    global header
    global agent
    global mc
    mc = '['+Fore.LIGHTBLACK_EX+'MISSION CONTROL'+Fore.RESET+'] '
    h = '\n['+Fore.LIGHTBLACK_EX+'LUNA'+Fore.RESET+'] '
    header = '\n['+Fore.LIGHTBLACK_EX+'SHADOW'+Fore.RESET+'] '
    agent = '\n['+Fore.LIGHTBLACK_EX+'AGENT'+Fore.RESET+'] '
    dr = '['+Fore.LIGHTBLACK_EX+'DIRECTOR'+Fore.RESET+'] '
    cell = '['+Fore.GREEN+'CELL'+Fore.RESET+']'+Fore.GREEN+'>>'+Fore.RESET
    uzer = ''
    bullet = Fore.GREEN + u"\u269B   " + Fore.RESET
    gbullet = Fore.LIGHTBLACK_EX + u"\u269B   " + Fore.RESET
    return mc, h, header, agent, dr, uzer, cell, bullet, gbullet


# move to weather directory
def get_coords():
    logging.debug('Obtaining spatial awareness.')
    try:
        raw_loc = geocoder.ip('me')
        coords = raw_loc.latlng
        if coords:
            persistence.clear_recent_locations()
            persistence.insert_coords(coords)
            return coords
        raise TypeError('')
    except:
        return persistence.fetch_coords()
