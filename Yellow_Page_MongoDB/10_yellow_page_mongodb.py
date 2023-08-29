
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
######################## Yellow Page Pizzeria #############################################


###########################################################################################
#################### Save 30 searchresults on one page as one file 
###########################################################################################


    

def main1():
    try:

        # define url
        url = 'https://www.yellowpages.com/search?search_terms=pizzeria&geo_location_terms=San%20Francisco%2C%20CA&page=1'




        # save page
        yp_all = requests.get(url)
        yp_results = yp_all.text

        with open(f'./sf_pizzeria_search_page.html','w', encoding='utf8') as fullPage:
                    fullPage.write(yp_results)
                    print('Search result page printed')

    except Exception as ex:
        print('error: ' + str(ex))


if __name__ == '__main__':
    main1()







###########################################################################################
####################  Get info from the page saved and print them to screen
###########################################################################################


def main2():
    try:
        
        # open page
        for i in range(1):
            yp_soup = soup(open(f'./sf_pizzeria_search_page.html','r').read(), 'lxml')
            results = yp_soup.find('div',{'class':'search-results organic'})


        # abstract information from all of the restaurants

        for result in results.children:


            
            ### search rank
            search_rank = result.find('h2',{'class':'n'})
            if search_rank is not None:
                search_rank = result.find('h2',{'class':'n'})
                search_rank = re.findall('\d+',str(search_rank.text))
                print('Rank: ',search_rank[0])

                
            
            ### name
            search_name = result.find('a',{'class':'business-name'})
            if search_name is not None:
                print('Name: ',search_name.text)
                

                
            ### store’s YP URL
            store_link_soup = result.find('a',{'class':'business-name'})
            if store_link_soup is not None:
                store_link = store_link_soup.get('href')
                print('https://www.yellowpages.com'+store_link)
            

            
            ### star rating five
            store_rating_5 = result.find('div',{'class':'result-rating five'})
            if store_rating_5 is not None:
                print('Store Star Rating: 5 Stars')
            
            ### star rating four.five
            store_rating_45 = result.find('div',{'class':'result-rating four half'})
            if store_rating_45 is not None:
                print('Store Star Rating: 4.5 Stars')

            ### star rating four
            store_rating_4 = result.find('div',{'class':'result-rating four'})
            if store_rating_4 is not None:
                print('Store Star Rating: 4 Stars')
            
            ### star rating three.five
            store_rating_35 = result.find('div',{'class':'result-rating three half'})
            if store_rating_35 is not None:
                print('Store Star Rating: 3.5 Stars')
            
            ### star rating three
            store_rating_3 = result.find('div',{'class':'result-rating three'})
            if store_rating_3 is not None:
                print('Store Star Rating: 3 Stars')
            
            ### star rating two half
            store_rating_25 = result.find('div',{'class':'result-rating two half'})
            if store_rating_25 is not None:
                print('Store Star Rating: 2.5 Stars')
            
            ### star rating two
            store_rating_2 = result.find('div',{'class':'result-rating two'})
            if store_rating_2 is not None:
                print('Store Star Rating: 2 Stars')
            
            ### star rating one half
            store_rating_15 = result.find('div',{'class':'result-rating one half'})
            if store_rating_15 is not None:
                print('Store Star Rating: 1.5 Stars')
                
            ### star rating one
            store_rating_1 = result.find('div',{'class':'result-rating one'})
            if store_rating_1 is not None:
                print('Store Star Rating: 1 Star')
            
            
            
            # number of reviews(after the star icons)
            star_section = result.find('span',{'class':'count'})
            star_section = re.sub('<span class="count">\(','',str(star_section))
            star_section = re.sub('\)<\/span>','',str(star_section))
            print('Number of reviews: ',star_section)
            
            
            
            ### ta rating
            store_ratings = result.find_all('div',{'class':'ratings'})
            for store_rating in store_ratings:
                store_rating_result = str(store_rating.attrs)
                store_rating_result = re.sub('((.+)\{\")','',store_rating_result)
                store_rating_result = re.sub('(\,\"(.+))','',store_rating_result)
                store_rating_result = re.sub('(\{\'class(.+))','None',store_rating_result)
                store_rating_result = re.sub('(rating\"\:\")','',store_rating_result)
                store_rating_result = re.sub('\"','',store_rating_result)
                
                print('Trip Advisor Rating: ',store_rating_result)
            
            
            
            # ta comments
            store_ta_comments = result.find_all('div',{'class':'ratings'})
            for store_ta_comment in store_ta_comments:
                store_ta_comment_result = str(store_ta_comment.attrs)
                store_ta_comment_result = re.sub('((.+)\,\"count\"\:\")','',store_ta_comment_result)
                store_ta_comment_result = re.sub('(\"(.+))','',store_ta_comment_result)
                store_ta_comment_result = re.sub('(\{\'class(.+))','None',store_ta_comment_result)
                
                print('Trip Advisor Comments: ',store_ta_comment_result)
            
            
            
            # dolla sign
            store_price = result.find('div',{'class':'price-range'})
            if store_price is not None:
                print('Price Range: ',store_price.text)
                 
            
            
            # pizzeria age
            store_age = result.find('div',{'class':'number'})
            store_age = re.sub('(\<(.+)\"\>)','',str(store_age))
            store_age = re.sub('(\<\/(.+))','',str(store_age))
            print('Years in Business: ',store_age)
            
            
            
            store_review_text = result.find('p',{'class':'body with-avatar'})
            if store_review_text is not None:
                store_review_text = store_review_text.text
                print('Review: ', store_review_text)
            else:
                store_review_text = ''
                print('Review: ', store_review_text)
                
            
            
            # ameneties
            store_ameneties = result.find('div',{'class':'amenities-info'})
            store_ameneties = re.sub('(<div class="amenities-info"><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg">)','',str(store_ameneties))
            store_ameneties = re.sub('<\/svg>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-group"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-outdoor"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<\/span><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg"><use xlink:href="#icon-amenity-alcohol"><\/use>',',',str(store_ameneties))
            store_ameneties = re.sub('<\/span><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg"><use xlink:href="#icon-amenity-family"><\/use>',',',str(store_ameneties))
            store_ameneties = re.sub('<\/span><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg">',',',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-wifi"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-wheelchair"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-reservation"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-alcohol"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-family"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<\/span><\/div>','',str(store_ameneties))
            print('Ameneties: ',store_ameneties)

    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    main2()











    
###########################################################################################
####################  Save the previous infos to MongoDB as sf_pizzerias
###########################################################################################
####################  Loop the links and save pages
###########################################################################################
####################  Save info from pages
###########################################################################################
####################  Include longitude and latitude data from API
###########################################################################################


def main3():
    try:

        # create lists to save info
        rank_1 = []
        name_1 = []
        link_1 = []
        star_1 = []
        num_review_1 = []
        ta_rating_1 = []
        num_ta_review_1 = []
        dolla_sign_1 = []
        yrs_business_1 = []
        revs_1 = []
        ameneties_1 = []


        # repeat the procdure in q5 but saving info to lists

        for i in range(1):
            yp_soup = soup(open(f'./sf_pizzeria_search_page.html','r').read(), 'lxml')
            results = yp_soup.find('div',{'class':'search-results organic'})

            
        for result in results.children:
            
            
            
            ### search rank
            search_rank = result.find('h2',{'class':'n'})
            if search_rank is not None:
                search_rank = result.find('h2',{'class':'n'})
                search_rank = re.findall('\d+',str(search_rank.text))
                rank_1.append(search_rank[0])
                
            
            
            ### name
            search_name = result.find('a',{'class':'business-name'})
            if search_name is not None:
                name_1.append(search_name.text)

                
                
                
            ### store’s YP URL
            store_link_soup = result.find('a',{'class':'business-name'})
            if store_link_soup is not None:
                store_link = store_link_soup.get('href')
                link_1.append('https://www.yellowpages.com'+store_link)
            

            
            
            ### star rating five
            store_rating_5 = result.find('div',{'class':'result-rating five'})
            if store_rating_5 is not None:
                star_1.append('5')
            
            ### star rating four.five
            store_rating_45 = result.find('div',{'class':'result-rating four half'})
            if store_rating_45 is not None:
                star_1.append('4.5')
                
            ### star rating four
            store_rating_4 = result.find('div',{'class':'result-rating four'})
            if store_rating_4 is not None:
                star_1.append('4')
            
            ### star rating three.five
            store_rating_35 = result.find('div',{'class':'result-rating three half'})
            if store_rating_35 is not None:
                star_1.append('3.5')
            
            ### star rating three
            store_rating_3 = result.find('div',{'class':'result-rating three'})
            if store_rating_3 is not None:
                star_1.append('3')
            
            ### star rating two half
            store_rating_25 = result.find('div',{'class':'result-rating two half'})
            if store_rating_25 is not None:
                star_1.append('2.5')
            
            ### star rating two
            store_rating_2 = result.find('div',{'class':'result-rating two'})
            if store_rating_2 is not None:
                star_1.append('2')
            
            ### star rating one half
            store_rating_15 = result.find('div',{'class':'result-rating one half'})
            if store_rating_15 is not None:
                star_1.append('1.5')
                
            ### star rating one
            store_rating_1 = result.find('div',{'class':'result-rating one'})
            if store_rating_1 is not None:
                star_1.append('1')
            
            
            if all(x is None for x in [store_rating_1, store_rating_15, store_rating_2, store_rating_25, store_rating_3, store_rating_35, store_rating_4, store_rating_45, store_rating_5]):
                star_1.append('')
            


            
            # number of reviews(after the star icons)
            star_section = result.find('span',{'class':'count'})
            star_section = re.sub('<span class="count">\(','',str(star_section))
            star_section = re.sub('\)<\/span>','',str(star_section))
            num_review_1.append(star_section)
            
            
            
            
            ### ta rating
            store_ratings = result.find_all('div',{'class':'ratings'})
            for store_rating in store_ratings:
                store_rating_result = str(store_rating.attrs)
                store_rating_result = re.sub('((.+)\{\")','',store_rating_result)
                store_rating_result = re.sub('(\,\"(.+))','',store_rating_result)
                store_rating_result = re.sub('(\{\'class(.+))','None',store_rating_result)
                store_rating_result = re.sub('(rating\"\:\")','',store_rating_result)
                store_rating_result = re.sub('\"','',store_rating_result)
                
                ta_rating_1.append(store_rating_result)
            
            
            

            
            # ta comments
            store_ta_comments = result.find_all('div',{'class':'ratings'})
            for store_ta_comment in store_ta_comments:
                store_ta_comment_result = str(store_ta_comment.attrs)
                store_ta_comment_result = re.sub('((.+)\,\"count\"\:\")','',store_ta_comment_result)
                store_ta_comment_result = re.sub('(\"(.+))','',store_ta_comment_result)
                store_ta_comment_result = re.sub('(\{\'class(.+))','None',store_ta_comment_result)
                
                num_ta_review_1.append(store_ta_comment_result)
            
            
            

            # dolla sign
            store_price = result.find('div',{'class':'price-range'})
            if store_price is not None:
                dolla_sign_1.append(store_price.text)
            else:
                dolla_sign_1.append('')
                 
            

            
            # pizzeria age
            store_age = result.find('div',{'class':'number'})
            store_age = re.sub('(\<(.+)\"\>)','',str(store_age))
            store_age = re.sub('(\<\/(.+))','',str(store_age))
            yrs_business_1.append(store_age)
            
            
            
            

            store_review_text = result.find('p',{'class':'body with-avatar'})
            if store_review_text is not None:
                store_review_text = store_review_text.text
                revs_1.append(store_review_text)
            else:
                store_review_text = ''
                revs_1.append(store_review_text)
                
                
            
            
            # ameneties
            store_ameneties = result.find('div',{'class':'amenities-info'})
            store_ameneties = re.sub('(<div class="amenities-info"><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg">)','',str(store_ameneties))
            store_ameneties = re.sub('<\/svg>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-group"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-outdoor"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<\/span><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg"><use xlink:href="#icon-amenity-alcohol"><\/use>',',',str(store_ameneties))
            store_ameneties = re.sub('<\/span><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg"><use xlink:href="#icon-amenity-family"><\/use>',',',str(store_ameneties))
            store_ameneties = re.sub('<\/span><span><svg class="amenities-icon" height="17" viewbox="0 0 20 17" width="20" xmlns="http:\/\/www\.w3\.org\/2000\/svg">',',',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-wifi"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-wheelchair"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-reservation"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-alcohol"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<use xlink:href="#icon-amenity-family"><\/use>','',str(store_ameneties))
            store_ameneties = re.sub('<\/span><\/div>','',str(store_ameneties))
            ameneties_1.append(store_ameneties)


        # further process the lists


        n=2
        star_11 = star_1[n:]
        num_review_11 = num_review_1[n:]
        dolla_sign_11 = dolla_sign_1[n:]
        yrs_business_11 = yrs_business_1[n:]
        revs_11 = revs_1[n:]
        ameneties_11 = ameneties_1[n:]


        # combine the lists into one df


        df2 = pd.DataFrame(
                    {'rank': rank_1,
                     'name':name_1,
                     'yp_url': link_1,
                     'star_rating': star_11,
                     'num_star_reviews': num_review_11,
                     'ta_rating': ta_rating_1,
                     'num_ta_reviews': num_ta_review_1,
                     'price_range': dolla_sign_11,
                     'years_in_business': yrs_business_11,
                     'reviews_content': revs_11,
                     'ameneties': ameneties_11
                    })


        # insert df to MongoDB


        # create a db
        client = pymongo.MongoClient('localhost:27017')
        db = client["individual_project"]
        yp = db["sf_pizzerias"]
        db.sf_pizzerias.insert_many(df2.to_dict('records'))



        # save 30 pages



        headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

        for i in range(30):
            yp_url = link_1[i]
            response = requests.get(url=yp_url,headers=headers)
            yp_content = response.text
            with open(f'./sf_pizzerias_{i+1}.html','w', encoding='utf8') as fp:
                fp.write(yp_content)
                time.sleep(5)
            
            print('Printed' + str(i+1) + ':' + yp_url)



        # normal scraping of the web pages

        address_1 = []
        phone_1 = []
        website_1 = []

        for i in range(30):
            page = soup(open(f'./sf_pizzerias_{i+1}.html','r').read(), 'lxml')

            
            # get the bape title
            address = page.find('span',{'class':'address'})
            address_1.append(address.text)
            
            
            phone = page.find('strong')
            phone_1.append(phone.text)
            
            website_soup = page.find('a',{'class':'website-link dockable'})
            if website_soup is not None:
                website = website_soup.get('href')
                website_1.append(website)
            else:
                website_1.append('')


        # API


        api_key = 'ec4f7b49e805a87ebe7b9c6ae2cc96e5'
        api_url = 'http://api.positionstack.com/v1/forward'

        lac = []
        long = []

        for i in range(30):
            one_address = str(address_1[i])
            conn = http.client.HTTPConnection('api.positionstack.com')

            params = urllib.parse.urlencode({
                'access_key': api_key,
                'query': one_address,
                'country': 'US',
                'region': 'California',
                'limit': 1,
                })



            res = requests.get(url=api_url,params=params)
            
            doc = soup(res.content, 'html.parser')
            json_dict = json.loads(str(doc))
            json_dict = json_dict['data']
            
            lac_one = re.sub('(,(.+))','',str(json_dict))
            lac_one = re.sub('((.+)\:\s)','',lac_one)
            lac_one = re.sub('(\[\])','',lac_one)
            lac_one = re.sub('(\[\])','',lac_one)
            lac.append(lac_one)
            
            
            long_one = re.sub('(\,\s\'type(.+))','',str(json_dict))
            long_one = re.sub('((.+)\:\s)','',long_one)
            long_one = re.sub('(\[\])','',long_one)
            long_one = re.sub('(\[\])','',long_one)
            long.append(long_one)
            
            
            
        

        for i in range(30):
            db.sf_pizzerias.update_one({'rank': rank_1[i]}, {'$set': {'address': address_1[i], 'phone': phone_1[i], 'website': website_1[i], 'longitude':long[i], 'latitude':lac[i]}}, upsert=True)
        print('All restaurant information updated')

        

    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    main3()



