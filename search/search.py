import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import search.constants as const
from search.search_filters import SearchFilters
from search.collect_data import CollectData
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from prettytable import PrettyTable



"""
     The following Search class inhert's webdrive.Chrome class and inititalized with it that 
     do the process of searching products, applying filter and storing the attributes after applying the filters
     The process of Applying filters is done with help of other two class that are define
     SearFilters and CollectData
"""

class Search(webdriver.Chrome):
    
    def __init__(self, teardown=False):
        
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.set_capability('sessionName', 'flipkart Bot PC')
        super(Search, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
       
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
          self.quit()
          
    def land_first_page(self):
        
        """
        The following method is used to handle the operation of searching for the flipkart website and
        it does that after it locates the title of the HTML page. After the page is loaded it executes
        script to set the status in the BrowserStack Automate Infrastructure else it executes the script for error 
        """
        
        try:
            self.get(const.BASE_URL)  
            WebDriverWait(self, 10).until(EC.title_contains(
                "Online Shopping Site for Mobiles, Electronics, Furniture, Grocery, Lifestyle, Books & More. Best Offers!"
            ))
            self.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Landed on first page!"}}') 

        except NoSuchElementException as err:
            logging.error(f"Error in landing first page: {err}")
            message = 'Exception: ' + str(err.__class__) + str(err.msg)
            self.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
            
    def product_search(self, product):
        
        """
        The following methof is used to search for the particular product and executes the script
        accordingly to update the status.
        
        Args:
          product: Name of the product
          
        
        """
        
        try:
            search_field = WebDriverWait(self, 10).until(
                (EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[class="Pke_EE"]')))
            )
            search_field.clear()
            search_field.send_keys(product)
            
            WebDriverWait(self, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="_2iLD__"]'))
            ).click()
            self.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Product Search completed!"}}') 
            
        except NoSuchElementException as err:
            logging.error(f"Error in Searching for product: {err}")
            message = 'Exception: ' + str(err.__class__) + str(err.msg)
            self.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
        
    def apply_filters(self, category=None, brand=None, flipkart_assured=None, price=None):
        
        """
        The following method is used to apply the filters to the page where the product is searched
        and the executes the script accordinly to update the status
        
        Args:
          category: Category of the product
          brand: Name of the brand
          flipkart_assured:  flipkart_assured or not
          price: Sort the price
        """
        
        try:
            filters = SearchFilters(driver=self)
            filters.apply_category(category)
            filters.apply_brand(brand)
            filters.select_assured(flipkart_assured)
            filters.sort_price(price)
            self.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Filters applied to search!"}}') 
        except NoSuchElementException as err:
            logging.error(f"Error in applying filters: {err}")
            message = 'Exception: ' + str(err.__class__) + str(err.msg)
            self.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
        
    def get_parameters(self):
        
        
        """
        The following method is used to get the parametes from the final page and store it in a list
        and then print results. For bettter I have used python library "prettytable".
        """
        
        try:
            collect_data = CollectData(driver=self)
            attributes = collect_data.pull_attributes()
            table = PrettyTable(
            field_names=["Name", "Price", "Link"]
            )
            table.add_rows(attributes)
            print(table)
            
            self.execute_script(
               'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "All attributes are stored!"}}') 
            return attributes
        except NoSuchElementException as err:
            logging.error(f"Error in getting parameters data: {err}")
            message = 'Exception: ' + str(err.__class__) + str(err.msg)
            self.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')