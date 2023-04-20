#!/usr/bin/env python
# coding: utf-8


# import modules
from bs4 import BeautifulSoup
import requests
import urllib
import re
import pandas as pd
pd.options.mode.chained_assignment = None
import time


# fctables cookie login practice

# before scraping, go to the website, create an account, log in, and bet on a team (bet on Wolfsburg in this case)



def cookieLogin():
    try:
        # Get cookie
        headers = {
                'authority': 'www.fctables.com',
                'method': 'GET',
                'path':'/user/login/',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding':'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control':'no-cache',
                'cookie': '_ga=GA1.2.848635916.1675311424; _gid=GA1.2.2064590529.1675311424; __gads=ID=3ee37ae847cb167b-220e9c30beda000f:T=1675311424:RT=1675311424:S=ALNI_MZ2bMZ-hv6v3O5sRhG7Nv_Y3wTdGQ; _uid=3595988904e468307a0383c21589d939; timezone=America%2FLos_Angeles; PHPSESSID=srte4n4113tcrtd505mbab6pu2; country_code=us; user_login=hahalolsofunny; __gpi=UID=0000093afe9a2f03:T=1675311424:RT=1675384914:S=ALNI_MZ-DfRNuY4wdWKl6JEarHaARmL0bA; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2C%5B%5B1675385074%2C803000000%5D%2C%221YNN%22%5D%2Cnull%2C%5B%5D%5D; FCNEC=%5B%5B%22AKsRol92MT45E-SrtoJj4TTZNkATP7qNPq5KaFt0QxvEk-K0h9zXB_xuAkq2iicp-DIUlFgLWc1mY8keXm03W_MzGkHuKZz_wztaUIBaxFbHGSBIG6UqJOnfmxnY3-DgN7Q9Qxw5bGXrbBmgnYRTAtauj6c-WSBgBw%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
                'pragma': 'no-cache',
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
        URL = "https://www.fctables.com/user/login/"
        page1 = requests.get(URL)
        doc1 = BeautifulSoup(page1.content, 'html.parser')

        session_requests = requests.session()

        res = session_requests.post(URL,
                                    data = {
                                        "login_username" : "ur_user_name",
                                        "login_password" : "ur_passwrd",
                                        "login_action" : "1",
                                        "user_remeber" : "1"
                                    },
                                    headers = headers,
                                    timeout = 15)


        cookies = session_requests.cookies.get_dict()


        page2 = session_requests.get(URL, cookies=cookies)
        doc2 = BeautifulSoup(page2.content, 'html.parser')

        # Try to fake login
        URL='https://www.fctables.com/tipster/my_bets/'
        cookies = cookies
        header_dic = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        info = {':authority': 'www.fctables.com',
        ':method': 'GET',
        ':path': '/tipster/my_bets/',
        'cache-control': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'cookie': cookies}

        res=requests.get(URL, data=info,headers=header_dic, cookies=cookies)
        doc3 = str(BeautifulSoup(res.text,'html.parser'))



        print(doc2)
        print(cookies)


        if 'Wolfsburg' in doc3:
            print('Wolfsburg found.')

    except Exception as ex:
        print('error: ' + str(ex))


if __name__ == '__main__':
    cookieLogin()

