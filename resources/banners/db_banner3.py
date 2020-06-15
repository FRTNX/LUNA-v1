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


base_x = '############################################'
base_y = '#########################################LLL'
gram_a = '#############LLLLLLLLLLLLLLLLLL#############'
gram_b = '#############LLLLLL      LLLLLL#############'
space = '                             '

char_set = ['1','2','3','4','5','6','7','8','9','#','@','U', 'E', 'M', 'I', 'P', 'V', 'B', 'L', 'S', 'D', 'O', 'R', 'N', 'A']

def color(text, color):
    if (color == 'light_black'):
        return  Fore.LIGHTBLACK_EX + text + Fore.RESET
    if (color == 'green'):
        return Fore.GREEN + text + Fore.RESET

# todo: refactor
print('\n\n')
for i in range(4):
    formatted_line = ''
    for letter in base_x:
        if letter == '#':
            formatted_line += color(random.choice(char_set), 'light_black')
            sys.stdout.flush()
        elif letter == ' ':
            formatted_line += ' ' 
            sys.stdout.flush()
    print(f'{space}{formatted_line}')

for i in range(6):
    line = random.choice([gram_a, gram_b])
    formatted_line = ''
    for letter in line:
        if letter == '#':
            formatted_line += color(random.choice(char_set), 'light_black')
            sys.stdout.flush()
        elif letter == ' ':
            formatted_line += color(random.choice(char_set), 'light_black')
            sys.stdout.flush()
        else:
            formatted_line +=  ' '
            sys.stdout.flush()  
    print(f'{space}{formatted_line}\n{space}{formatted_line}')

for i in range(4):
    formatted_line = ''
    if i < 2:
        for letter in base_x:
            if letter == '#':
                formatted_line += color(random.choice(char_set), 'light_black')
                sys.stdout.flush()
            elif letter == ' ':
                formatted_line += ' ' 
                sys.stdout.flush()
        print(f'{space}{formatted_line}')
    else:
        for letter in base_y:
            if letter == '#':
                formatted_line += color(random.choice(char_set), 'light_black')
                sys.stdout.flush()
            else:
                formatted_line += color(random.choice(char_set), 'green') 
                sys.stdout.flush()
        print(f'{space}{formatted_line}')

print(Fore.RESET+'\n\n')
time.sleep(1)



