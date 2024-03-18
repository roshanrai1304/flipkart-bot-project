
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import logging

"""
The following class is used to collect the attributes from the final page. The class is instantiated with 
driver Object.
"""

class CollectData:
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        
    def pull_attributes(self):
        
        """
        The following is used to pull the attributes data from the final page and return the results

        Returns:
            list: the final list of the results
        """
        
        try:
            results = self.driver.find_elements(By.CLASS_NAME, '_2kHMtA')
            attributes = []
            for product in results:
                name = product.find_element(By.CLASS_NAME, "_4rR01T").get_attribute('innerHTML').strip()
                price = product.find_element(By.CLASS_NAME, "_1_WHN1").get_attribute('innerHTML').strip()
                link = product.find_element(By.CSS_SELECTOR, 'a[class="_1fQZEK"]').get_attribute('href')
                attributes.append([name, price, link])
            return attributes
        except Exception as e:
            logging.error(f"Error in collecting data: {e}")
            
            
        
    
        