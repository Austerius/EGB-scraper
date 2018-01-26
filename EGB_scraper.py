from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import sys
import shlex
""" Script for scraping bets information(odds, date, event, players) from website EGB.com (only about events, 
    you can still bet on, but this can be modified inside a 'egb_spider()' function)
    Scraped information returns as a dictionary of lists of dictionaries and have a following format:
    {'name of the 1st esport': [{'time': event time, 'player1': name of the first player, 
                                'player2': name of the second player, 'odds1': bet odds on the first player,
                                'odds2': bet odds on the second player},
                                {another game information},],
     'name of the 2nd esport': [{}, {}, ], 
     ..............................................
    }
    The names of the esport obtained from the site(LoL, Overwatch etc - print results of scraping 
    to check all names)  
    This script using Selenium and Firefox driver, so, before running it - make sure you have all 
    packets installed: Selenium, BeautifulSoup, GeckoDriver(for Windows), Firefox browser. 
    On a server you'll need a some sort of virtual monitor to ran a browser, but again - running 
    selenium+firefox on server machine can cause a performance problems, - better to use other solution(maybe 
    scrapy + Splash?).
    Take note: script was tested on Windows machines
    You can ran this script from the command line using a parameter 'show' to scrape and to list information 
    directly into terminal('help' will list available options).
    After importing this script into your own - use 'egb_spider()' function to run a scraper.         
    """


# script author - Alexander Shums'kii
# https://github.com/Austerius
def egb_spider(show=False):

    sleeptime = 2  # edit sleeptime, when you need to change delay(time) to load webpage
    info_dict = {}  # we will save obtained information into this dictionary
    browser = webdriver.Firefox()
    try:
        browser.get("https://egb.com/play/simple_bets")
        time.sleep(sleeptime)  # give some time to load
        info = browser.find_element_by_xpath("//*")
        # getting outerHTML code for parsing with BeautifulSoup
        source_code = info.get_attribute("outerHTML").encode('utf-8')
        time.sleep(sleeptime)
    finally:
        browser.quit()  # shutting browser window

    bs = BeautifulSoup(source_code, 'html.parser')
    # information about single event contained in this 'div' block:
    event = bs.findAll('div', {"class": "table-bets__main-row js-expand-row has-already-bet"})
    # print(event[0])
    for item in event:
        date_block = item.find('div', {"class": "table-bets__date"})
        if date_block is not None:
            event_date = date_block.find('span', {'data': "date"}).get_text()
        else:
            continue  # don't scrape event with no date(live event etc)
            # date = None
        event_time = date_block.find('span', {'data': "time"}).get_text()
        # It seems, site shows dates in UTC format, but I'm not sure(
        current_time = datetime.datetime.utcnow()
        day, month = event_date.split('.')
        hour, minute = event_time.split(':')
        # Trying to resolve year here:
        if current_time.month == 12 and (month == 1):
            year = int(current_time.year) + 1
        else:
            year = current_time.year
        # print(year)
        # UTC date for event
        global_event_time = datetime.datetime(year=int(year), month=int(month), day=int(day),
                                              hour=int(hour), minute=int(minute))
        # print(global_event_time)
        # ok, we will not scrape events from the past(only events, we can still bid on):
        # comment 'if' statement, if you need all events to be scrapped
        if global_event_time <= current_time:
            continue

        esport_block = item.find('div', {"class": "table-bets__event"})
        esport = esport_block.find('img')['alt']  # name of the e-sport

        player1_block = item.find('div', {"class": "table-bets__player1"})
        player1_name = player1_block.find('span').get_text()  # name of the 1st participant
        player1_bet_block = item.find('div', {'class': "bet-rate"})  # first value of bet rates
        # print(player1_bet_block)
        if player1_bet_block is None:
            continue
        else:
            player1_bet = player1_bet_block.get_text()

        player2_block = item.find('div', {'class': "table-bets__player2"})
        player2_name = player2_block.find("span").get_text()  # name of the 2nd participant
        player2_bet = item.findAll('div', {'class': "bet-rate"})[-1].get_text()  # last value of bet rates

        # adding scraped info to the dictionaries
        temp_dict = {'time': global_event_time, 'player1': player1_name, 'player2': player2_name,
                     'odds1': player1_bet, 'odds2': player2_bet}
        try:
            info_dict[esport].append(temp_dict)
        except KeyError:
            info_dict[esport] = [temp_dict]
        if show:
            print(esport)
            print(global_event_time)
            # print(event_date)
            # print(event_time)
            print("{0}  {1}:{2}  {3}".format(player1_name, player1_bet, player2_bet, player2_name))
            print("-"*40)

    # for key in info_dict:
    #     print("{}: {}".format(key, info_dict[key]))
    # print(source_code)
    return info_dict


if __name__ == "__main__":
    show = False
    try:
        command = shlex.quote(sys.argv[1])
        if command.lower() == "show":
            show = True
        if command.lower() == "help":
            print("Keywords:")
            print("show - print scrapped data")
            print("help - print info about available commands")
            sys.exit(0)
    except IndexError:
        pass
    egb_spider(show=show)