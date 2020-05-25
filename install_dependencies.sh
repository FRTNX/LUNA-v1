#!/bin/sh

sudo apt-get update
sudo apt-get -y install build-essential
sudo apt-get -y install python3-setuptools
sudo apt-get -y install python3-pip
pip3 install conda
conda create -y --name luna python=3.6
source activate luna
sudo apt-get update
# sudo apt-get upgrade
sudo apt install whois
sudo apt-get -y install wget
sudo apt-get -y install traceroute
sudo apt-get -y install htop
sudo apt-get -y install macchanger macchanger-gtk
sudo apt-get -y install xbacklight
sudo apt -y install speedtest-cli speedtest-cli
sudo apt-get -y install htop

# todo: Postgres Setup
sudo apt-get install postgresql postgresql-contrib


# Python dependencies
pip3 install pillow --user
pip3 install Pillow --user
pip3 install lxml --user
pip3 install google --user
pip3 install googletrans --user
pip3 install aiml --user
pip3 install rollbar --user
pip3 install geocoder --user
pip3 install twython --user
pip3 install bs4 --user
pip3 install psutil -- user
pip3 install ipgetter --user
pip3 install colorama --user
pip3 install wikipedia --user
pip3 install ipgetter --user
pip3 install nltk --user
pip3 install matplotlib --user
pip3 install geopy==1.11.0 --user
pip3 install google_images_download --user
pip3 install inflect --user --user
pip3 install rasa-nlu==0.13.7
pip3 install service_identity --user
pip3 install tensorflow --user
pip3 install sklearn --user
pip3 install sklearn-crfsuite --user
pip3 install scipy --user
pip3 install wolframalpha --user
pip3 install psycopg2 --user
pip3 install -U pytest
pip3 install pytest-mock --user
pip3 install func-timeout --user
pip3 install prompt_toolkit --user
pip3 install webbrowser --user


# finally copy the nltk folder into host machines home dir

