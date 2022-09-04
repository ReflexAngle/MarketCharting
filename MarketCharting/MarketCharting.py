from tkinter import *
from bs4 import BeautifulSoup
from pip._vendor import requests
import time
import sys


Window = Tk(className='Market Charting')
Window.geometry("500x400")

# scrapes the prices for each oif the markets.
# uses a loop to continuously scrape every 15 seconds.
# all three sources will be averaged out to try and get a
# more accurate number this is different sources give different numbers.
DOW = 'https://www.google.com/finance/quote/.DJI:INDEXDJX'
SP = 'https://www.google.com/finance/quote/.INX:INDEXSP'
NAS = 'https://www.google.com/finance/quote/.IXIC:INDEXNASDAQ'

DOW2 = 'https://www.marketwatch.com/investing/index/djia'
SP2 = 'https://www.marketwatch.com/investing/index/spx'
NAS2 = 'https://www.marketwatch.com/investing/index/comp'

DOW3 = ''
SP3 = ''
NAS3 = ''

# each variable above is place in the array.
Markets = [DOW, SP, NAS]
Markets2 = [DOW2, SP2, NAS2]

Market_results = []

# runs each link through a loop to scrape the information.
# scrapes from business insider.
for i in Markets:
    page = i
    page = requests.get(page)
    soup = BeautifulSoup(page.text, "html.parser")

    result = soup.find('div', class_='fxKbKc')
    result = result.string
    result = result.replace(',', '')
    # converts string to float to average out values.
    result = float(result)
    Market_results.append(result)

# scrapes fom market watch.
for i in Markets2:
    page2 = i
    page2 = requests.get(page2)
    soup = BeautifulSoup(page2.text, "html.parser")

    # had to use find twice to get result I was looking for on market watch.
    # tried this with other markets didn't have to do this twice.
    # well this is annoying the website switches HTML tags throughout the day.
    # use a try to try both bg-quote and span tags.
    try:
        result = soup.find('h2', class_='intraday__price')
        result = result.find('bg-quote', class_='value')
        result = result.string
        result = result.replace(',', '')
        result = float(result)
        Market_results.append(result)
    except:
        result = soup.find('h2', class_='intraday__price')
        result = result.find('span', class_='value')
        result = result.string
        result = result.replace(',', '')
        result = float(result)
        Market_results.append(result)
    # use else for safe measure
    else:
        result = 'invalid'
        Market_results.append(result)

# stores the variables from the array in individual variables.
# Average the results from the sources.
# 0 - 2 BI 3 - 5 MW.
# use a check to see if any equal invalid.
if Market_results[3] or Market_results[4] or Market_results[5] == 'invalid':
    Dow_A = Market_results[0]
    SP_A = Market_results[1]
    NAS_A = Market_results[2]
else:
    Dow_A = Market_results[0] + Market_results[3]
    SP_A = Market_results[1] + Market_results[4]
    NAS_A = Market_results[2] + Market_results[5]
    # rounds the number to the nearest a hundred place so there isn't long decimal places for a price.
    Dow_A = round((Dow_A / 2), 2)
    SP_A = round((SP_A / 2), 2)
    NAS_A = round((NAS_A / 2), 2)

revert = [Dow_A, SP_A, NAS_A]
Revert_str = []

# this is to implement a comma back in to make it easier to read.
# to check get the comma in the right area it checks the size of the number
for i in revert:
    revert = i
    if i >= 100000:
        revert = str(revert)
        revert = revert[:3] + ',' + revert[3:]
    elif i >= 10000:
        revert = str(revert)
        revert = revert[:2] + ',' + revert[2:]
    elif i >= 1000:
        revert = str(revert)
        revert = revert[:1] + ',' + revert[1:]
    else:
        revert = str(revert)
    Revert_str.append(revert)

print(Revert_str)
Dow_B = Revert_str[0]
SP_B = Revert_str[1]
NAS_B = Revert_str[2]

# print the prices from each market on the screen.
DLabel = Label(Window, text=Dow_B, font="ubuntu")
SLabel = Label(Window, text=SP_B, font="ubuntu")
NLabel = Label(Window, text=NAS_B, font="ubuntu")

# place labels on the screen
DLabel.grid(row=0, column=0)
SLabel.grid(row=0, column=1)
NLabel.grid(row=0, column=2)


# ____________________________________________________________________________________________________________________ #
# The part of the application that does stuff.

