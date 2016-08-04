# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 15:32:42 2016

@author: Marcus Therkildsen
"""

from __future__ import division
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

"""
This script logs into jobnet.dk and autochecks the "jobs" recommended from them.
If this is not done reguarly you basically cannot get "dagpenge"

On a Raspberry Pi, install selenium with

sudo apt-get install python-pip
sudo pip install selenium

Also get PhantomJS from here https://github.com/spfaffly/phantomjs-linux-armv6l
and follow the instructions

Remember full path to phantomjs as well as to the config file when putting into crontab -e
Like so: executable_path='/home/pi/jobnet/phantomjs'
"""

def check_jobnet(log_pass):

    # Sleep time (10 on the Pi)
    sleep_time = 10

    # URL to the 11th prog mission
    url_data = 'https://job.jobnet.dk/CV/frontpage'

    # Open in Firefox/PhantomJS/
    driver = webdriver.PhantomJS(executable_path='/home/pi/jobnet/phantomjs')
    #driver = webdriver.PhantomJS(executable_path='./phantomjs')
    #driver = webdriver.Chrome(executable_path='./chromedriver')

    # Load the page
    driver.get(url_data)

    # Username
    inputElement = driver.find_element_by_name('Username')
    inputElement.send_keys(log_pass['jobnet']['name'])

    # Password
    inputElement = driver.find_element_by_name('Password')
    inputElement.send_keys(log_pass['jobnet']['password'])

    # Enter
    inputElement.send_keys(Keys.ENTER)
    time.sleep(sleep_time)

    # Find the "tjek jobs" button
    check_button = driver.find_element_by_id('TjobButton')

    # Enter
    check_button.send_keys(Keys.ENTER)
    time.sleep(sleep_time)

    # Get the source code
    source = driver.page_source

    # Search for verification
    search_word = 'vi har nu registreret, at du har tjekket dine jobforslag'
    found = source.find(search_word)

    # Logout
    url_data = 'https://job.jobnet.dk/CV/logout.aspx'
    driver.get(url_data)
    time.sleep(sleep_time)

    # Close webdriver
    driver.close()

    return found


def send_mail(message, log_pass):

    import smtplib

    # Sender and receiver
    s = log_pass['mail']['sender']
    s_pass = log_pass['mail']['sender password']
    r = log_pass['mail']['receiver']

    # Email server and port
    mail = smtplib.SMTP(log_pass['mail']['server'], log_pass['mail']['port'])
    mail.ehlo()
    mail.starttls()
    mail.login(s, s_pass)

    # Header needed
    header = 'To:' + r + '\n' + 'From: ' + s + '\n' + 'Subject:Jobnet tjek \n'
    content = header + '\n ' + message + ' \n\n'
    mail.sendmail(s, r, content)
    mail.close()

if __name__ == '__main__':

    # Load credentials (json file is implicitly closed automatically)
    with open('/home/pi/jobnet/config.json') as json_data:
        log_pass = json.load(json_data)

    try:
        status = check_jobnet(log_pass)
    except Exception:
        status = -1

    if status > -1:
        #print("Jobnet tjekket")
        pass
    elif status == -1:
        #print("Jobnet ikke tjekket, noget fuckede")
        send_mail("Noget gik galt da jeg ville lave automatisk tjek hos jobnet.dk Plizz fix.", log_pass)
