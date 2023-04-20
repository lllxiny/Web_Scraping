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


# Dissecting the structure of ebay search result website


# https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_oac=1
# The variable of search item: ‘nkw=amazon+gift+card’

# https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_oac=1&rt=nc&LH_Sold=1
# The variable of ‘sold items’: ‘LH_Sold=1’

# https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&_oac=1&LH_Sold=1&_pgn=2
# The variable that identifies page num: ‘pgn=2’

# Inspect the elements
# 0. Item info:     div.s-item__info
# 1. Item image:     div.s-item__image-section
# 2. Item tag:      div.s-item__title--tag
# 3. Item title:     div.s-item__title
# 4. Item price:     span.s-item__price
# 5. Item bid count:      span.s-item__bids s-item__bidCount
# 6. Item shipping price:     span.s-item__shipping s-item__logisticsCost
# 7. Item return policy:      span.s-item__free-returns s-item__freeReturnsNoFee
# 8. Similar items:     span.s-item__similar-items s-item__similarItemsInfo
# 9. One like this:     span.s-item__sell-one-like-this s-item__sellLikeThisInfo
# 10. Top-rated Plus:     span.s-item__etrs-text



### Start scraping



# Load and save the first page of search result
# Save the first 10 pages of search result


def saveOnePage():
    try:

        # Specify headers
        headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

        #Send request with requests.get

        amz_response = requests.get(url="https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_oac=1&rt=nc&LH_Sold=1", headers=headers)


        # Save the page as a file
        amz_result = amz_response.text
        with open(f'./amazon_gift_card_01.html','w', encoding='utf8') as fullPage:
            fullPage.write(amz_result)
            time.sleep(10)
            print('Search result page 1 printed')

        for i in range(10):
            try:
                amz_url = 'https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&_oac=1&LH_Sold=1&_pgn='+str(i+1)
                amz_responses = requests.get(url=amz_url,headers=headers)
                amz_results = amz_responses.text
                with open(f'./amazon_gift_card_{i+1}.html','w', encoding='utf8') as fullPage:
                    fullPage.write(amz_results)
                    time.sleep(10)
                print('Search result page printed')
            except:
                print('Failed to print')

    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    saveOnePage()



# Loops the 10 pages and save the content
# Get title, price, and shipping price
# Get face value and measure if it is overpriced or not
# Calculate fraction and comment

def getContent():
    try:
        amz_card_title = []
        amz_card_price = []
        amz_card_shipping = []

        # Obtain the info
        for i in range(10):
            content = BeautifulSoup(open(f'./amazon_gift_card_{i+1}.html','r').read(), 'lxml')
            results = content.find_all('div',{"class":"s-item__info"})

            for result in results[1:]:
                title = result.select('div.s-item__title')[0].text
                amz_card_title.append(title)
                price = result.select('span.s-item__price')[0].text
                amz_card_price.append(price)
                ship = result.select('span.s-item__logisticsCost')
                amz_card_shipping.append(ship)
        # Define the format of price
        price_format = re.compile(r'\d+.\d+')

        # Deal with the rows without a shipping info
        for i in range(len(amz_card_shipping)):
            if amz_card_shipping[i] == []:
                amz_card_shipping[i]='0.00'


        # Grab the format
        amz_card_shipping1 = re.sub('Free shipping','0.00', str(amz_card_shipping))
        amz_card_shipping1 = price_format.findall(str(amz_card_shipping1))

        # Process price info
        amz_card_price
        amz_card_price1 = list(map(lambda x: x.replace('$',''), amz_card_price))
        df1 = pd.DataFrame(
            {'Title': amz_card_title,
             'Price': amz_card_price1,
             'Shipping_Price': amz_card_shipping1
            })

        # Grab listed FV; form to numeric
        df1['Face_Value'] = df1['Title'].str.extract(r'(\$\d+)', expand=False)
        df1['Face_Value'] = df1['Face_Value'].str.replace('$', '',regex=True)
        df1['Face_Value'] = pd.to_numeric(df1['Face_Value'])

        # Create a new column replacing price with range; format to numeric
        for i in range(len(df1['Price'])):
            if len(df1['Price'][i])>8:
                df1['Price'][i]=''
        df1['Price'] = pd.to_numeric(df1['Price'])

        # Shipping price column format to numeric
        df1['Shipping_Price'] = pd.to_numeric(df1['Shipping_Price'])

        # Add a cum of ebay price column
        df1['Full_Price']=df1['Price']+df1['Shipping_Price']

        # Add a comparison column; if Full_Price<Face_Value, then TRUE
        df1['Fair_Price'] = df1['Face_Value'] >= df1['Full_Price']
        df2=df1.loc[df1['Fair_Price'] == False]

        # Count and calculate
        count_fair_price=df1['Fair_Price'].values.sum()
        count_fair_price=pd.to_numeric(count_fair_price)
        count_over_price=(~df1['Fair_Price']).values.sum()
        count_over_price=pd.to_numeric(count_over_price)
        over_price_percentage='{:.1%}'.format(count_over_price/(count_fair_price+count_over_price))



        print(amz_card_title)
        print(amz_card_price)
        print(amz_card_shipping1)
        print(df1)
        print(df2)
        print('Number of full price lower than face value: '+str(count_fair_price))
        print('Number of full price higher than face value: '+str(count_over_price))
        print('Fraction of overprice sellings: '+over_price_percentage)
        print('Reasons for the situation: some of the buy-and-sell transactions are fake transactions for some other purposes, such as money laundrying. And thus they are actually supposed to be overpriced.')


    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    getContent()