#!usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
import contextlib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui


class TestSeleniumBot(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_post_to_site(self):
        driver = self.driver
        driver.get("http://www.auction-comparer.appspot.com")
        elem = driver.find_element_by_id("keyword")
        elem.send_keys("asus")
        while True:
            elem.send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.close()


def selenium_bot(searched_word):
    with contextlib.closing(webdriver.Firefox()) as driver:
        driver.get("http://www.auction-comparer.appspot.com")
        wait = ui.WebDriverWait(driver, 30)  # timeout after 10 seconds
        inputElement = driver.find_element_by_id('keyword')
        inputElement.send_keys(searched_word)
        inputElement.send_keys(Keys.RETURN)
        results1 = wait.until(
            lambda driver: driver.find_elements_by_class_name('allegro')
        )
        results2 = driver.find_elements_by_class_name('nokaut')
        assert '3.1' in results1[0].text
        print '3.1 founded in  {}'.format(results1[0].text.encode('utf-8'))
        print '------------------'
        assert '43.99' in results2[0].text
        print '43.99 founded in  {}'.format(results2[0].text.encode('utf-8'))

count = 1
while count != 100:
    print '=================='
    print 'Number of action: {}'.format(count)
    print '------------------'
    selenium_bot('asus')
    count += 1
