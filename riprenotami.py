#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

import sys
import time
import logging

def PCheck(driver, url, type):
  driver.get(url)
  size = len(driver.find_elements(By.XPATH, '//div[@id="typeofbooking"]'))
  if size > 0:
    return 0
  size = len(driver.find_elements(By.XPATH, "//div[text()='Al momento non ci sono date disponibili per il servizio richiesto']"))
  if size > 0:
    return 1
  return -1

def PLogin(driver, url, email, password):
  driver.get(url)
  elems = driver.find_elements(By.ID, "login-email")
  if len(elems) == 0:
    return False
  elem = elems[0]
  elem.clear()
  elem.send_keys(email)
  elems = driver.find_elements(By.ID, "login-password")
  if len(elems) == 0:
    return False
  elem = elems[0]
  elem.clear()
  elem.send_keys(password)
  elem.send_keys(Keys.RETURN)
  size = len(driver.find_elements(By.XPATH, '//table[@id="dataTableServices"]'))
  #WebDriverWait(driver, 120).until(
  #  EC.presence_of_element_located((By.XPATH, '//table[@id="dataTableServices"')))
  return size > 0

def login(driver, login_url, email, password):
  driver.delete_all_cookies()
  logging.warning(f'Logging in as {email}...')
  while not PLogin(driver, login_url, email, password):
    driver.delete_all_cookies()
  logging.warning(f'Logged in as {email}')

def main():
  try:
    import params
  except ImportError:
    print("Please create params.py based on params_default.py first.")
    sys.exit(1)

  logging.basicConfig(level=params.log_level, format=params.log_format, datefmt=params.log_datefmt)

  check_urls = {}
  if params.id_check:
    check_urls["id"] = params.id_url
  if params.passport_check:
    check_urls["passport"] = params.passport_url

  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  driver = webdriver.Chrome(options=options, service_log_path=None)
  driver.maximize_window()

  login(driver, params.login_url, params.email, params.password)

  done = False
  while True:
    for type, url in check_urls.items():
      while True:
        ret = PCheck(driver, url, type)
        if ret >= 0:
          break
        logging.error(f"Error checking for {type}, resetting...")
        login(driver, params.login_url, params.email, params.password)
      if ret == 0:
        logging.warning(f'Found slot for {type}!')
        if params.pushbullet_token:
          headers = {'Access-Token': params.pushbullet_token, 'Content-Type' : 'application/json'}
          data = f'{{"type": "note", "title": "Prenot@Mi", "body": "Found slot for {type}!"}}'
          requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, data=data)
        if params.stop_on_success:
          done = True
          break
      else:
        logging.info(f'No slot found for {type}...')
    if done:
      break
    time.sleep(params.check_interval_sec)

  driver.close()

if __name__ == "__main__":
  main()