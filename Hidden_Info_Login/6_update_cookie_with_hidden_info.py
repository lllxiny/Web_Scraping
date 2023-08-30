#!/usr/bin/env python
# coding: utf-8



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





# # Planespotters: obtain cookie --> use cookie to obtain hidden info --> update cookie --> use cookie to login




# ## 1 Access website; save cookies and hidden contents


# Specify headers
headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

#Send request with requests.get
session_requests = requests.session()
page_new1 = session_requests.get(url="https://www.planespotters.net/user/login", headers=headers)

# Get cookies
cookies = page_new1.cookies.get_dict()

# Parse the html text and obtain csrf and. rid
doc1 = soup(page_new1.content, 'html')
input1 = doc1.select("div.planespotters-form table.photoUpload tr td input[name=csrf]")[0]
csrf = input1.get("value")
input2 = doc1.select("div.planespotters-form table.photoUpload tr td input[name=rid]")[0]
rid = input2.get("value")




# ## 2 Log in and update cookies


# Log in and get cookies

headers = {
                'authority': 'www.planespotters.net',
                'method': 'POST',
                'path':'/user/login/',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding':'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control':'no-cache',
                'content-length': '78',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.planespotters.net',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            }

session_requests = requests.session()

url ="https://www.planespotters.net/user/login"

res = session_requests.post(url, 
                            data = {
                                "action":"/user/login",
                                "method":"post",
                                "referer" : "https://www.planespotters.net/",
                                "username" : "ur_username",
                                "password" : "ur_pswrd",
                                "rid":rid,
                                "csrf":csrf,
                                "remember" : "yes"
                            },
                            headers = headers,
                            cookies = cookies,
                            timeout = 15)


cookies1 = session_requests.cookies.get_dict()

# check if the procedure succeeded

print(res)


  

# ## 3 Get and add cookies



# combine all cookies
all_cookies = {
                "1": cookies,
                "2": cookies1,
                }






# ## 4 Verify log in on profile page



# Try to fake login

URL1='https://www.planespotters.net/member/profile'
session_requests = requests.session()
header_dic = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


profile = session_requests.get(URL1, headers = header_dic, cookies = cookies1)
profile_soup1 = soup(profile.content, 'html')






# ## 5 Print results

# ### 5.1 Print beautifulsoup document

print(profile_soup1)


# ### 5.2 Print cookies

print(all_cookies)


# ### 5.3 Print logged in or not

checking = bool(re.findall(r'ur_username',str(profile_soup1)))
print('username user logged in?: ', checking)

