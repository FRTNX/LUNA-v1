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
import gc
import poplib
import geopy
import datetime
import uuid
import webbrowser
import wikipedia
import time
import psutil
import rollbar
import random, smtplib, requests
from personality import *
from urllib.request import URLError
from urllib.request import urlopen
from translator import trans_to_eng
from rasa_nlu.model import Interpreter
from colorama import Fore
from functions.responses import *
from goo import search
from lxml import html
from geopy.geocoders import Nominatim
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from resources.algorithms import Stack
from datetime import date
from func_timeout.StoppableThread import StoppableThread
from geopy.distance import vincenty
from glob import glob
from requests.exceptions import ConnectionError
from persistence import index as persistence
from functions.display_manager.main import output_prompt as H
from functions.display_manager import main as display_manager
from prompt_toolkit.shortcuts import prompt
# from prompt_toolkit.history import FileHistory
# from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

layout = Nominatim()

standard_output_prompt = '\n[' + Fore.LIGHTBLACK_EX + 'LUNA' + Fore.RESET + '] '

def is_online():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err: 
        return False


def find_external_resource():
    """Searches for links related to a specified subject. e.g., It can be used to search for pdf
       links that can then be curled through Luna's ghost terminal."""

    H(); sprint("What do you need?")
    res = display_manager.input_prompt()

    try:
        # for anonymity edit google library to run through proxychains
        urls = search(res, stop=20)
        H(); sprint("Take your pick.")
        for url in urls:
            print(url)
            time.sleep(0.03)
        return
    except Exception as e:
        logging.debug(str(e))
        H(); sprint(random.choice(bad_connection_responses))
        return


def imageFinder(entity, num_instances):
    """Deprecated. Downloads images without displaying them. Stores them in ./LUNA/downloads.
    """
    try:
        os.system( 'googleimagesdownload --keywords "%s" --limit %s' % (entity, num_instances) )
        H(); sprint("You know where to find them.")
    except KeyboardInterrupt:
        H(); sprint("You know where to find them.")


def population_density():
    """Measures the population density of a specified area, given the population.
    """
    H(); sprint("Please enter the number of people who live in this area.")
    population = display_manager.input_prompt().replace(',','')
    H(); sprint("Enter the size of the area in square kilometers.")
    area = display_manager.input_prompt().replace(',','')
    H(); sprint("The population density of this area is %s people per square kilometer." % str(int(population)/int(area)))


def init_translator(*session):
    """Initialises and terminates translator mode.
    """
    if not session:
        H(); sprint('translator activated.')
    raw_text = display_manager.input_prompt()

    if raw_text.lower() != 'exit':
        human_lang_translator(raw_text)
    else:
        H(); sprint('translator terminated.')


def human_lang_translator(text):
    """Translates text to english.
    """
    try:
        H(); sprint(trans_to_eng(text))
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(str(e))
        H(); sprint('Some of my agents seem to be inhibited. Check the logs.')
    init_translator(*['session'])


def code_search():
    """Searches files in specified folder for occurances substring.
    """
    H(); sprint('Enter phrase or code snippet')
    term = display_manager.input_prompt()

    H(); sprint("Please enter the path to the folder you'd like to begin the search from.")
    root_dir = display_manager.input_prompt()

    try:
        H(); sprint("Looking it up..")
        os.system("gnome-terminal -e \"grep -rnw '%s' -e '%s'\"" % (root_dir, term))
    except KeyboardInterrupt as e:
        return
    except Exception as e:
        rollbar.report_exc_info()
        print(e)
        pass
    return


def groundDistance(point_x, point_y):
    """Measures distance between one geographic location to another.
       Example input: 'what is the distance between New York and California'.
    """
    try:
        x_raw = layout.geocode(point_x)
        y_raw = layout.geocode(point_y)
        x = (x_raw.latitude, x_raw.longitude)
        y = (y_raw.latitude, y_raw.longitude)
        xydistance = vincenty(x,y).kilometers # other options: .nautical, .miles, .ft, ...etc. see docs
        H(); sprint("The distance between %s and %s is %s kilometers" % (point_x.title(), point_y.title(), xydistance))
        return
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(e)
        groundDistance(point_x, point_y)


def gridWeight(entity):
    """Unimplemented. Ignore for now.
    """
    try:
        loc = layout.geocode(entity)
        H(); sprint("%s has an importance weight of %s" % (entity.title(), loc.raw['importance']))
        return
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(e)
        gridWeight(entity)