# function for the stock button.
def sto_click():

    # searches for the stock that the user has inputted
    def search():

        user_entry = enter.get()

        # search based on the name of the company the stock is based on
        # A little finicky some stocks companies like ford may be a company but is the symbol for a stock too
        # It's better for now to stay with the name of the stocks symbol
        # for instance if you type ford instead of getting Ford Motor you get Forward Industries
        url = 'https://markets.businessinsider.com/searchresults?_search=' + user_entry
        try:
            sto_req = requests.get(url)
            sto_soup = BeautifulSoup(sto_req.text, "html.parser")
            sto_result = sto_soup.find('table', class_='table')
            sto_result = sto_result.find('td', class_='table__td')

            for a in sto_result.find_all('a'):
                sto_result = (a.get('href'))
                sto_result = sto_result.strip()
                sto_result = sto_result
        except:
            sto_result = 'invalid entry'

        # try both the name and the symbol
        if sto_result != 'invalid entry':
            try:
                sto_URL = 'https://markets.businessinsider.com' + sto_result
                sto_URL = requests.get(sto_URL)
                soup = BeautifulSoup(sto_URL.text, "html.parser")

                sto_result = soup.find('span', class_='price-section__current-value')
                sto_result = sto_result.string

                sto_result1 = soup.find('h1', class_='price-section__identifiers')
                '''sto_result1 = sto_result1.string
                sto_result1 = sto_result1.find("Stock")'''


                print(sto_result)
                print(sto_result1)
            except:
                sto_URL = 'https://markets.businessinsider.com/stocks/' + user_entry + '-stock'
                sto_URL = requests.get(sto_URL)
                soup = BeautifulSoup(sto_URL.text, "html.parser")
                sto_result = soup.find('span', class_='price-section__current-value')
                sto_result = sto_result.string

                print(sto_result)
        else:
            sto_result = 'invalid entry'

        # displays the price of the stock
        get_price = Label(Window, text=sto_result)
        get_price.grid(row=8, column=0)

    new_label = Label(Window, text="type a Stock", font='ubuntu')
    new_label.grid(row=5, column=0)

    enter = Entry(Window)
    enter.grid(row=7, column=0)

    search = Button(Window, text='search', font='ubuntu', command=search)
    search.grid(row=9, column=0)


# function for the commodity button.
def com_click():

    # searches for the inputted commodity
    # and out put the price
    def search():

        user_entry = enter.get()

        user_entry = user_entry.replace(" ", "-")

        print(user_entry)

        try:
            html = 'https://markets.businessinsider.com/commodities/' + user_entry + '-price'
            com_page = requests.get(html)
            com_soup = BeautifulSoup(com_page.text, "html.parser")

            com_result = com_soup.find('span', class_='price-section__current-value')
            com_result = com_result.string
        except:
            com_result = 'please select a commodity'

        print(com_result)

        # displays the price of the commodity
        get_price = Label(Window, text=com_result)
        get_price.grid(row=8, column=0)

    second_label = Label(Window, text="type a commodity", font="ubuntu")
    second_label.grid(row=5, column=0)

    enter = Entry(Window)
    enter.grid(row=7, column=0)

    search = Button(Window, text='search', font='ubuntu', command=search)
    search.grid(row=9, column=0)


# searches through cryptocurrencies
def cry_click():

    def search():

        user_entry = enter.get()
        html = 'https://markets.businessinsider.com/currencies/' + user_entry + '-usd'

        cry_page = requests.get(html)
        cry_soup = BeautifulSoup(cry_page.text, "html.parser")

        cry_result = cry_soup.find('span', class_='price-section__current-value')
        cry_result = cry_result.string

        get_price = Label(Window, text=cry_result)
        get_price.grid(row=8, column=0)

    enter = Entry(Window)
    enter.grid(row=7, column=0)

    search = Button(Window, text='search', font='ubuntu', command=search)
    search.grid(row=9, column=0)


'''def etf_click():

    def search():
        user_entry = user_entry.get()'''


'''    enter = Entry(Window)
    enter.grid(row=7, column=0)

    search = Button(Window, text='search', font='ubuntu', command=search)
    search.grid(row=9, column=0)'''


# just some UI stuff
# buttons that let you select different markets that you might want to see
# such as stocks commodities crypto and ETFs
Commodity_Button = Button(Window, text="Commodity", width=17, command=com_click, font="ubuntu")
Stock_Button = Button(Window, text="Stock", width=17, command=sto_click, font="ubuntu")
Crypto_Button = Button(Window, text="Crypto", width=17, command=cry_click, font="ubuntu")
'''ETF_Button = Button(Window, text="ETF", width=17, command=etf_click, font="ubuntu")'''


Commodity_Button.grid(row=3, column=0)
Stock_Button.grid(row=3, column=1)
Crypto_Button.grid(row=3, column=2)
'''ETF_Button.grid(row=3, column=3)'''

Window.mainloop()

