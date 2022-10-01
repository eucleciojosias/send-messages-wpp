#!/usr/bin/env python3

# https://medium.com/@jihargifari/how-to-send-multiple-whatsapp-message-using-python-3f1f19c5976b
# https://stackoverflow.com/questions/8665072/how-to-upload-file-picture-with-selenium-python
# https://stackoverflow.com/questions/51933480/how-to-send-media-files-on-whatsapp-programmatically-using-click-to-chat-feature


import os
import csv
import sys
from selenium import webdriver
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager


def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)


def send_message():
    element_presence(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]', 40)
    msg_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    msg_box.send_keys('\n')
    time.sleep(3)


def send_media(media_filename):
    driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']").click()
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys("{}/{}".format(os.getcwd(), media_filename))
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "span[data-icon='send']").click()
    time.sleep(2)


def load_number_with_message(phone_number, base_msg):
    base_url = 'https://web.whatsapp.com/send?phone={}&text={}'
    msg = urllib.parse.quote(base_msg)
    wpp_web_url = base_url.format(phone_number, msg)

    driver.execute_script("window.onbeforeunload = function() {};")
    driver.get(wpp_web_url)
    time.sleep(5)


## INPUTS
phone_numbers_file = sys.argv[1]

text_msg_file = open(sys.argv[2], 'r')
text_msg = text_msg_file.read()
text_msg_file.close()

attachments_dir = sys.argv[3]
attachments_files = [f for f in os.listdir(attachments_dir) if os.path.isfile(os.path.join(attachments_dir, f))]


##### LOG
log_prefix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
log_file = open('logs/{}.log'.format(log_prefix), 'w')


##### INIT BROWSER
chrome_options = Options()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_options.add_argument("--user-data-dir-Session")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

##### SEND
with open(phone_numbers_file, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        log_file.write('\n------------------------------')
        log_file.write('\n{} - sending'.format(row['number']))

        try:
            load_number_with_message(row['number'], text_msg)
            log_file.write('\n{} - loaded'.format(row['number']))

            send_message()
            log_file.write('\n{} - message sent'.format(row['number']))

            for filename in attachments_files:
                media_path = '{}/{}'.format(attachments_dir, filename)
                send_media(media_path)
                log_file.write('\n{} - {} - attachment sent'.format(row['number'], media_path))

        except Exception as e:
            print(e)
            log_file.write('\n{} - failed'.format(row['number']))

            continue

        log_file.write('\n{} - succeeded'.format(row['number']))


log_file.close()
driver.quit()
