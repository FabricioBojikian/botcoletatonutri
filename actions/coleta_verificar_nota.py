from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from driver.driver_chrome import DriverChrome
from PIL import Image
import pyautogui
import time
import os

chave_imput_xpath = '//*[@id="chave"]'
captcha_xpath = '//*[@id="rc-imageselect"]'
bt_popup_ok = '/html/body/div[1]/div[5]/div/div/div/div/div/div/div/a[1]'
bt_busca_xpath = '/html/body/div[1]/div[2]/div/div[1]/div/div[1]/form[1]/button'
bt_download_xpath = '/html/body/div[1]/div[4]/div/div/div[2]/div/div[3]/p[2]/a'
url_nota = 'https://consultadanfe.com/'

def buscar_conteudo(cor):
    screenshot = pyautogui.screenshot()
    screenshot.save('cor.png')
    img = Image.open('cor.png')
    width, height = img.size

    try:
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                if pixel[:3] == cor:
                    return True
                
        time.sleep(1)
        return False

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        time.sleep(1)
        return False

def verificar_codigo_barras(codigo_barras):

    while True:
        chrome_options = webdriver.ChromeOptions()
        prefs = {'safebrowsing.enabled': 'false'}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(url_nota)
        time.sleep(4)

        # ----------------------------------------------------------------- Baixar Nota Fiscal
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, bt_popup_ok).click()
        driver.implicitly_wait(10)            
        driver.find_element(By.XPATH, chave_imput_xpath).send_keys(codigo_barras)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, bt_busca_xpath).click()
        driver.implicitly_wait(10)
        time.sleep(1)

        cor_captcha = (26,115,232)

        if not buscar_conteudo(cor_captcha):
            print('Sem captcha, seguindo...')
            print(" ")

            cor = (248, 215, 218)

            if not buscar_conteudo(cor):
                print('Código de barras correto.')
                print(" ")
                retorno = True
                time.sleep(1)
                driver.quit()
                return retorno
            
            else:
                print('Código de barras incorreto.')
                print(" ")
                retorno = False
                time.sleep(1)
                driver.quit()
                return retorno
        
        else:
            print('Captcha detectado, reiniciando o processo...')
            print(" ")
            driver.quit()