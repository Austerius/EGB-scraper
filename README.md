# EGB-scraper
<p>Script for scraping bets information(odds, date, event, players) from website EGB.com (only about events, 
    you can still bet on, but this can be modified inside a 'egb_spider()' function).</p>
    Scraped information returns as a dictionary of lists of dictionaries and have a following <b>format</b>:</br>
    {</br>
    '<i>name of the 1st esport</i>': [{'<i>time</i>': event time, '<i>player1</i>': name of the first player,</br> 
                                '<i>player2</i>': name of the second player, '<i>odds1</i>': bet odds on the first player,</br>
                                '<i>odds2</i>': bet odds on the second player},</br>
                                {another game information},], </br>
     '<i>name of the 2nd esport</i>': [{}, {}, ],</br> 
     ..............................................</br>
    }</br>
    <p>The names of the esport obtained from the site(LoL, Overwatch etc - print results of scraping 
    to check all names)</p>  
    <p>This script using Selenium and Firefox driver, so, before running it - make sure you have all 
    <b>packets installed</b>: Selenium, BeautifulSoup, GeckoDriver(for Windows), Firefox browser. 
    On a server you'll need a some sort of virtual monitor to ran a browser, but again - running 
    selenium+firefox on server machine can cause a performance problems, - better to use other solution(maybe 
    scrapy + Splash?).</p>
    <p><i>Take note</i>: script was written for and tested on Windows machines.</p>
    <p>You can ran this script from the <b>command line</b> using parameter <i>'show'</i> to scrape and to list information 
    directly into the terminal('help' will list available options).</p>
    <p>Before runing actual script - run <i>test_egb_scraper.py</i></p>
    <p>After importing this script into your own - use 'egb_spider()' function to run a scraper.</p> 
