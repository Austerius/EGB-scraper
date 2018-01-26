from selenium import webdriver
import unittest
import requests
import time
from bs4 import BeautifulSoup

""" Simple tests for EGB_scraper.py script. Run before starting actual script.
    Packets: request, bs4, selenium + firefox browser needed to be installed.
"""


class TestInv(unittest.TestCase):

    def setUp(self):
        self.sleeptime = 2
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_url(self):
        """checking if link exist"""
        try:
            site = requests.get("https://egb.com/play/simple_bets")
        except requests.exceptions.ConnectionError:
            self.fail("Connection Error")
        self.assertEqual(site.status_code, 200)

    def test_outer_html(self):
        """testing if needed css elements exist"""
        self.browser.get("https://egb.com/play/simple_bets")
        time.sleep(self.sleeptime)
        info = self.browser.find_element_by_xpath("//*")
        source_code = info.get_attribute("outerHTML").encode('utf-8')
        # Checking for source code existence
        self.assertNotEqual(source_code, None)

        bs = BeautifulSoup(source_code, 'html.parser')
        # Checking if there are any events/ blocks with used css selector
        events = bs.findAll('div', {"class": "table-bets__main-row js-expand-row has-already-bet"})
        self.assertNotEqual(events, [])

        # Checking if esport selector still exist
        esport = events[0].find('div', {"class": "table-bets__event"})
        self.assertNotEqual(esport, None)

        # Checking if css for first participant exist
        player1 = events[0].find('div', {"class": "table-bets__player1"})
        self.assertNotEqual(player1, None)

        # Checking if bets rate css exist
        bets = events[0].find('div', {'class': "bet-rate"})
        self.assertNotEqual(bets, None)