import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random

mp_url = 'https://www.marktplaats.nl/'
#login_url = 'https://www.marktplaats.nl/account/login.html?target=https%3A%2F%2Fwww.marktplaats.nl%2F'
item_url = 'https://www.marktplaats.nl/a/sport-en-fitness/roeien/m1594115209-concept-2-model-d-roeitrainer.html'
un = 'info@lorenzkort.nl'
pw = 'M8g6enc6'

# navigate to item
driver = webdriver.Firefox()
driver.get(item_url)
driver.find_element_by_link_text('Bericht').click()

# login
username = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
for i in un:
    username.send_keys(i)
password = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
for i in pw:
    password.send_keys(i)
cookie_accept = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-consent-banner-accept-button"]'))).click()
login_bt = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-form-login"]/form/button'))).click()


#username = driver.find_element_by_class_name('mp-Form-controlGroup')

time.sleep(30)
driver.quit()