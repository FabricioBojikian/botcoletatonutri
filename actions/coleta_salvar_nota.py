import tkinter as tk
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from db.database_bigquery import DatabaseBigQuery

from actions.coleta_log_error import *
from actions.coleta_resposta import *

def salvar_nota(n_nf, n_oc, n_bol):
    # falha_salvar = False
    
    # try:
    #     data = {
    #         "n_nf": [n_nf],
    #         "n_oc": [n_oc],
    #         "n_bol": [n_bol],
    #         "processado": [False],
    #         "erro_processamento": [False]
    #     }

    #     dataframe = pd.DataFrame(data)
    #     db = DatabaseBigQuery()
    #     db.data_load(dataframe=dataframe, destination_table="notas_tonutri", replace=False)

    #     print(f"Dados inseridos com sucesso na tabela destination_table!")
    #     print(" ")

    #     enviar_confirmacao()

    # except Exception as e:
    #     falha_salvar = True

    #     error_message = f"Erro ao salvar no banco de dados: {str(e)}"
    #     print(error_message)
    #     log_error(error_message)

    #     enviar_falha()

    falha_salvar = True

    error_message = "Erro ao salvar no banco de dados:"
    print(error_message)
    log_error(error_message)

    enviar_falha()

    return falha_salvar