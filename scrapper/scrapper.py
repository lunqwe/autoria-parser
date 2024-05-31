import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from database.models import Card
from run import setup_logger

class Scrapper:
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    website_url = 'https://auto.ria.com/uk/car/used/'
    page_amount = 0
    logger = setup_logger()
    
    def get_page_amount(self):
        response = requests.get(self.website_url)

        if response.status_code == 200:
             html_content = response.text

             soup = BeautifulSoup(html_content, 'lxml')

             element = soup.select_one('#pagination > nav > span:nth-child(8) > a') 
             page_amount = element.text
             # log: found {page_amount} pages
             self.page_amount = int(page_amount.replace(' ', ''))
        else:
            self.logger.error(f"Failed to retrieve page, status code: {response.status_code}")
    
    def get_cards_links(self, link):
        response = requests.get(link)

        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, 'lxml')

            content_elements = soup.find_all(class_='address')

            links = [element['href'] for element in content_elements]
            
            return links
        
    def get_card_data(self, link):
        self.driver.get(link)
        
        data = {
            'url': link,
            'title': DetailsScrapper.get_title(driver=self.driver),
            'price_usd': DetailsScrapper.get_price(driver=self.driver),
            'odometer': DetailsScrapper.get_odometer(driver=self.driver),
            'username': DetailsScrapper.get_username(driver=self.driver),
            'phone_number': DetailsScrapper.get_phone_number(driver=self.driver),
            'image_url': DetailsScrapper.get_image_url(driver=self.driver),
            'images_count': DetailsScrapper.get_images_amount(driver=self.driver),
            'car_number': DetailsScrapper.get_car_number(driver=self.driver),
            'car_vin': DetailsScrapper.get_car_vin(driver=self.driver),
        }
        return data
    


class DetailsScrapper:
    
    def get_title(driver):
        try:
            title = driver.find_elements(by=By.CLASS_NAME, value='auto-content_title')[0].text
            return title
        except:
            return None
        
    def get_price(driver):
        try:
            price_usd = driver.find_element(by=By.XPATH, value="//*[@id='showLeftBarView']/section[1]/div[1]/strong").text
            return int(price_usd.replace(' ', '')[:-1])
        except:
            return None
        
    def get_odometer(driver):
        try:
            odometer = driver.find_element(by=By.XPATH, value='//*[@id="details"]/dl/dd[2]/span[2]').text
            return odometer.replace('тис.', '000').replace(' ', '')[:-2]
        except:
            return None

    def get_username(driver):
        try:
            username = driver.find_element(by=By.XPATH, value='/html/body/div[7]/div[10]/div[4]/aside/section[2]/div[1]/div/div[2]').text
            if 'На сайті був' or "Зараз на сайті" in username:
                return "undefined"
            return username
        except:
            return None
        
    def get_phone_number(driver):
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="phonesBlock"]/div/span/a').click()
            phone_number_obj = driver.find_element(by=By.XPATH, value='//*[@id="openCallMeBack"]/div[2]/div[2]').text
            driver.find_element(by=By.XPATH, value='//*[@id="show-phone"]/div[1]/a').click()
            phone_number = 1212
            return phone_number
        except:
            return None
    
    def get_image_url(driver):
        try:
            image_url = driver.find_element(by=By.XPATH, value='//*[@id="photosBlock"]/div[1]/div[1]/div[1]/picture/img')
            return image_url.get_attribute('src')
        except:
            return None
        
    def get_images_amount(driver):
        try:
            images_amount_obj = driver.find_element(by=By.XPATH, value='//*[@id="photosBlock"]/div[2]/div[2]/a').text
            images_count = re.search(r'\d+', images_amount_obj).group()
            return images_count
        except:
            return None
        
    def get_car_number(driver):
        try:
            car_number = driver.find_element(by=By.XPATH, value='/html/body/div[7]/div[10]/div[4]/main/div[2]/div[2]/div[1]/dl/dd[1]/div[2]/span[1]').text
            if "Перевірений" in car_number:
                return None
            return car_number
        except:
            return None
        
    def get_car_vin(driver):
        try:
            car_vin = driver.find_elements(by=By.CLASS_NAME, value='label-vin')
                
            if len(car_vin) > 1:
                car_vin = car_vin[1].text
            else:
                car_vin = car_vin[0].text
                
            return car_vin

        except:
            try:
                car_vin = driver.find_elements(by=By.CLASS_NAME, value='vin-code').text
                return car_vin
            except:
                return None
    

