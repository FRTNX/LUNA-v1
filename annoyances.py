import os
import rollbar
import random
import logging
from colorama import Fore

beam = "-------------------------------------------------------------------------------"
semi = "                    --------------------------------------"
solid_semi = "__________________________________"

logFormatter = logging.Formatter(Fore.BLUE + '[LUNA] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]' + Fore.RESET + ' %(message)s')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("{0}/{1}.log".format('logs/', 'luna'))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
os.system("gnome-terminal --geometry=130x128+0+200 -e 'tail -f logs/luna.log'")
os.system('python3 resources/banners/logs_banner1.py')
server_banner = open('resources/banners/logs_banner1.txt', 'r').read()
rootLogger.debug(server_banner)
rootLogger.info('Beginning orientation.')
rollbar.init('e0327e81b0294b24b80a0d9723fd574d')

climate_monitor = [
                   'Hamgyong',
                   'Kangwon', 
                   'Gedo, Somalia',
                   'Middle Juba',
                   'Lower Juba',
                   'Lower Shebelle',
                   'Middle Shebelle',
                   'Hiran, Somalia',
                   ]
# 'Ͼ μ ή Δ'