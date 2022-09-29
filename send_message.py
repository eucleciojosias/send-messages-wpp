#!/usr/bin/env python3

# https://medium.com/@jihargifari/how-to-send-multiple-whatsapp-message-using-python-3f1f19c5976b
# https://stackoverflow.com/questions/8665072/how-to-upload-file-picture-with-selenium-python
# https://stackoverflow.com/questions/51933480/how-to-send-media-files-on-whatsapp-programmatically-using-click-to-chat-feature


import os
from selenium import webdriver
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)

def send_message():
    element_presence(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]', 40)
    msg_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    msg_box.send_keys('\n')
    time.sleep(3)

def send_image():
    driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']").click()
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(os.getcwd()+"/video.mp4")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "span[data-icon='send']").click()
    time.sleep(2)

def prepare_msg(contact_list):
    base_msg = """
Vote 0000
"""
    base_url = 'https://web.whatsapp.com/send?phone={}&text={}'
    for contact in contact_list:
        msg = urllib.parse.quote(base_msg)
        url_msg = base_url.format(contact, msg)
        try:
            driver.get(url_msg)
            time.sleep(2)
            send_message()
            send_image()
            driver.execute_script("window.onbeforeunload = function() {};")
        except:
            continue


chrome_options = Options()
chrome_options.add_argument("--user-data-dir-Session")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)

contact_list = [
    # '+5524999017267',
    # '+5524999639009',
    '+5521972978654',
    # '+5524981368359',
    '+5524999436241',
    # '+5524999036403',
    # '+5521967047697'
]

prepare_msg(contact_list)
driver.quit()
