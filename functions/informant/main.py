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
from PIL import Image
from colorama import Fore
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

def H(*n):
    if not n:
        print(output_prompt, end='');
    else:
        print(n[0], end='')
    time.sleep(0.2)


def is_online():
    try:
        wikipedia.page('science')
        return True
    except ConnectionError as e:
        return False
    except Exception as e:
        logging.debug(f'Error running connection tests: {e}')
        return False


def reset_prompt():
    global found
    found = True
    time.sleep(0.01)
    print("\033[A                             \033[A")


def fetch_and_display_images(subject, image_urls=[]):
    if image_urls == []:
        try:
            logging.info(f'Extracting image urls for: {subject}')
            res = wikipedia.page(subject)
            image_urls = res.images
            logging.info(f'Got image urls: {image_urls}')
        except Exception as e:
            logging.error(e)
            return

    render_images = StoppableThread(target=display_manager.fetch_images, args=(subject, image_urls,))
    render_images.daemon = True
    render_images.start()



def informant(mark, images=True, latency=0, flesh=False, first_call=True, search_online=False):
    """Looks for specified subject in local database and looks for it on wikipedia if not found.
       Also searches for images subject.

       params:
           mark (string)  : the subject/object being sought (e.g., Physics, Barack Obama, Milk, Proximal Policy Optimisation, ...etc)
           images (boolean) : look for images on a parallel thread. set to False to disable.
           latency (int)    : if no data is found locally on subject, the time spent running this process up to this
                              point is inserted as the value here and this function is called again from within itself,
                              this time with a flag indicating that the local database is to be ignored and an internet
                              search to be conducted immediately if possible.
           flesh (boolean)  : controls whether to display introductory article summary or article detail. Set to True when seeking
                              article detail and False when only a summary is required.
           search_online    : if True the local database is ignored and the request goes straight to wikipedia.org
    """

    # logging.debug('informant recieved: %s' % mark)
    logging.info('Requested document "%s".' % mark)
    logging.info(f'Inherited latency: {latency} seconds')
    logging.info(f'First call: {first_call}')
    logging.info(f'Search online: {search_online}')

    global found

    if search_online:
        render_ellipses = StoppableThread(target=ellipses)
        render_ellipses.daemon = True
        render_ellipses.start()

    if first_call and images and not search_online:
        render_images = StoppableThread(target=fetch_and_display_images, args=(mark,))
        render_images.daemon = True
        render_images.start()

    try:
        if search_online:
            try:
                logging.warn('Nature of request requires internet. Attempting to connect')
                start = time.time()
                res = func_timeout(8, wikipedia.page, args=(mark,))
                if first_call and images:
                    image_urls = res.images
                    render_images = StoppableThread(target=fetch_and_display_images, args=(mark, image_urls,))
                    render_images.daemon = True
                    render_images.start()

                content = res.content
                title = res.title
                slice_limit = content.find('\n\n\n')
                reset_prompt()
                display_manager.output_prompt(); display_manager.output_prompt(); print(gbullet + '\n')
                end = time.time()
                logging.info('"%s" found. latency is at %s seconds.' % (title, str(end - start + latency)))

                if flesh:
                    logging.info('Fleshing out requested document.')
                    action = directive(content, title, slice_limit + 3, *['flesh'])
                    return action

                if 'displaystyle' not in content[:slice_limit] and 'textstyle' not in content[:slice_limit]:
                    sprint(content[:slice_limit], 0.015)
                else:
                    output_controller(content[:slice_limit])

                action = directive(content, title, slice_limit, *['enable-saving'])
                logging.info(f'Returning {action} to caller for real this time')
                return action

            except KeyboardInterrupt as e:
                print('\n')
                found = True
                action = directive(content, title, slice_limit, *['enable-saving'])
                return action

            except FunctionTimedOut:
                end = time.time()
                reset_prompt()
                logging.error('Request for %s timed out. Request took %s seconds' % (mark, end - start + latency))
                display_manager.output_prompt(); display_manager.output_prompt(); sprint('We seem to have a really bad internet connection. Try again when conditions improve.')
                return

            except wikipedia.PageError as e:
                logging.error(e)
                reset_prompt()
                display_manager.output_prompt(); display_manager.output_prompt(); sprint("I couldnt find anything on %s in my online repositories." % mark)
                display_manager.output_prompt(); sprint('Perhaps try a different alias.')
                return

            except wikipedia.DisambiguationError as e:
                logging.error(e)
                reset_prompt()
                display_manager.output_prompt(); display_manager.output_prompt(); sprint("'%s' refers to too many things. Try being more specific." % mark)
                return

            except Exception as e:
                logging.error(e)
                reset_prompt()
                # todo: resolve malfomrmed output here
                display_manager.output_prompt(); display_manager.output_prompt(); sprint(random.choice(bad_connection_responses))
                rollbar.report_exc_info()
                utils.queue_for_extraction(mark)
                return

        else:
            try:
                start = time.time()
                content = func_timeout(2, persistence.get_document, args=('intelligence', mark,))
                slice_limit = content.find('\n\n\n')
                end = time.time()
                logging.info('"%s" found. latency is at %s seconds.' % (mark, str(end-start+latency)))
                display_manager.output_prompt(); sprint(bullet + "\n")

                if flesh:
                    logging.info('Fleshing out requested document.')
                    action = directive(content, mark, slice_limit + 3, *['flesh'])
                    return action

                if 'displaystyle' not in content[:slice_limit] and 'textstyle' not in content[:slice_limit]:
                    sprint(content[:slice_limit], 0.015)
                else:
                    output_controller(content[:slice_limit])

                action = directive(content, mark, slice_limit, *['savenot'])
                return action

            except KeyboardInterrupt as e:
                print('\n')
                action = directive(content, mark, slice_limit, *['savenot'])
                return action

            except FunctionTimedOut:
                end = time.time()
                logging.error('Could not find requested document locally within acceptable time.')
                logging.warning('Attempting to find requested document online.')
                informant(mark, False, end-start, flesh, False, *['engagethehive'])
                return

            except TypeError:
                end = time.time()
                logging.error('Could not find requested document locally.')
                logging.warning('Attempting to find requested document online.')
                informant(mark, False, end-start, flesh, False, True)
                return

            except Exception as e:
                logging.error(e)
                rollbar.report_exc_info()
                return

    except KeyboardInterrupt as e:
        return
    except Exception as e:
        logging.debug(str(e))
        return


