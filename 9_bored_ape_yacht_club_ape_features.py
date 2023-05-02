
#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as soup
import requests
import urllib
import re
import pandas as pd
import time
import json
import pymongo
import xmltodict
import copy
import html_to_json
import http.client
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint




######################## Info inserted to databases is printed before inserted
######################## Remember to change the location of chromediver



###########################################################################################
######################## Selenium x MongoDB x Bored Ape Yacht Club ########################
###########################################################################################


###########################################################################################
#################### Get the URL of 'solid gold' fur bape with price ranged from high to low
#################### loop the 8 pages and save them to disk
###########################################################################################

def main1():
    try:

        url = 'https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold'


        # Loop and save 8 page
        driver = webdriver.Chrome(executable_path='/chromedriver_mac_arm64/chromedriver')


        for i in range (8):
            driver.implicitly_wait(10)
            driver.set_script_timeout(300)
            driver.set_page_load_timeout(300)
            driver.get(url)
            
            bape = driver.find_element("css selector", "div.sc-29427738-0.jFfKPa > div.sc-29427738-0.dVNeWL > div > div:nth-child("+ str(i+1) + ")> article > a > div.sc-29427738-0.sc-d17323ed-6.wOaQH.mCJzn > div > div > div > div > span > img").click()
            time.sleep(11)
            
            html_from_page = driver.page_source
            
            File = open(f"bayc_{i+1}.html","w", encoding='utf-8')
            File.write(html_from_page)
            print("Bape " +str(i+1)+ " captured")
            time.sleep(2)
            
        driver.quit()

    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    main1()








    
###########################################################################################
#################### Loop the 8 html files downloaded in (2) and stores each ape’s name (its number) and all its attributes in a document inside a MongoDB collection called “bayc”.
###########################################################################################

def main2():
    try:
        # create a db
        client = pymongo.MongoClient('localhost:27017')
        db = client["individual_project"]
        bape = db["bayc"]



        bape_index_1 = []
        bape_name_1=[]
        bape_clothes_1=[]
        bape_background_1=[]
        bape_eyes_1=[]
        bape_earring_1=[]
        bape_hat_1=[]
        bape_fur_1=[]
        bape_mouth_1 =[]


        for i in range(8):
            # load the page
            page = soup(open(f'./bayc_{i+1}.html','r').read(), 'lxml')

            
            
            
            # get the bape title
            bape_title = page.find('h1',{'class':'sc-29427738-0 hKCSVX item--title'})
            print(f"Bape Name: {bape_title.text}")
            bape_name_1.append(bape_title.text)
            

            
            property_type_1 = page.find_all('div',{'class': 'Property--type'})[0]
            if property_type_1.text == 'Background':
                property_bg = page.find_all('div',{'class': 'Property--value'})[0]
                bape_background_1.append(property_bg.text)
                print(bape_background_1)
            else:
                property_bg = page.find_all('div',{'class': 'Property--value'})[1]
                bape_background_1.append(property_bg.text)
                print(bape_background_1)
            
            
            
            property_type_2 = page.find_all('div',{'class': 'Property--type'})[1]
            if property_type_2.text == 'Clothes':
                property_clothes = page.find_all('div',{'class': 'Property--value'})[1]
                bape_clothes_1.append(property_clothes.text)
                print(bape_clothes_1)
            else:
                property_clothes = page.find_all('div',{'class': 'Property--value'})[2]
                bape_clothes_1.append(property_clothes.text)
                print(bape_clothes_1)
                
                
                
                
            
            property_type_3 = page.find_all('div',{'class': 'Property--type'})[2]
            if property_type_3.text == 'Earring':
                property_eyes = page.find_all('div',{'class': 'Property--value'})[3]
                bape_eyes_1.append(property_eyes.text)
                print(bape_eyes_1)
            else:
                property_eyes = page.find_all('div',{'class': 'Property--value'})[2]
                bape_eyes_1.append(property_eyes.text)
                print(bape_eyes_1)
                
                
                
            property_type_4 = page.find_all('div',{'class': 'Property--type'})[3]
            if property_type_4.text == 'Eyes':
                property_fur = page.find_all('div',{'class': 'Property--value'})[4]
                bape_fur_1.append(property_fur.text)
                print(bape_fur_1)
            else:
                property_fur = page.find_all('div',{'class': 'Property--value'})[3]
                bape_fur_1.append(property_fur.text)
                print(bape_fur_1)
                
                
                
                
            property_type_5 = page.find_all('div',{'class': 'Property--type'})[4]
            if property_type_5.text == 'Fur':
                property_hat = page.find_all('div',{'class': 'Property--value'})[5]
                bape_hat_1.append(property_hat.text)
                print(bape_hat_1)
            else:
                property_hat = page.find_all('div',{'class': 'Property--value'})[4]
                bape_hat_1.append(property_hat.text)
                print(bape_hat_1)
            
            
            
            
            
            property_type_6 = page.find_all('div',{'class': 'Property--type'})[2]
            if property_type_6.text == 'Earring':
                property_earring = page.find_all('div',{'class': 'Property--value'})[2]
                bape_earring_1.append(property_earring.text)
                print(bape_earring_1)
            else:
                bape_earring_1.append('')
                print(bape_earring_1)
                
            
            property_type_7 = page.find_all('div',{'class': 'Property--type'})[-1]
            if property_type_7.text == 'Mouth':
                property_mouth = page.find_all('div',{'class': 'Property--value'})[-1]
                bape_mouth_1.append(property_mouth.text)
                print(bape_mouth_1)

        # put all lists in a df


        df1 = pd.DataFrame(
                    {'name': bape_name_1,
                     'background': bape_background_1,
                     'clothes':bape_clothes_1,
                     'earring': bape_earring_1,
                     'eyes': bape_eyes_1,
                     'fur':bape_fur_1,
                     'hat': bape_hat_1,
                     'mouth':bape_mouth_1
                    })




        db.bayc.insert_many(df1.to_dict('records'))
        print('All 8 bapes inserted to MongoDB collection bayc')

        # should work fine if all of the 8 bapes have at least 6 attributes
        # but the data could be inserted to the wrong column if any bape has less or equal to 5 attributes

    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    main2(),'',str(store_ameneties))amenity-alcohol"><\/use>',',',str(store_ameneties))amenity-family"><\/use>',',',str(store_ameneties))es)):,'',str(store_ameneties))amenity-alcohol"><\/use>',',',str(store_ameneties))amenity-family"><\/use>',',',str(store_ameneties))es))rt=True)