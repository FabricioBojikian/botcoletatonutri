import tkinter as tk
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from db.database_bigquery import DatabaseBigQuery

store_url = "http://tinywebdb.appinventor.mit.edu/storeavalue"
store_tag_enviar = "datametria.io_confirmacao"
store_tag_ligar = "datametria.io_boton"
tag_imput_xpath = '/html/body/form/p[1]/input'
value_imput_xpath = '/html/body/form/p[2]/input'
store_imput_xpath = '/html/body/form/input[2]'

def enviar_ativacao(ativacao_estado):
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(store_url)
    driver.implicitly_wait(10)

    if ativacao_estado:
        value_imput = "1"
    else:
        value_imput = "0"

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(store_tag_ligar)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys(value_imput)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("Falha no envio da confirmação, tentando novamente...")
            print(" ")

            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(store_url)
            driver.implicitly_wait(10)

def enviar_confirmacao():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(store_url)
    driver.implicitly_wait(10)

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(store_tag_enviar)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys("1")
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("Falha no envio da confirmação, tentando novamente...")
            print(" ")

            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(store_url)
            driver.implicitly_wait(10)

def enviar_falha():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(store_url)
    driver.implicitly_wait(10)

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(store_tag_enviar)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys("2")
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("Falha no envio da confirmação, tentando novamente...")
            print(" ")

            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(store_url)
            driver.implicitly_wait(10)