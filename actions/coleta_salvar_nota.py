import tkinter as tk
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from db.database_bigquery import DatabaseBigQuery

from actions.coleta_log_error import *
from actions.coleta_resposta import *

def salvar_nota(n_nf, n_oc, n_bol):
    attempts = 0
    max_attempts = 3
    falha_salvar = False

    while attempts < max_attempts:
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

            print("Dados inseridos com sucesso na tabela notas_tonutri!")
            print(" ")

            enviar_confirmacao()

            return falha_salvar

        except Exception as e:
            attempts += 1

            print("Erro ao salvar, tentando novamente em 10 segundos...")
            print(" ")

            time.sleep(10)

            if attempts == max_attempts:
                falha_salvar = True
                ativacao_estado = False

                enviar_falha()
                time.sleep(5)
                enviar_ativacao(ativacao_estado)

                return falha_salvar