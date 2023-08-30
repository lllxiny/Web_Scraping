#!/usr/bin/env python


from bs4 import BeautifulSoup as soup
import requests
import urllib
import re
import pandas as pd
import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint


# # Selenium ChromeDriver search practice


# search for askew

def main1():
    try:
        driver = webdriver.Chrome(executable_path='/Users/liuxinyu/chromedriver_mac_arm64/chromedriver')
        driver.implicitly_wait(10)
        driver.set_script_timeout(120)
        driver.set_page_load_timeout(10)
        driver.get("https://google.com")
        inp = driver.find_element("css selector", "input[type=text]")
        inp.send_keys("askew\n")
    except:
        print('Error')

if __name__ == '__main__':
    main1()



# search for google in 1998
def main2():
    try:
        driver = webdriver.Chrome(executable_path='/Users/liuxinyu/chromedriver_mac_arm64/chromedriver')
        driver.implicitly_wait(10)
        driver.set_script_timeout(120)
        driver.set_page_load_timeout(10)
        driver.get("https://google.com")
        inp = driver.find_element("css selector", "input[type=text]")
        inp.send_keys("google in 1998\n")
    except:
        print('Error')

if __name__ == '__main__':
    main2()
