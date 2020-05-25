##################################################################################################

###########
###########
###########
###########
###########
###########                  '########           '##########################                    '######
###########                  '########           '###########################                  '########
###########                  '########           '############################                '##########
###########                  '########           '#######          '###########              '############
###########                  '########           '#######          '###########             '#####   '#####
###########                                      '#######          '###########            '#####     '#####
###########                  '########           '#######          '###########           '#######   '#######
###########                  '########           '#######          '###########          '####################
###########                                      '#######          '###########         '######################
###########                  '########           '#######          '###########        '########################
###########                  '########           '#######          '###########       '########         '########
###########                  '########           '#######          '###########      '########           '########
###########                  '########           '#######          '###########     '########             '########
###########                  '########           '#######          '###########    '########
#####################        '########           '#######          '###########   '########
############################# '########          '#######          '###########  '########
###############################'########         '#######          '########### '########
##############################  '################'#######          '###########   '#####
#############################    '###############   '####          '############'######
#############################      '################'####           '###########'##########


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

import sys
import random
import time
from colorama import Fore

ban = [
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '######################################TTTTTTLLLLLLLL######################################',
   '##################################TTTTTTLLLLLLLLLLLLLLLL##################################',
   '###############################TTTTTTLLLLLLLLLLLLLLLLLLLLL################################',
   '#############################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLL##############################',
   '############################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLL#############################',
   '###########################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLLLL############################',
   '###########################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLLLL############################',
   '###########################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLLLL############################',
   '###########################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLLLL############################',
   '############################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLL#############################',
   '#############################TTTTTTLLLLLLLLLLLLLLLLLLLLLLLLL##############################',
   '###############################TTTTTTLLLLLLLLLLLLLLLLLLLLL################################',
   '#################################TTTTTTLLLLLLLLLLLLLLLLL##################################',
   '#####################################TTTTLLLLLLLLLLL######################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################',
   '##########################################################################################'
]

char_set = ['1','2','3','4','5','6','7','8','9','#','@','F','R','T','N','X']

random_char = ['\u2648', 
               '\u2649', 
               '\u2650', 
               '\u2652', 
               '\u2651', 
               '\u2653', 
               '\u264c', 
               '\u264d', 
               '\u264a', 
               '\u264f',
               '\u264e',
               '\u26ce'
              ]

char_set.append(random.choice(random_char))

banner_line = 1

x_column = 1

print('\n\n')
for line in ban:
    formatted_line = ''
    for letter in line:
        if letter == '#':
            formatted_line += ' '
            # time.sleep(0.0001)
            sys.stdout.flush()
        # elif letter == ' ':
        #     print(letter, end='')
        #     sys.stdout.flush()
        elif letter == 'T':
            formatted_line += Fore.RESET+random.choice(char_set) + Fore.RESET
            # time.sleep(0.0001)
            sys.stdout.flush()
        else:
            formatted_line +=  Fore.LIGHTBLACK_EX+random.choice(char_set) + Fore.RESET
            # time.sleep(0.0001)
            sys.stdout.flush()  
    print(formatted_line)          
    # banner_line += 1
    # if banner_line == 13:
    #     for line in x:
    #         for char in line:
    #             if x_column == 9:
    #                 time.sleep(1)
    #                 print(Fore.GREEN+random.choice(char_set))
    #             else:
    #                 print(Fore.LIGHTBLACK_EX+random.choice(char_set), end='')
    #                 time.sleep(0.05)
    #                 sys.stdout.flush()
    #                 x_column += 1
    #         print()
    # else:
    #     print()

print(Fore.RESET+'\n\n')