def directive(content, title, interm, *mode):
    """This fuction is informants() helper. It can save or show more data from the
       data displayed by informant. If user request is neither of these two actions
       it is sent to NLU and coordinated as necessary.
    """
    if mode and mode[0] == 'flesh':
        text_normaliser(content[interm:])

    action = display_manager.input_prompt()

    if (not mode) or (mode[0] != 'flesh') and ('more' in action):
        logging.info('Displaying the rest of document "%s".' % title)
        if 'displaystyle' not in content[interm:] and 'textstyle' not in content[interm:]:
            display_manager.output_prompt(); print(content[interm:])
            directive(content, title, interm, *['break'])
        else:
            display_manager.output_prompt(); output_controller(content[interm:], True)
            directive(content, title, interm, *['break'])

    elif action == 'save':
        try:
            insertion_res = persistence.insert_document('intelligence', title, content)
            logging.info(insertion_res)
            display_manager.output_prompt(); sprint("Saved.")
            return

        except ValueError as e:
            logging.error(e)
            display_manager.output_prompt(); sprint("Previous intell already exists. Update?[yes/no]")
            user_action = display_manager.input_prompt().lower()

            if user_action == 'yes':
                try:
                    old_entry = persistence.get_document('intelligence', title)
                    insertion_res = persistence.insert_document('archive', title, old_entry)
                    logging.info(insertion_res)
                    deletion_res = persistence.delete_document(title)
                    logging.info(deletion_res)
                    insertion_res = persistence.insert_document('intelligence', title, content)
                    logging.info(insertion_res)
                    display_manager.output_prompt(); sprint("Done.")
                    return

                except Exception as e:
                    rollbar.report_exc_info()
                    logging.error(str(e))
                    display_manager.output_prompt(); sprint('I ran into trouble. Check the logs.')
                    return
            else:
                if user_action == 'no':
                    display_manager.output_prompt(); sprint("Old entry sustained.")
                    return
        except Exception as e:
            rollbar.report_exc_info()
            logging.error(str(e))
            display_manager.output_prompt(); sprint('I ran into trouble. Check the logs.')
            return

    elif action.lower() == 'pin':
        result = persistence.update_doc_flags('intelligence', title, 'PIN_TO_START')
        logging.debug(result)
        if (result.startswith('Success')):
            display_manager.output_prompt(); sprint('Pinned.')
        else:
            display_manager.output_prompt(); sprint('I couldnt pin this article. Check the logs.')
        return

    else:
        logging.info(f"Returning '{action}' to caller")
        return action


def ellipses():
    global found
    logging.info(f'Is article found: {found}')
    found = False
    count = 0
    unit = '.'
    print('')

    while not found:
        try:
            os.system('setterm -cursor off')
            sys.stdout.write('\r{}                                        '.format(output_prompt.strip('\n') + unit * count))
            sys.stdout.flush()

            if count == 3:
                count = 0
            else: 
                count += 1
                time.sleep(0.2)

        except KeyboardInterrupt as e:
            print("\033[A                             \033[A")
            os.system('setterm -cursor on')
            found = True
            break

    print("\033[A                             \033[A")
    os.system('setterm -cursor on')
    found = False
    return

def output_controller(content, plain=False):
    """Handles the display of mathematical equations and other specially formatted text.
    """
    logging.info('Output controller invoked.')
    x = content.split('\n')
    safe_words = ['is', 'or', 'to']
    for i in x:
        if len(i.replace(' ','')) <= 2 and i.replace(' ','') not in safe_words:
            print(i.replace(' ',''), end='')
        elif 'displaystyle' in i or 'textstyle' in i:
            print('\n')
        else:
            if '==' in i:
                print('\n')
            if not plain:
                sprint(i)
            else:
                print(i)
    return

def text_normaliser(text):
    """Seeks out custom formatted text styles such as mathematical equations within an text (here
       refered to as 'flesh'). If custom text exists output_controller() is invoked, else it
       is printed as is.
    """
    if 'displaystyle' not in text and 'textstyle' not in text:
        print(text)
    else:
        output_controller(text, True)
    return