def find_root(t):
    """Find the square root of a specified number.
    """
    index = float(t[t.find('the')+4:t.find('root')-1])
    radicand = float(t[t.find('of')+3:])
    root = radicand**(1/index)
    H(); sprint('The %s root of %s is %s' % (index, radicand, root))
    return


def converter(string):
    """Converts decimal to one of several bases. Valid bases are 2,3,4,5,6,7,8,9,10,11,12,16,20 and 60.
    """
    request = string

    mapper = [
               { 'binary': 2 },
               { 'ternary': 3 },
               { 'quarternary': 4 },
               { 'quinary': 5 },
               { 'senary': 6 },
               { 'septenary': 7 },
               { 'octal': 8 },
               { 'nonary': 9 },
               { 'decimal': 10 },
               { 'undenary': 11 },
               { 'duodecimal': 12 },
               { 'hexadecimal': 16 },
               { 'vigesimal': 20 },
               { 'sexagesimal': 60 }
            ]

    formats = []

    for mapp in mapper:
        formats.append(list(mapp)[0])

    # TODO: replace this algorithm with NLU
    if request.endswith('to decimal'):
        seg = request[:len(request)-8]
        base = ''
        for form in formats:
            if form in seg:
                base = form
        if base != '':
            extracted = 0
            for f in mapper:
                if list(f)[0] == base:
                    extracted = f[base]
            operand = seg[seg.find(base) + len(base) + 1: seg.find('to')]
            H(); sprint(int(operand, extracted))
            return
    else:
        base = ''
        for formatt in formats:
            if formatt in request:
                base = formatt
        if base != '':
            extracted = 0
            for f in mapper:
                if list(f)[0] == base:
                    extracted = f[base]
        else:
            H(); sprint("Sorry. I couldn't convert that.")
            logging.error('No converter found')
        stop1 = string.find(' to ')
        operand = string[8:stop1]
        try:
            H(); sprint(base_converter(int(operand), extracted))
            return
        except Exception as e:
            rollbar.report_exc_info()
            print(str(e))
            return


def base_converter(dec_number, base):
    """converter() helper function. Does the actual conversion.
    """
    digits = "0123456789ABCDEF"
    rem_stack = Stack()
    while dec_number > 0:
        rem = dec_number % base
        rem_stack.push(rem)
        dec_number = dec_number // base
    new_string = ""
    while not rem_stack.is_empty():
        new_string = new_string + digits[rem_stack.pop()]
    return new_string


def help_center():
    """Provides a list of valid commands and general instructions.
    """
    f = open('commands', 'r')
    ff = f.read()
    print(ff)
    return


def latency():
    os.system("python performance.py")


def directions(destination=None, origin=None):
    """Opens default browser and maps out possible routes between two geographic points.
       params:
           destination -> string; route destination
           origin      -> string; route origin
    """
    try:
        if not origin:
            origin = 'my+location'
            H(); sprint('Charting a course to %s.' % destination.title())
        else:
            H(); sprint('Charting a course to %s from %s.' % (destination.title(), origin.title()))
        os.system("gnome-terminal -e 'python -m webbrowser -t 'https://www.google.com/maps/dir/%s/%s''" % (origin, destination))
        return
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(e)
        H(); sprint(random.choice(error_responses))
        return


def find_location(location_name):
    """Plots the location of a specified place within google maps in default browser.
       params:
           location_name -> string; name of place whose location is sought.
    """
    try:
        os.system("gnome-terminal -e 'python -m webbrowser -t 'https://www.google.com/maps/place/%s''" % location_name)
        return
    except Exception as e:
        rollbar.report_exc_info()
        H(); sprint(random.choice(error_responses))
        return

# note_manager
def ethan():
    inp = display_manager.input_prompt()

    if inp.startswith('open'):
        target = inp[5:]
        try:
            x = hades.find_one({'title': target})
            sprint(x['payload'])
        except Exception as e:
            rollbar.report_exc_info()
            H(); sprint("No record found.")
    else:
        controlCentre(*[inp])


