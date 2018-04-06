#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
import os
import urllib
import codecs

class PriceParser():

    def __init__(self, link = None, page_range = None):
        
        __slots__ = ['run', 'GoToURL', 'pricesAndTitles']

        if link == None:
            self.link = 'blablabla'
        else:
            self.link = link
        if page_range == None:
            self.page_range = 100
        else:
            self.page_range = page_range

        self.PRODUCTS = {}
        
        self.driver = webdriver.Firefox()

    def run(self):
        # Execute method for parsing out of pages
        self.GoToURL()
        # Save data to txt file
        with codecs.open('./parsed.txt', 'w', 'utf-16') as file:
        	for element in self.PRODUCTS:
		        file.write(str(self.PRODUCTS[element]) + u"\n")

        return self.PRODUCTS
    
    def GoToURL(self):
        for number in range(self.page_range):
            try:
                sleep(3)
                self.driver.get(self.link + str(number))
                self.pricesAndTitles(number)
            except Exception as e:
                print(e)
                print('[info] Stop.')
                return 0
            
    def pricesAndTitles(self, page):
        pricePlusTitle = []
        product_range = 72
        
        # Get elements by class names
        price = self.driver.find_elements_by_class_name("val")
        title = self.driver.find_elements_by_class_name("title")

        prices_list = [price[num].text for num, i in enumerate(price)]
        # Cut all the '' from list
        # To do it we use magic method __ne__ that checks if statement is not equal (!=) to something or not
        # Function filter returns only those values for whom check method returns True
        # At last, we packing it to list
        price = list(filter(('').__ne__, prices_list))

        for element_number in range(product_range):
            product = price[element_number] + ' : ' + str(title[element_number+1].text)
            pricePlusTitle.append(product)

        del price, title

        self.PRODUCTS[page] = pricePlusTitle
        print('[info] PRODUCTS: ', self.PRODUCTS)

if __name__ == "__main__":
  pp = PriceParser()
  parsing_results = pp.run()
