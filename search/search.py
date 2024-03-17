import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import search.constants as const
from search.search_filters import SearchFilters
from search.collect_data import CollectData

class Search(webdriver.Chrome):
    
    def __init__(self, drvier_path=r"C:\Users\HP\Documents\Selenium\chromedriver.exe", teardown=False):
        
        self.driver_path = drvier_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Search, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
       
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
          self.quit()
          
    def land_first_page(self):
        try:
            self.get(const.BASE_URL)
            WebDriverWait(self, 10).until(EC.title_contains(
                "Online Shopping Site for Mobiles, Electronics, Furniture, Grocery, Lifestyle, Books & More. Best Offers!"
            ))    

        except Exception as e:
            logging.error(f"Error in landing first page: {e}")
            
    def product_search(self, product):
        
        try:
            search_field = self.find_element(By.CLASS_NAME, 'Pke_EE')
            search_field.clear()
            search_field.send_keys(product)
            
            
            WebDriverWait(self, 10).until(
                (EC.visibility_of_element_located((By.CLASS_NAME, '_2iLD__')))
            ).click()
        except Exception as e:
            logging.error(f"Error in Searching for product: {e}")
        
    def apply_filters(self, category=None, brand=None, flipkart_assured=None, price=None):
        try:
            filters = SearchFilters(driver=self)
            filters.apply_category(category)
            filters.apply_brand(brand)
            filters.select_assured(flipkart_assured)
            filters.sort_price(price)
        except Exception as e:
            logging.error(f"Error in applying filters: {e}")
        
    def get_parameters(self):
        
        try:
            collect_data = CollectData(driver=self)
            attributes = collect_data.pull_attributes()
            return attributes
        except Exception as e:
            logging.error(f"Error in getting parameters data: {e}")