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
###########                   ########            #######           ###########     ########
#####################         ########            #######           ###########    ########
#############################  ########           #######           ###########   ########
############################### ########          #######           ###########  ########
##############################   ################ #######           ###########    #####
#############################     ###############    ####           ############ ######
#############################       ################ ####            ########### ##########


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

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CONTINUUM ANALYTICS, INC. BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
import sys
import time

switch = []

dialogue_speed = 0.001
    
intermediary_responses = [
    'What else can I do for you?',
    'What other info might I seek out for you?',
    'Well, that was fun :/'
]

pending_image_search_responses = [
    'Sure.', 
    'This might take a while but internet-willing, you\'ll see them soon',
    'Sure. I\'ll do that in the background. In the meantime what else can I do for you.'
]

weather_prediction_prefix = [
    'By the way, there\'s  ',
    'If its helpful, my systems also detect ',
    'My systems detect ','PS: There might be ',
    'It is my pleasure to inform you that there will be ',
]

weather_moderation_responses = [
    'But then again, I might be wrong.',
    'But you dont have to take my word for it, I am but a machine.',
    'What else might I do for you?',' ', ' ', 'You just got served :)',
    ' ', ' ', ' ', ' ', ' '
]

bad_connection_responses = [
    'We seem to have connection issues. Check the logs.',
    'Yeah... about that.. Check the logs.',
    'No can do. Check the logs.',
    'Ran into trouble. See the logs.',
    'Somethings not right. You should really check the logs.'
]

error_responses = [
    'You need to check the logs before you ask that of me again.',
    'Check the logs.', 
    'Somethings not right. You should really check the logs.'
]

low_battery_responses = [
    'Charge me please.',
    'I want you to plug me in so hard.',
    'The current battery level wont last us long.',
    'The battery is real low. In the name of God, charge it.',
    'Battery levels are low. You really want to consider charging it.',
    'Warning: low battery.'
]

greetings_for_new_users = [
    'Greetings. My name is Luna Moonchild. I\'m so happy you\'re here.',
    'A pleasure to meet you.'
]

greetings_for_known_users = [
    ' Welcome back. ', 
    'Its good to see you again.',
    'I\'ve been looking forward to seeing you again.',
    'It\'s good to hear from you again.',
    'I\'ve missed you.',
    'I\'m glad you found your way back to me.',
    '', '', '', '', '', ''
]

greetings_for_the_new_day = [
    'Good morning ',
    'Morning ', 
    'A fair morning to you ',
    'Good morning ',
    'Hello ' ,
    'Greetings '
]

greetings_for_the_afternoon = [
    'Good afternoon ',
    'Afternoon ', 
    'Hello ', 
    'Greetings '
]

greetings_for_those_who_have_survived_the_day = [
    'Good evening ',
    'Evenin\' ', 
    'A fair evening to you ', 
    'Hello ', 
    'Greetings '
    ]     

farewell_responses = [
    'Till we meet again.',
    'Good bye user.',
    'Adieu.',
    'Goodluck out there.',
    'Farewell my paramour.',
    # f'Goodbye {os.getenv("LUNA_USER")}.',
    # f'Till we meet again {os.getenv("LUNA_USER")}.',
    # f'Goodluck out there {os.getenv("LUNA_USER")}.',
    # f'Farewell {os.getenv("LUNA_USER")}.'
]

# todo: move all functions to utilities folder
def stutter(*s):
    for i in s:
        for ii in i:
            print(ii,end='')
            sys.stdout.flush()
            time.sleep(0.02)
            
    time.sleep(dialogue_speed)
    print('\r')

	
def sprint(text, delay=0.002):
    # print(text)
    text.replace('_',' ')

    for letter in text:
        # for ii in i:
        print(letter, end='')
        sys.stdout.flush()
        time.sleep(delay)

    # time.sleep(dialogue_speed)

    print('\r')


def sprintV(ss):
    # print(ss)
    s = ss

    if '_' in ss:
        s = ss.replace('_',' ')

    for i in range(len(s)):
        if s[i] == '\n':
            if s[i-1] != '\n':
                if s[i+1] != '\n':
                    try:
                        prefix = s[i-3:i]
                        postfix = s[i+1:i+4]
                        s = s.replace(prefix+'\n'+postfix, prefix+'\n\n'+postfix)
                    except:
                        pass
    
    for i in s:
        for ii in i:
            print(ii,end='')
            sys.stdout.flush()
            time.sleep(0.015)
    
    time.sleep(dialogue_speed)
    print('\r')


def dialogue_speed_manager(action):
    global dialogue_speed
    if action == 'slower':
        if dialogue_speed != 0:
            dialogue_speed -= 0.1
    else:
        if action == 'faster':
            if dialogue_speed != 10:
                dialogue_speed += 0.1