# migrate
def find_related(key_word):
    """Finds articles in main database (intel, in this case) that contain keyword.
    """
    H(); sprint('This might take a while so please be patient.')
    try:
        keyword = key_word
        found = []
        count = 0
        cycle = 0
        for file in intel.find():
            if ' '+keyword.lower()+' ' in file['payload'][0].lower():
                found.append([file['payload'][0].lower().count(keyword.lower()), file['title']])
                count += file['payload'][0].lower().count(keyword.lower())
                cycle += 1
                if cycle == 1 or cycle == 100000:
                    logging.debug('<<<%s>>>...>' % file['payload'][0].lower().count(keyword.lower()))
                    cycle = 0
    except KeyboardInterrupt:
        logging.warning('User aborted search for keyword "%s".' % key_word)
        H(); sprint("I guess patience isn't your strong suit.")
        return

    if found:
        logging.debug('keyword "%s" appears %s times in current universe.' % (key_word, str(count)))
        try:
            found.sort()
            found.reverse()
            for title in found:
                print('%s     (%s)' % (title[1].strip(), str(title[0])))
                time.sleep(0.02)
            return
        except KeyboardInterrupt:
            return

    else:
        H(); sprint("No mentions of %s exist locally, shall I do an internet sweep for requested data?" % key_word)
        response = display_manager.input_prompt()

        if 'yes' in response:
            logging.debug('relation seeker sent "%s" to informant.' % key_word)
            H(); sprint('Doing that.')
            informant(key_word, False, 0, False, *['relation seeker'])
        else:
            controlCentre(*[response])
            return


def zen():
    """Outputs a random Koan.
    """
    H(); print('\n' + persistence.fetch_koan()) 
    return


def nearby(req):
    """Finds places related to specified subject near users location.
    """
    try:
        mid = req.find('near')
        obj = req[:9-1]
        pos = req[9+5:]
        coords = find_lc(pos)
        H();sprint('Searching for %s near %s' % (obj, pos))
        webbrowser.open('https://google.com/maps/search/%s/@%s,%s' % (obj, coords[0], coords[1]))
        return
    except Exception as e:
        rollbar.report_exc_info()
        logging.debug(str(e))
        print("Couldn't comnply. Check the logs.")
        return


def delete_latest():
    """Called after sending an email through Luna. Deletes the message just sent from 
       your mailbox's Sent Items.
    """
    numMessages = 2
    try:
        mailserver = poplib.POP3_SSL('pop.gmail.com')
        mailserver.user('recent:%s' % os.getenv('LUNADDR'))
        mailserver.pass_(os.getenv('EMAILPWD'))
        numMessages = len(mailserver.list()[1])
        mailserver.dele(numMessages)
        mailserver.quit()
        logging.info("Mail clean up successful.")
    except:
        rollbar.report_exc_info()
        logging.warn("Could not clean up mail. Manual removal required. Sorry Bud.")
        return


def porter():
    """Sends an email to a specified email address.
    """
    uheader = '['+user[0].upper()+']'
    H(); sprint("Enter payload\n")
    lines = []
    try:
        while True:
            lines.append(input(u"\u262F "))
    except EOFError:
        pass
    except KeyboardInterrupt:
        H(); sprint("Aborted.")
    payload = "\n".join(lines)
    print('\n'); H(); sprint("Label the package")
    subject = display_manager.input_prompt()

    H(); sprint("Who's the mark?")
    target = display_manager.input_prompt()

    try:
        fa = os.getenv('LUNADDR')
        if not target:  # Env vars
            ta = os.getenv('MYEMAIL')
        else:
            ta = target
        msg = MIMEMultipart()
        msg['From'] = fa
        msg['To'] = ta
        msg['Subject'] = subject
        body = payload
        msg.attach(MIMEText(body,'plain'))
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(fa, os.getenv('EMAILPWD'))
        text = msg.as_string()
        server.sendmail(fa,ta,text)
        server.quit()
        H(); sprint("Package sent.")
        delete_latest()
        return
    except:
        rollbar.report_exc_info()
        H(); sprint('Package sending failed.')
        return


def health_check():
    try:
        battery = psutil.sensors_battery()
        if battery.percent <= 20 and battery.power_plugged == False:
            H(); sprint(random.choice(low_battery_responses))
        logging.info('Battery level is at %s percent. Charging: %s' % (str(battery.percent), str(battery.power_plugged)))
    except Exception as e:
        rollbar.report_exc_info()
        logging.error(e)
        pass


def media_player(artist):
    result = [y for x in os.walk('%s/Downloads' % os.path.expanduser('~')) for y in glob(os.path.join(x[0], '*.mp3'))]
    for file in result:
        if artist.lower() in file.lower():
            os.system('xdg-open "%s"' % file)
            return
    H(); sprint('Could not find any %s' % artist)
    return


