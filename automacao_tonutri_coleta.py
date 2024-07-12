import tkinter as tk
import requests
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from db.database_bigquery import DatabaseBigQuery

url_store = "http://tinywebdb.appinventor.mit.edu/storeavalue"
tag_store = "datametria.io_confirmacao"
tag_boton = "datametria.io_boton"
tag_imput_xpath = '/html/body/form/p[1]/input'
value_imput_xpath = '/html/body/form/p[2]/input'
store_imput_xpath = '/html/body/form/input[2]'

running = True
falha_ocorrida = False

def log_error(message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

def enviar_confirmacao():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_store)
    time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(tag_store)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys("1")
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("---------------------------------------------------------------------------")
            print("Falha no envio da confirmação, tentando novamente...")
            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url_store)
            time.sleep(1)

def falha_processo():
    global falha_ocorrida
    falha_ocorrida = True
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_store)
    time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(tag_store)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys("2")
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("---------------------------------------------------------------------------")
            print("Falha no envio da confirmação, tentando novamente...")
            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url_store)
            time.sleep(1)

def salvar_bd(n_nf, n_oc, n_bol):
    try:
        data = {
            "n_nf": [n_nf],
            "n_oc": [n_oc],
            "n_bol": [n_bol],
            "processado": [False],
            "erro_processamento": [False]
        }

        dataframe = pd.DataFrame(data)
        db = DatabaseBigQuery()
        db.data_load(dataframe=dataframe, destination_table="notas_tonutri", replace=False)
        print(f"Dados inseridos com sucesso na tabela notas_tonutri.")

    except Exception as e:
        error_message = f"Erro ao salvar no banco de dados: {str(e)}"
        print(error_message)
        log_error(error_message)
        falha_processo()

def main():
    global running, falha_ocorrida

    url_get = "http://tinywebdb.appinventor.mit.edu/getvalue"
    old_n_oc = None

    print("---------------------------------------------------------------------------")
    print("Ativando bot para o aplicativo...")

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_store)
    time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(tag_boton)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys("1")
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("---------------------------------------------------------------------------")
            print("Falha no envio da confirmação, tentando novamente...")
            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url_store)
            time.sleep(1)

    print("---------------------------------------------------------------------------")
    print("Coletando codigos de barras...")
    print(" ")

    while running:
        data = {
            "tag": "datametria.io_codigo_barras",
        }

        try:
            response = requests.post(url_get, data=data)

            if response.status_code == 200:
                try:
                    json_data = json.loads(response.text)
                    texto_limpo = json_data[2].replace('\'"', '').replace('"\'', '').replace('\\', '')
                    texto_limpo = texto_limpo[1:-1]
                    json_valido = json.loads(texto_limpo)

                    print("Aguardando leitura do aplicativo...")
                    print(f" - Ultima OC: {json_valido['OC']}")
                    print(" ")

                    if old_n_oc != json_valido['OC']:
                        if old_n_oc is not None:
                            print("---------------------------------------------------------------------------")
                            print("Salvando NF no banco de dados...")

                            salvar_bd(json_valido['NF'], json_valido['OC'], json_valido['BOLETOS'])

                            if not falha_ocorrida:
                                print("---------------------------------------------------------------------------")
                                print("Enviando confirmação para o aplicativo...")
                                enviar_confirmacao()

                        old_n_oc = json_valido['OC']

                except json.JSONDecodeError:
                    print("Deu erro no json!")
                    error_message = response.text
                    print(error_message)
                    log_error(error_message)

                except IndexError:
                    print("---------------------------------------------------------------------------")
                    print("Índice inválido no JSON")

            else:
                print("---------------------------------------------------------------------------")
                error_message = f"Erro {response.status_code} ao fazer a requisição"
                print(error_message)
                log_error(error_message)
                falha_processo()

        except requests.ConnectionError:
            print("---------------------------------------------------------------------------")
            print("Sem conexão com a internet, tentando novamente em 5 segundos...")
            print(" ")
            time.sleep(5)
            continue

        root.update()
        time.sleep(2)

def stop_loop():
    global running
    running = False
    root.destroy()

root = tk.Tk()
root.title("Automação Tonutri Coleta")
root.geometry("400x200")
label = tk.Label(root, text="Para cancelar a coleta, clique em Parar", font=("Arial", 12))
label.pack(pady=20)
stop_button = tk.Button(root, text="Parar", font=("Arial", 14), command=stop_loop)
stop_button.pack(pady=20)

def run_loop():
    main()
    print("---------------------------------------------------------------------------")
    print("Desativando bot e notificando o aplicativo...")

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_store)
    time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, tag_imput_xpath).send_keys(tag_boton)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, value_imput_xpath).send_keys("0")
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, store_imput_xpath).click()
            driver.implicitly_wait(10)
            driver.quit()
            time.sleep(1)
            break

        except NoSuchElementException:
            print("---------------------------------------------------------------------------")
            print("Falha no envio da confirmação, tentando novamente...")
            driver.quit()
            time.sleep(1)
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url_store)
            time.sleep(1)

    print("---------------------------------------------------------------------------")
    print("Processo de coleta finalizado!")

root.after(0, run_loop)
root.mainloop()
