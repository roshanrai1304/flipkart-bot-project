from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class SearchFilters:
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        
    def check_filter(self, filter):
        filter_element = WebDriverWait(self.driver, 10).until(
            (EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="_3sckoD"]')))
        ).get_attribute('innerHTML').strip()
        
        if filter_element == filter:
            return
        
    def wait_for_class_change(self, element, class_name):
        """
        Wait for the class of an element to change.
        
        Args:
        element: WebElement to wait for the class change.
        class_name: The new class name to wait for.
        """
        def class_changed(driver):
            return class_name in element.get_attribute("class")
        WebDriverWait(self.driver, 10).until(class_changed)
        
        
    def apply_category(self, category):
        
        try:
            category_element = WebDriverWait(self.driver, 10).until(
                (EC.visibility_of_element_located((By.CLASS_NAME, '_2q_g77')))
            ).find_element(By.CLASS_NAME, "_1jJQdf")
            
            text = category_element.get_attribute('innerHTML').strip()
            if text == category:
                category_element.click()
        except Exception as e:
            logging.error(f"Error in applying category: {e}")
            
    def apply_brand(self, brand):
        try:
            WebDriverWait(self.driver, 10).until(
                (EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[title={brand}]")))
            ).click()
            self.check_filter(brand)
        except Exception as e:
            logging.error("Error in applying brand filter: {e}")
        
        
    def select_assured(self, value):
        try:
            if value:
                WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="_24_Dny _3tCU7L"]'))
                ).click()
                self.check_filter(value)
        except Exception as e:
            logging.error("Error in applying assured filter: {e}")
            
    def sort_price(self, price_high_to_low=None):
        
        try:
            if price_high_to_low:
                sort_element = self.driver.find_elements(By.CLASS_NAME, '_10UF8M')
                for element in sort_element:
                    text = element.get_attribute('innerHTML').strip()
                    if text == price_high_to_low:
                        element.click()
                        
                        self.wait_for_class_change(element, "_10UF8M _3LsR0e")
        except Exception as e:
            logging.error("Error in sorting price: {e}")
                    
        
                    
            
        
        
        