def lightIntel(): # a misnomer now
    try:
        page1 = requests.get('https://washingtonpost.com')
        tree1 = html.fromstring(page1.content)
        page2 = requests.get('https://techcrunch.com')
        tree2 = html.fromstring(page2.content)

        excerpt = tree2.xpath('//a[@class="post-block__title__link"]/text()')
        H(); print("\n\nTechCrunch:\n")
        articles = tree2.xpath('//a[@class="post-block__title__link"]/text()')
        for i in articles:
            print(i.strip())
            time.sleep(0.03)

        headlinez = tree1.xpath('//a[@data-pb-placeholder="Write headline here"]/text()')
        stutter("\nWashington Post:\n")
        time.sleep(1)
        for i in headlinez:
            print(i)
            time.sleep(0.03)

    except KeyboardInterrupt as e:
        H(); sprint('Aborted.')
    except Exception as e:
        rollbar.report_exc_info()
        logging.debug(str(e))
        H(); sprint(random.choice(error_responses))
    finally:
        return


def laFibonacci():
    H(); sprint('The first two numbers are 1 and 1. Continue the sequence. The last one standing wins (I always win).')
    straws = [1,2]
    firstGo = random.choice(straws)
    if firstGo == 1:
        H(); sprint("I'll go first.")
        lunasTurn(1,1,0)
    else:
        usersTurn()


def usersTurn(n1=1, n2=1, depth=0):
    try:
        start = time.time()
        nextInt = n1+n2
        try:
            userNext = display_manager.input_prompt()
            test = int(userNext)
        except Exception as e:
            logging.error(e)
            return

        end = time.time()
        gameOver = False

        if int(end - start) > 10:
            H(); sprint('You took too long. Your max depth is %s.' % depth)
            start_over()

        if int(userNext) != nextInt:
            H(); sprint('Cute. Max depth is %s.' % depth)
            gameOver = True

        if gameOver:
            start_over()
            # todo: save high score to file. Sustain if depth is lower.
        else:
            n1 = n2
            n2 = nextInt
            depth += 1
            lunasTurn(n1, n2, depth)
    except KeyboardInterrupt as e:
        H(); sprint("Sequence terminated.")
        return


def start_over():
    H(); sprint('Would you like to start over?')
    directive = display_manager.input_prompt()

    if 'yes' in directive:
        laFibonacci()
    else:
        H(); sprint("Cool. It was nice reminding you who's the boss around here.")
        return


def lunasTurn(n1,n2,depth):
    nextInt = n1+n2
    n1 = n2
    n2 = nextInt
    H(); time.sleep(2);print(nextInt)
    usersTurn(n1, n2, depth)


# def port_1():
#     try:
#         hh.append(user_input_tag)
#         H(); sprint('Enter code name')
#         cn = input(user_input_tag)
#         H(); sprint('Enter text')
#         txt = input(user_input_tag)
#         save_in_db(cn, txt)
#     except KeyboardInterrupt as e:
#         print('Aborted.')
#         return


def save_in_db(code_name, obj):
    entry = {
             '_id': str(uuid.uuid4()),
             'code_name': code_name,
             'date': str(datetime.datetime.now()),
             'payload': [obj]
    }
    files.insert_one(entry)
    H();sprint("New file stored successfully.")
    return


"""
host_handler():
    q1 = input('Would like to add or remove a host to the black list?')
    if 'add' in q1:
        #under construction
"""

dict_header = '\n[' + Fore.LIGHTBLACK_EX + 'DICT' + Fore.RESET + '] '

def dictionary():
    try:
        H(dict_header); print("Choose a dictionary database (enter the associated number)\n\n",
             "1. The Collaborative International Dictionary of English\n",
             "2. Wordnet (2006)\n",
             "3. The Devil's Dictionary (1881-1906)\n",
             "4. The Moby Thesaurus II by Grady Ward")
        dic = display_manager.input_prompt()
        mapper = { '1': 'gcide', '2': 'wn', '3': 'devil', '4': 'moby-thesaurus' }
        mapper2 = {
            '1': 'The Collaborative International Dictionary of English',
            '2': 'Wordnet (2006)',
            '3': "The Devil's Dictionary (1881-1906)",
            '4': 'The Moby Thesaurus II by Grady Ward'
        }
        H(dict_header); sprint("You are now in %s" % mapper2[dic])
        dictionaryHelper(mapper[dic])
    except KeyboardInterrupt:
        H(); sprint('Aborted')
        return


def dictionaryHelper(dictionary):
    # todo: auto suggest from wordlist
    # print(dict_header, end='')
    # word = prompt('', history=FileHistory('wordlist.txt'), auto_suggest=AutoSuggestFromHistory())
    word = display_manager.input_prompt()

    if word != 'exit':
        try:
            H(dict_header); os.system('dict -d %s %s' % (dictionary, word))
            dictionaryHelper(dictionary)
        except Exception as e:
            rollbar.report_exc_info()
            H(); sprint(e)
            return
    else:
        H(); sprint('Dictionary closed.')
        return
