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

import requests
import datetime, time
import json
import uuid
from lxml import html
import rollbar
from geopy.geocoders import Nominatim
from colorama import Fore
from func_timeout import func_timeout, FunctionTimedOut
from func_timeout.StoppableThread import StoppableThread
from persistence import index as persistence
from functions.display_manager import main as display_manager
from functions.responses import *
from annoyances import *


LOCAL_TIMEZONE = str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)

layout = Nominatim()

dialogue_speed = 0.01
shit_times = 1
cycles = 1


def get_coords():
    logging.debug('Establishing spatial awareness.')
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


def find_lc(city):
    """Converts city name to latitude-longitude values.

           params:
               city (string) : name of the city to be converted.
    """
    # logging.debug('find_lc recived %s' % city)
    global shit_times
    try:
        lc = layout.geocode(city)
        shit_times = 0
        return [lc.latitude, lc.longitude]
    except:
        if shit_times <= 10:
            shit_times += 1
            find_lc(city)
        else:
            shit_times = 0
            return 'booper'


def get_weather(void=False, api_request=False, *city):
    logging.info('Running in target')
    """Finds the weather of a specified city. Outputs either a converstional string or
       returns JSON or runs silently and stores output in database.
    """
    # if city:
        # logging.debug('weather recieved %s' % city)
    global cycles

    try:
        if not city:
            coords = get_coords()

        else:
            coords_raw = find_lc(city[0])
            if coords_raw != 'blooper':
                coords = []
                try:
                    for coord in coords_raw:
                        c = str(coord)
                        coords.append(c[:8])
                except TypeError:
                    logging.error('no coordinates for city: {}'.format(city))
                    pass

        page = requests.get('https://darksky.net/forecast/%s,%s/si24/en' % (coords[0], coords[1]))
        tree = html.fromstring(page.content)
        minTemp = tree.xpath('//span[@class="minTemp"]/text()')
        maxTemp = tree.xpath('//span[@class="maxTemp"]/text()')
        windhumidity = tree.xpath('//span[@class="num swip"]/text()')
        skystatus = tree.xpath('//span[@class="summary swap"]/text()')[0].lower()
        humidity = windhumidity[1]+'%'
        windspeed = windhumidity[0]+'m/s'
        currenttemp = skystatus[:3]+'c'
        maxtemp = maxTemp[0]+'c'
        mintemp = minTemp[0]+'c'
        visibility = windhumidity[2]+'km'
        pressure = windhumidity[3]+'hPa'
        logging.debug('alpha')
        cloud_cover = ['clear.', 'partly cloudy.', 'overcast.', 'cloudy.',
                       'mostly cloudy.', 'ostly cloudy']

        temp_descOpts = ['freezing ', 'chilly ', 'warm ', 'hot ', 'blazing ']

        integers = ['0', '1','2','3','4','5','6','7','8','9']
        temp_num = []
        for i in skystatus:
            if i in integers:
                temp_num.append(i)
        tempState = int(''.join(temp_num))

        # TODO: add 15 - 20 = cool. Rearrange other values as necessary.
        if tempState < 10:
            descr = temp_descOpts[0]
        elif tempState >= 10 and tempState <= 15:
            descr = temp_descOpts[1]
        elif tempState >= 15 and tempState <= 23:
            descr = temp_descOpts[2]
        elif tempState >= 23 and  tempState <= 30:
            descr = temp_descOpts[3]
        elif tempState > 30:
            descr = temp_descOpts[4]

        if skystatus[4:] in cloud_cover:
            prefix = 'Skies are '

        else:

            if city:
                prefix = 'This location is currently experiencing '

            else:
                prefix = 'Our current position is experiencing '


        t = tree.xpath('//div[@class="summary"]/text()')
        l = t[0]

        if city:
            a1 = "\n%s's temperature range: " % city[0].title()
            a2 = ".\nCurrent temperature: a "

        else:
            a1 = "\nCurrent temperature range: "
            a2 = ".\nCurrent temperature: a "

        ll = l.strip().lower()

        weather_json = {
                        '_id': str(uuid.uuid4()),
                        'date': str(datetime.datetime.now()),
                        'collectedFromTimezone': LOCAL_TIMEZONE,
                        'location': {
                                     'latitude': coords[0],
                                     'longitude': coords[1]
                                    },
                        'data': {
                                 'mintemp': mintemp,
                                 'maxtemp': maxtemp,
                                 'currentTemp': currenttemp,
                                 'humidity': humidity,
                                 'windspeed': windspeed,
                                 'skystatus': skystatus[4:],
                                 'visibility': visibility,
                                 'pressure': pressure
                                }
                        }

        logging.debug('bravo')
        logging.info('Constructed weather JSON: %s' % weather_json)
        # research.insert_one(weather_json)
        # for file in research.find():
        #     pprint.pprint(file)
        if void:
            return
        if api_request:
            return json.dumps(weather_json)
        else:
            if not void:
                display_manager.output_prompt; sprint(
                            a1 + mintemp + " => " + maxtemp + a2 + descr + currenttemp
                            + "\nHumidity: " + humidity
                            + "\nWind speed: " + windspeed + "\n\n" + prefix
                            + skystatus[4:] + " " + t[1] + "\n" + random.choice(weather_prediction_prefix)
                            + ll
                      )
        logging.debug('charlie')
        cycles = 0
        return

    except KeyboardInterrupt as e:
        logging.debug('User interupted weather request.')
        display_manager.output_prompt; sprint("Aborted.")
        print('\n');
        return

    except Exception as e:
        rollbar.report_exc_info()
        logging.error(str(e))
        if void:
            return
        if city:
            if cycles < 10:     # times out after 10 attempts
                cycles += 1     # TODO: it would be best to differentiate between no-internet
                get_weather(void, api_request, *city)  # and bad connection errors.
            else:
                logging.debug(str(e))
                display_manager.output_prompt; sprint("Couldn't. Check the logs.")
                return
        else:
            if void:
                return
            else:
                logging.debug(str(e))
                display_manager.output_prompt; sprint("Couldn't. Check the logs.")
                return
